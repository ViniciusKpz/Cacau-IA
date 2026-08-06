import os
import glob
import subprocess
from datetime import datetime
from duckduckgo_search import DDGS
from core.ajuda import AjudaCacauIA
from core.ia import IAEngine

class CacauIA:
    def __init__(self):
        self.pasta_output = "output"
        self.ajuda = AjudaCacauIA()
        self.ia = IAEngine()

    def saudar(self, nome: str = "Dev"):
        print(f"\nOlá, {nome}! 🍫\nEu sou a CacauIA, sua assistente no Arch Linux.")

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
            print(f"❌ Aplicativo '{app}' não encontrado no Arch Linux.")

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

        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        pasta_destino = os.path.join(diretorio_script, "..", self.pasta_output)
        os.makedirs(pasta_destino, exist_ok=True)

        nome_arquivo = f"{termo.lower().strip().replace(' ', '_')}.txt"
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)

        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(conteudo_final)

        print(f"✨ Pesquisa salva em: {caminho_completo}")

    def abrir_arquivo(self, nome_entrada: str):
        nome_limpo = nome_entrada.lower().strip().replace(" ", "_")
        if not nome_limpo.endswith(".txt"):
            nome_limpo += ".txt"

        caminho = os.path.join(os.getcwd(), self.pasta_output, nome_limpo)
        if os.path.exists(caminho):
            print(f"\n📖 Lendo: {caminho}\n" + "="*40)
            with open(caminho, "r", encoding="utf-8") as f:
                print(f.read())
            print("="*40)
        else:
            print(f"❌ Arquivo '{nome_limpo}' não foi encontrado.")

    def excluir_pesquisa(self, termo: str):
        pasta = os.path.join(os.getcwd(), self.pasta_output)
        if not os.path.exists(pasta):
            print("⚠️ Nenhuma pesquisa para excluir.")
            return

        termo_limpo = termo.lower().strip()
        if termo_limpo in ["todas", "tudo", "*"]:
            for arq in glob.glob(os.path.join(pasta, "*.txt")):
                os.remove(arq)
            print("🗑️ Todas as pesquisas foram excluídas!")
            return

        nome_arquivo = termo_limpo.replace(" ", "_")
        if not nome_arquivo.endswith(".txt"):
            nome_arquivo += ".txt"

        caminho = os.path.join(pasta, nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)
            print(f"🗑️ Arquivo '{nome_arquivo}' removido!")
        else:
            print(f"❌ Arquivo '{nome_arquivo}' não encontrado.")