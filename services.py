import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def load_orders():
    return json.loads((DATA_DIR / "orders.json").read_text(encoding="utf-8"))

def load_return_policy():
    return json.loads((DATA_DIR / "return_policy.json").read_text(encoding="utf-8"))

def find_order(tracking_number: str):
    tracking_number = tracking_number.strip().upper()
    for order in load_orders():
        if order["tracking_number"].upper() == tracking_number:
            return order
    return None

def evaluate_return(order: dict, opened: bool = False):
    policy = load_return_policy()
    category = order["category"]

    if category == "perecedero":
        return {
            "eligible": False,
            "reason": policy["non_returnable_categories"]["perecedero"],
            "action": "Explicar la restricción con empatía y ofrecer escalamiento si existe una reclamación por daño o error."
        }

    if category == "higiene" and opened:
        return {
            "eligible": False,
            "reason": policy["non_returnable_categories"]["higiene"],
            "action": "Explicar la restricción de higiene y ofrecer revisión humana si el producto llegó defectuoso."
        }

    if category in policy["returnable_categories"]:
        return {
            "eligible": True,
            "reason": policy["returnable_categories"][category],
            "action": f"Verificar que la solicitud esté dentro de {policy['return_window_days']} días y registrar la devolución."
        }

    if category == "higiene" and not opened:
        return {
            "eligible": True,
            "reason": "El producto de higiene no presenta apertura reportada; puede pasar a validación dentro del plazo.",
            "action": "Validar sellado, plazo y condiciones antes de autorizar."
        }

    return {
        "eligible": None,
        "reason": "La política no permite determinar la elegibilidad con certeza.",
        "action": policy["escalation_rule"]
    }

def deterministic_order_response(order: dict):
    if not order:
        return (
            "No puedo verificar ese número de seguimiento en la base de prueba. "
            "Por favor valida el número o solicita apoyo de un agente humano."
        )

    parts = [f"El pedido {order['tracking_number']} está actualmente en estado: {order['status']}."]
    if order.get("estimated_delivery"):
        parts.append(f"La fecha estimada de entrega es {order['estimated_delivery']}.")
    if order.get("carrier") and order["carrier"] != "No aplica":
        parts.append(f"Transportadora: {order['carrier']}.")
    if order.get("tracking_url"):
        parts.append(f"Seguimiento: {order['tracking_url']}.")
    if order.get("status", "").lower() == "retrasado":
        reason = order.get("delay_reason") or "motivo no disponible"
        parts.append(f"Lamentamos el retraso. Motivo registrado: {reason}.")
    if order.get("status", "").lower() == "cancelado":
        parts.append("El pedido fue cancelado antes del despacho.")
    return " ".join(parts)
