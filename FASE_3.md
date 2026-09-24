# Fase 3. Aplicación de Ingeniería de Prompts

## 3.1 Objetivo

La tercera fase busca demostrar cómo la estructura de un prompt modifica la calidad de la respuesta generada por un modelo de lenguaje. Para ello se implementan dos escenarios: consulta del estado de un pedido y gestión de devoluciones.

## 3.2 Principios utilizados

Los prompts fueron diseñados con los siguientes componentes:

1. **Rol:** define el comportamiento esperado del modelo.
2. **Objetivo:** especifica la tarea.
3. **Contexto:** suministra la información empresarial necesaria.
4. **Restricciones:** limita comportamientos no deseados, especialmente la invención de datos.
5. **Instrucciones de salida:** establece el tono y el contenido esperado.
6. **Mecanismo de escalamiento:** obliga al modelo a reconocer cuándo no dispone de información suficiente.

## 3.3 Prompt para consulta de pedido

Un prompt básico como:

`Dame el estado del pedido EM-1001`

es insuficiente porque el modelo no posee necesariamente acceso al sistema transaccional de EcoMarket.

Por ello se construye primero un contexto a partir de `orders.json` y luego se genera un prompt estructurado. El modelo recibe el estado real, la transportadora, la fecha estimada y el enlace de seguimiento. Además, se le prohíbe inventar información.

La regla principal utilizada es:

> Usa exclusivamente los datos del contexto. No inventes estados, fechas, transportadoras, enlaces ni motivos.

Si un pedido se encuentra retrasado, el prompt solicita una disculpa breve y una explicación basada únicamente en el motivo almacenado.

## 3.4 Base simulada

Se creó el archivo `data/orders.json` con 12 pedidos. Cada registro contiene:

- número de seguimiento;
- nombre;
- producto;
- categoría;
- estado;
- transportadora;
- fecha estimada;
- enlace de seguimiento;
- motivo de retraso.

Esta base funciona como sustituto controlado del sistema de pedidos real.

## 3.5 Prompt para devoluciones

El segundo prompt utiliza `return_policy.json`.

La política simulada distingue productos retornables y categorías con restricciones especiales.

Los productos perecederos no son aceptados en una devolución ordinaria. Los productos de higiene requieren comprobar que no hayan sido abiertos o utilizados. Para otras categorías se aplican condiciones de plazo y estado.

La respuesta debe mantener un tono empático incluso cuando la devolución sea rechazada.

## 3.6 Prevención de alucinaciones

La solución aplica cuatro controles:

1. Contexto recuperado desde archivos JSON.
2. Instrucción explícita de no inventar información.
3. Respuesta alternativa cuando faltan datos.
4. Escalamiento a un agente humano para casos ambiguos.

## 3.7 Uso opcional de un LLM local

El proyecto incluye integración con Ollama mediante `ollama_client.py`.

De esta forma es posible ejecutar los mismos prompts sobre un modelo open-source instalado localmente, por ejemplo `phi3:mini`.

Esto permite comparar:

- respuesta determinística basada en reglas;
- respuesta generada por IA a partir del mismo contexto.

## 3.8 Resultado esperado

La práctica demuestra que un prompt bien estructurado ofrece mayor control que una instrucción simple.

El patrón utilizado puede resumirse como:

**Rol + tarea + contexto confiable + restricciones + formato de respuesta + escalamiento.**

En un entorno empresarial real, los archivos JSON serían sustituidos por APIs conectadas al CRM, inventario, sistema de pedidos y plataforma logística de EcoMarket.
