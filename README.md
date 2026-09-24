# Taller Práctico #1 — EcoMarket

## Caso de estudio
Optimización de la atención al cliente mediante Inteligencia Artificial Generativa.

La solución implementa una demostración de ingeniería de prompts para dos escenarios:

1. Consulta del estado de un pedido utilizando un número de seguimiento.
2. Evaluación de una solicitud de devolución, diferenciando productos retornables y no retornables.

El repositorio incluye una base simulada con 12 pedidos, por lo que supera el mínimo de 10 registros requerido para el ejercicio.

## Arquitectura

Cliente
→ Aplicación Python
→ Búsqueda de pedido / política
→ Construcción del prompt
→ Respuesta determinística o LLM local
→ Cliente

Para demostración con IA generativa:

Cliente
→ Python
→ JSON
→ Prompt estructurado
→ Ollama
→ LLM local
→ Respuesta

## Estructura

```text
ecomarket_taller1/
├── app.py
├── prompts.py
├── services.py
├── ollama_client.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── orders.json
│   └── return_policy.json
└── tests/
    ├── __init__.py
    └── test_services.py
```

## Requisitos

- Python 3.10 o superior.
- Opcional: Ollama, si se desea generar respuestas con un LLM local.
- Modelo sugerido para la práctica: `phi3:mini`.

El proyecto funciona sin instalar librerías externas.

## Ejecución sin LLM

### Consultar estado de pedido

```bash
python app.py order EM-1001
```

Ejemplo con un pedido retrasado:

```bash
python app.py order EM-1003
```

### Evaluar devolución

Producto retornable:

```bash
python app.py return EM-1010
```

Producto perecedero:

```bash
python app.py return EM-1003
```

Producto de higiene abierto:

```bash
python app.py return EM-1002 --opened
```

### Modo interactivo

```bash
python app.py interactive
```

## Ejecución con Ollama

Primero verificar que Ollama esté instalado y que el modelo exista localmente.

Ejemplo:

```bash
ollama pull phi3:mini
```

Luego:

```bash
python app.py --llm order EM-1001
```

Para devolución:

```bash
python app.py --llm return EM-1002 --opened
```

También puede seleccionarse otro modelo:

```bash
python app.py --llm --model llama3.1:8b order EM-1003
```

## Diseño del Prompt 1 — Estado del pedido

El prompt utiliza cinco elementos:

- rol;
- objetivo;
- reglas;
- contexto;
- pregunta.

Una regla central es que el modelo debe utilizar exclusivamente los datos recuperados desde la base simulada y no debe inventar estados, fechas, transportadoras ni enlaces.

Esto permite demostrar la diferencia entre un prompt básico como:

> Dame el estado del pedido EM-1001.

y un prompt estructurado que proporciona rol, contexto, restricciones y formato esperado.

## Diseño del Prompt 2 — Devoluciones

El prompt de devoluciones recibe:

- datos del pedido;
- categoría del producto;
- condición de apertura;
- política de devolución.

El sistema diferencia, entre otros:

- productos perecederos;
- productos de higiene;
- textiles;
- papelería;
- artículos reutilizables;
- productos de limpieza.

Los casos ambiguos deben escalarse a un agente humano.

## Pruebas

Ejecutar:

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican:

- existencia de pedidos;
- manejo de pedidos inexistentes;
- rechazo de perecederos;
- rechazo de productos de higiene abiertos;
- aceptación de productos textiles bajo la política simulada.

## Evidencia sugerida para el informe

Tomar capturas de:

1. `python app.py order EM-1001`
2. `python app.py order EM-1003`
3. `python app.py return EM-1010`
4. `python app.py return EM-1003`
5. `python app.py return EM-1002 --opened`
6. Una ejecución con `--llm`, si Ollama está disponible.

Comparar el prompt básico con el prompt mejorado y explicar por qué el segundo reduce ambigüedad y riesgo de alucinaciones.

## Conclusión

La demostración muestra cómo la ingeniería de prompts puede combinarse con datos empresariales estructurados para obtener respuestas más controladas. El LLM se utiliza para generar lenguaje natural, mientras que los datos del pedido y las políticas actúan como fuente de verdad.
