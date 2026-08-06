import requests

class IAEngine:
    def __init__(self, modelo="llama3.2", url="http://localhost:11434"):
        self.modelo = modelo
        self.url_generate = f"{url}/api/generate"
        self.disponivel = self._verificar_ollama(url)

    def _verificar_ollama(self, url: str) -> bool:
        try:
            return requests.get(f"{url}/", timeout=1).status_code == 200
        except Exception:
            return False

    def resumir_texto(self, termo: str, texto_bruto: str) -> str:
        if not self.disponivel:
            return texto_bruto

        prompt = f"Você é a CacauIA. Sintetize as informações sobre '{termo}':\n\n{texto_bruto}"

        try:
            res = requests.post(
                self.url_generate,
                json={"model": self.modelo, "prompt": prompt, "stream": False},
                timeout=20
            )
            if res.status_code == 200:
                resumo = res.json().get("response", "").strip()
                if resumo:
                    return f"=== RESUMO CACAU IA: {termo.upper()} ===\n\n{resumo}\n\n=== FONTES BRUTAS ===\n{texto_bruto}"
        except Exception:
            pass

        return texto_bruto