import requests
import json

class IAEngine:
    def __init__(self, modelo="llama3.2", url="http://localhost:11434"):
        self.modelo = modelo
        self.url_generate = f"{url}/api/generate"
        self.url_chat = f"{url}/api/chat"
        self.disponivel = self._verificar_ollama(url)
        self.historico = [
            {"role": "system", "content": "Você é a CacauIA, uma assistente virtual focada em Linux. Responda de forma direta, simpática e amigável."}
        ]

    def _verificar_ollama(self, url: str) -> bool:
        try:
            return requests.get(f"{url}/", timeout=1).status_code == 200
        except Exception:
            return False

    def conversar(self, mensagem_usuario: str) -> str:
        if not self.disponivel:
            return "❌ O serviço Ollama não está rodando. Inicie com 'ollama serve' no terminal."

        self.historico.append({"role": "user", "content": mensagem_usuario})

        try:
            res = requests.post(
                self.url_chat,
                json={
                    "model": self.modelo,
                    "messages": self.historico,
                    "stream": False
                },
                timeout=120
            )
            if res.status_code == 200:
                resposta = res.json().get("message", {}).get("content", "").strip()
                self.historico.append({"role": "assistant", "content": resposta})
                return resposta
        except Exception as e:
            return f"❌ Erro ao conectar com o Ollama: {e}"

        return "⚠️ Não foi possível obter resposta da IA."

    def interpretar_intencao(self, texto: str) -> dict:
        """Usa a IA para classificar o texto do usuário em um comando estruturado."""
        if not self.disponivel:
            return {"acao": "chat", "parametro": texto}

        prompt = f"""Analise a frase do usuário e retorne APENAS um objeto JSON no formato exato:
{{"acao": "<NOME_DA_ACAO>", "parametro": "<PARAMETRO>"}}

Ações válidas:
- "app": abrir um aplicativo (parametro = nome do programa, ex: firefox, spotify, alacritty)
- "buscar": pesquisar algo na web (parametro = termo da pesquisa)
- "relogio": ver horas ou data (parametro = "")
- "ver": ler um arquivo de pesquisa salvo (parametro = nome do termo)
- "excluir": apagar arquivos gravados (parametro = termo ou "todas")
- "chat": qualquer outra conversa, dúvida ou interação normal

Frase: "{texto}"
JSON:"""

        try:
            res = requests.post(
                self.url_generate,
                json={
                    "model": self.modelo,
                    "prompt": prompt,
                    "format": "json",
                    "stream": False
                },
                timeout=10
            )
            if res.status_code == 200:
                dados = json.loads(res.json().get("response", "{}"))
                return dados
        except Exception:
            pass

        return {"acao": "chat", "parametro": texto}

    def resumir_texto(self, termo: str, texto_bruto: str) -> str:
        if not self.disponivel:
            return texto_bruto

        prompt = f"Sintetize as informações sobre '{termo}':\n\n{texto_bruto}"
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