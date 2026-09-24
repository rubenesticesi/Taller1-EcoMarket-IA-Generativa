import json
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_with_ollama(prompt: str, model: str = "phi3:mini") -> str:
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("response", "").strip()
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "No fue posible conectar con Ollama. Verifica que esté ejecutándose "
            "y que el modelo indicado esté instalado."
        ) from exc
