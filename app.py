import argparse
from prompts import order_status_prompt, return_prompt
from services import (
    find_order,
    load_return_policy,
    evaluate_return,
    deterministic_order_response,
    deterministic_return_response,
)
from ollama_client import generate_with_ollama

def show_order(tracking_number: str, use_llm: bool, model: str):
    order = find_order(tracking_number)
    if not order:
        print(deterministic_order_response(None))
        return

    prompt = order_status_prompt(order)

    print("\n=== PROMPT GENERADO ===\n")
    print(prompt)

    print("\n=== RESPUESTA ===\n")
    if use_llm:
        print(generate_with_ollama(prompt, model=model))
    else:
        print(deterministic_order_response(order))

def show_return(tracking_number: str, opened: bool, use_llm: bool, model: str):
    order = find_order(tracking_number)
    if not order:
        print("No se encontró el pedido. Verifica el número o escala el caso.")
        return

    policy = load_return_policy()
    prompt = return_prompt(order, policy, opened=opened)
    evaluation = evaluate_return(order, opened=opened)

    print("\n=== PROMPT GENERADO ===\n")
    print(prompt)

    print("\n=== EVALUACIÓN DE POLÍTICA ===\n")
    print(f"Elegible: {evaluation['eligible']}")
    print(f"Razón: {evaluation['reason']}")
    print(f"Acción: {evaluation['action']}")

    print("\n=== RESPUESTA AL CLIENTE ===\n")
    if use_llm:
        print(generate_with_ollama(prompt, model=model))
    else:
        print(deterministic_return_response(order, evaluation))

def interactive(use_llm: bool, model: str):
    print("EcoMarket - Taller Práctico #1")
    print("1. Consultar estado de pedido")
    print("2. Evaluar devolución")
    option = input("Seleccione una opción: ").strip()

    if option == "1":
        tracking = input("Número de seguimiento (ej. EM-1001): ").strip()
        show_order(tracking, use_llm, model)
    elif option == "2":
        tracking = input("Número de seguimiento (ej. EM-1002): ").strip()
        opened_text = input("¿El producto fue abierto/usado? (s/n): ").strip().lower()
        show_return(tracking, opened_text == "s", use_llm, model)
    else:
        print("Opción no válida.")

def main():
    parser = argparse.ArgumentParser(
        description="EcoMarket - demostración de ingeniería de prompts"
    )
    parser.add_argument("--llm", action="store_true", help="Usar Ollama para generar la respuesta")
    parser.add_argument("--model", default="phi3:mini", help="Modelo Ollama, por defecto phi3:mini")

    subparsers = parser.add_subparsers(dest="command")

    order_parser = subparsers.add_parser("order", help="Consultar un pedido")
    order_parser.add_argument("tracking_number")

    return_parser = subparsers.add_parser("return", help="Evaluar una devolución")
    return_parser.add_argument("tracking_number")
    return_parser.add_argument("--opened", action="store_true")

    subparsers.add_parser("interactive", help="Modo interactivo")

    args = parser.parse_args()

    if args.command == "order":
        show_order(args.tracking_number, args.llm, args.model)
    elif args.command == "return":
        show_return(args.tracking_number, args.opened, args.llm, args.model)
    else:
        interactive(args.llm, args.model)

if __name__ == "__main__":
    main()
