import os
import sys
import glob
import subprocess
from datetime import datetime
from duckduckgo_search import DDGS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.ajuda import AjudaCacauIA
from core.ia import IAEngine
from ASCII.banner import exibir_banner_principal

class CacauIA:
    def __init__(self):
        diretorio_core = os.path.dirname(os.path.abspath(__file__))
        self.pasta_output = os.path.abspath(os.path.join(diretorio_core, "..", "output"))
        self.ajuda = AjudaCacauIA()
        self.ia = IAEngine()

    def exibir_banner(self):
        exibir_banner_principal()

    def iniciar_chat(self):
        self.exibir_banner()
        print("💬 Modo Chat da CacauIA iniciado!")
        print("Digite sua mensagem em linguagem natural (ou 'sair' para encerrar).\n")

        while True:
            try:
                entrada = input("\033[1;36mVocê > \033[0m").strip()
                if not entrada:
                    continue

                if entrada.lower() in ["sair", "exit", "quit", "tchau"]:
                    self.despedir()
                    break

                intencao = self.ia.interpretar_intencao(entrada)
                acao = intencao.get("acao", "chat")
                param = intencao.get("parametro", "")

                if acao == "app" and param:
                    self.abrir_aplicativo(param)
                elif acao == "buscar" and param:
                    self.pesquisar_e_salvar(param)
                elif acao == "relogio":
                    self.mostrar_relogio()
                elif acao == "ver" and param:
                    self.abrir_arquivo(param)
                elif acao == "excluir" and param:
                    self.excluir_pesquisa(param)
                else:
                    resposta = self.ia.conversar(entrada)
                    print(f"\n🍫 \033[1;33mCacauIA >\033[0m {resposta}\n")

            except (KeyboardInterrupt, EOFError):
                self.despedir()
                break

    def saudar(self, nome: str = "Dev"):
        self.exibir_banner()
        print(f"Olá, {nome}! 🍫\nEu sou a CacauIA, sua assistente no Linux.\n")

    def despedir(self):
        print("\nDesligando módulos. Até logo! 👋🍫\n")

    def mostrar_relogio(self):
        agora = datetime.now()
        print(f"\n⏰ [CacauIA] Data: {agora.strftime('%d/%m/%Y')} | Hora: {agora.strftime('%H:%M:%S')}\n")

    def abrir_aplicativo(self, nome_app: str):
        app = nome_app.lower().strip()
        try:
            subprocess.Popen([app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✨ {app.capitalize()} iniciado!")
        except FileNotFoundError:
            print(f"❌ Aplicativo '{app}' não encontrado no sistema.")

    def pesquisar_e_salvar(self, termo: str):
        print(f"🔍 [CacauIA] Pesquisando sobre '{termo}'...")
        try:
            with DDGS() as ddgs:
                resultados = list(ddgs.text(termo, max_results=5))
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            return

        if not resultados:
            print("⚠️ Nenhum resultado encontrado.")
            return

        texto_bruto = ""
        for i, res in enumerate(resultados, 1):
            texto_bruto += f"[{i}] {res.get('title')}\n    {res.get('body')}\n    Link: {res.get('href')}\n\n"

        conteudo_final = self.ia.resumir_texto(termo, texto_bruto)
        os.makedirs(self.pasta_output, exist_ok=True)

        nome_arquivo = f"{termo.lower().strip().replace(' ', '_')}.txt"
        caminho_completo = os.path.join(self.pasta_output, nome_arquivo)

        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(conteudo_final)

        print(f"✨ Pesquisa salva em: {caminho_completo}")

    def abrir_arquivo(self, nome_entrada: str):
        nome_limpo = nome_entrada.lower().strip().replace(" ", "_")
        if not nome_limpo.endswith(".txt"):
            nome_limpo += ".txt"

        caminho = os.path.join(self.pasta_output, nome_limpo)
        if os.path.exists(caminho):
            print(f"\n📖 Lendo: {caminho}\n" + "="*40)
            with open(caminho, "r", encoding="utf-8") as f:
                print(f.read())
            print("="*40)
        else:
            print(f"❌ Arquivo '{nome_limpo}' não foi encontrado em output.")

    def excluir_pesquisa(self, termo: str):
        if not os.path.exists(self.pasta_output):
            print("⚠️ Nenhuma pesquisa para excluir.")
            return

        termo_limpo = termo.lower().strip()
        if termo_limpo in ["todas", "tudo", "*"]:
            for arq in glob.glob(os.path.join(self.pasta_output, "*.txt")):
                os.remove(arq)
            print("🗑️ Todas as pesquisas foram excluídas!")
            return

        nome_arquivo = termo_limpo.replace(" ", "_")
        if not nome_arquivo.endswith(".txt"):
            nome_arquivo += ".txt"

        caminho = os.path.join(self.pasta_output, nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)
            print(f"🗑️ Arquivo '{nome_arquivo}' removido!")
        else:
            print(f"❌ Arquivo '{nome_arquivo}' não encontrado.")