import json
import warnings
import requests

# Silencia o aviso de renomeação da biblioteca DuckDuckGo
warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")

class IAEngine:
    def __init__(self, modelo="llama3.2", url="http://localhost:11434"):
        self.modelo = modelo
        self.url_generate = f"{url}/api/generate"
        self.url_chat = f"{url}/api/chat"
        self.disponivel = self._verificar_ollama(url)
        self.historico = [
            {"role": "system", "content": "Você é a CacauIA, uma assistente virtual focada em Linux e tecnologia. Responda de forma direta, simpática e objetiva."}
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

        prompt = f"""Analise a frase do usuário e classifique o tipo de pedido. Retorne APENAS um objeto JSON no formato exato:
{{"acao": "<NOME_DA_ACAO>", "parametro": "<PARAMETRO>"}}

Ações válidas:
- "analisar": USE para qualquer pedido de ler, ver, inspecionar, olhar ou resumir PASTAS, DIRETÓRIOS ou ARQUIVOS do sistema (ex: "analisa ~/game", "oq tem em ~/Jogos", "ve o arquivo script.py", "olha o README.md").
- "ver": USE SOMENTE se o usuário pedir explicitamente para abrir um RELATÓRIO OU PESQUISA SALVA anterior na pasta output (ex: "abrir pesquisa salva X", "mostrar relatorio Y").
- "buscar": USE SOMENTE se o usuário pedir explicitamente para pesquisar/buscar na internet (ex: "pesquise sobre X", "busque na web Y", "procure no google Z").
- "app": abrir um aplicativo (ex: "abre o firefox", "inicia o spotify").
- "jogar": USE quando o usuário pedir para jogar algo (ex: "vamos jogar jogo da velha", "jogar velha").
- "relogio": ver horas ou data atual (ex: "que horas sao", "qual a data").
- "excluir": apagar arquivos gravados (ex: "deleta as pesquisas", "apaga o arquivo Z").
- "chat": QUALQUER OUTRA PERGUNTA, dúvida, conversa, explicação, conceito ou cálculo matematico (ex: "o que e sujeito", "quanto e 10 + 10", "me explica o kernel").

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
                timeout=120
            )
            if res.status_code == 200:
                resumo = res.json().get("response", "").strip()
                if resumo:
                    return f"=== RESUMO CACAU IA: {termo.upper()} ===\n\n{resumo}\n\n=== FONTES BRUTAS ===\n{texto_bruto}"
        except Exception:
            pass

        return texto_bruto