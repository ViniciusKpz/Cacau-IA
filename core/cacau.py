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

    def exibir_status(self):
        """Exibe o Dashboard Operacional da CacauIA no terminal ao chamar '!Papai chegou'."""
        import socket
        import subprocess
        import requests
        from pathlib import Path

        sistemas_ok = True

        try:
            res_rede = requests.get("https://1.1.1.1", timeout=3)
            if res_rede.status_code == 200:
                status_rede = "ONLINE (HTTP 200)"
                status_dns = "OK"
            else:
                status_rede = "ONLINE"
                status_dns = "OK"
        except Exception:
            try:
                res_dns = requests.get("https://www.google.com", timeout=3)
                status_rede = "ONLINE"
                status_dns = "OK"
            except Exception:
                status_rede = "OFFLINE"
                status_dns = "FALHA"
                sistemas_ok = False

        try:
            url_base = self.ia.url_generate.replace("/api/generate", "")
            res = requests.get(f"{url_base}/", timeout=1)
            if res.status_code == 200:
                status_ollama = "ONLINE (HTTP 200)"
            else:
                status_ollama = "ERRO"
                sistemas_ok = False
        except Exception:
            status_ollama = "OFFLINE"
            sistemas_ok = False

        raiz = Path(__file__).resolve().parent.parent
        try:
            commit_atual = subprocess.check_output(
                ["git", "log", "-1", "--pretty=format:%s"],
                cwd=raiz, text=True, stderr=subprocess.DEVNULL
            ).strip()
        except Exception:
            commit_atual = "Não identificado"

        try:
            subprocess.run(["git", "fetch"], cwd=raiz, timeout=2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            status_git = subprocess.check_output(
                ["git", "status", "-sb"],
                cwd=raiz, text=True, stderr=subprocess.DEVNULL
            ).strip().splitlines()[0]

            if "behind" in status_git:
                sinc_github = "Desatualizado (commits pendentes no GitHub)"
            else:
                sinc_github = "Atualizado com o GitHub"
        except Exception:
            sinc_github = "Erro ao conectar com o GitHub"

        candidatos = [
            raiz / ".funcoes" / "Jogar",
            raiz / ".funcoes" / "jogar",
            raiz / "Jogar",
            raiz / "jogar",
        ]

        pasta_jogos = None
        num_jogos = 0

        for c in candidatos:
            if c.exists():
                conteudo = [
                    f for f in c.iterdir() 
                    if (f.is_dir() or f.suffix == ".py") 
                    and not f.name.startswith("__") 
                    and not f.name.startswith(".")
                ]
                if len(conteudo) > 0:
                    pasta_jogos = c
                    num_jogos = len(conteudo)
                    break
                elif pasta_jogos is None:
                    pasta_jogos = c

        if not pasta_jogos:
            pasta_jogos = raiz / ".funcoes" / "Jogar"

        nome_exibicao = f"{pasta_jogos.parent.name}/{pasta_jogos.name}" if pasta_jogos.parent.name.startswith(".") else pasta_jogos.name

        print("\n=== CACAU IA - OPERATOR DASHBOARD & DIAGNOSTICS ===")
        print('"Bem-vindo de volta, Senhor. Todos os sistemas estão operacionais."\n')

        print("REDE & CONEXAO")
        print(f"  [-] Conexao com a Internet ........ {status_rede}")
        print(f"  [-] Resolucao de DNS .............. {status_dns}")

        print("\nMOTOR DE IA (OLLAMA)")
        print(f"  [-] Servico Ollama (localhost) .... {status_ollama}")
        print(f"  [-] Modelo {getattr(self.ia, 'modelo', 'llama3.2')} .............. CARREGADO")

        print("\nREPOSITORIO GITHUB / VERSAO")
        print(f"  [-] Versao Atual (Sistema IA) ......... {commit_atual}")
        print(f"  [-] Sincronizacao Remota .......... {sinc_github}")

        print("\nESTRUTURA DO SISTEMA")
        print(f"  [-] Diretorio Raiz ({raiz}) ... OK")
        print(f"  [-] Modulo de Jogos ({nome_exibicao}/) ...... OK ({num_jogos} jogos encontrados)")
        print(f"  [-] Pasta de Saida ({self.pasta_output}) ...... OK")

        print("\n----------------------------------------------------")
        
        # Indicador visual exclusivo para o Status Geral
        if sistemas_ok:
            print("STATUS GERAL: 🟢 SISTEMA OPERACIONAL E PRONTO\n")
        else:
            print("STATUS GERAL: 🔴 FALHA EM UM OU MAIS SISTEMAS\n")

    def exibir_banner(self):
        exibir_banner_principal()

    def iniciar_chat(self):
        self.exibir_banner()
        print(" Modo Chat da CacauIA iniciado!")
        print("Digite sua mensagem em linguagem natural (ou 'sair' para encerrar).\n")

        if entrada.lower() in ["!papai chegou", "!papai_chegou", "papai chegou", "status", "operador"]:
                self.exibir_status()

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

                elif acao == "jogar":
                    self.jogar(param)

                elif acao == "buscar" and param:
                    self.pesquisar_e_salvar(param)
                elif acao == "analisar" and param:
                    print(f" [CacauIA] Inspecionando '{param}'...")
                    import importlib.util
                    from pathlib import Path

                    raiz = Path(__file__).resolve().parent.parent
                    caminho_script = raiz / ".funcoes" / "navegar" / "analise.py"

                    spec = importlib.util.spec_from_file_location("analise_modulo", caminho_script)
                    modulo_navegar = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(modulo_navegar)

                    analisar_caminho = modulo_navegar.analisar_caminho

                    dados_extraidos = analisar_caminho(param)

                    prompt_contexto = (
                        f"O usuário pediu para analisar o caminho '{param}'. "
                        f"Abaixo estão os dados coletados do sistema:\n\n{dados_extraidos}\n\n"
                        f"Faça um resumo explicativo e amigável sobre o que é este projeto ou arquivo."
                    )

                    resposta = self.ia.conversar(prompt_contexto)
                    print(f"\n \033[1;33mCacauIA >\033[0m {resposta}\n")
                elif acao == "relogio":
                    self.mostrar_relogio()
                elif acao == "ver" and param:
                    self.abrir_arquivo(param)
                elif acao == "excluir" and param:
                    self.excluir_pesquisa(param)
                else:
                    resposta = self.ia.conversar(entrada)
                    print(f"\n \033[1;33mCacauIA >\033[0m {resposta}\n")

            except (KeyboardInterrupt, EOFError):
                self.despedir()
                break
    def jogar(self, nome_jogo: str = None):
        """Lista e executa jogos disponíveis procurando em múltiplos caminhos."""
        import importlib.util
        from pathlib import Path

        raiz = Path(__file__).resolve().parent.parent

        caminhos_possiveis = [
            raiz / "Jogar",
            raiz / "jogar",
            raiz / "Jogos",
            raiz / "jogos",
            raiz / ".funcoes" / "Jogar",
            raiz / ".funcoes" / "jogar",
            raiz / ".funcoes" / "Jogos",
            raiz / ".funcoes" / "jogos",
        ]

        pasta_jogos = None
        for caminho in caminhos_possiveis:
            if caminho.exists() and caminho.is_dir():
                pasta_jogos = caminho
                break

        if not pasta_jogos:
            print(f" Nenhuma pasta de jogos foi encontrada em '{raiz}'. Crie a pasta 'Jogar' ou '.funcoes/jogar'.")
            return

        jogos_disponiveis = {}
        for pasta in pasta_jogos.iterdir():
            if pasta.is_dir():
                # Procura script executável
                script = pasta / "main.py"
                if not script.exists():
                    # Procura por qualquer .py dentro da pasta
                    scripts_py = list(pasta.glob("*.py"))
                    if scripts_py:
                        script = scripts_py[0]

                if script and script.exists():
                    jogos_disponiveis[pasta.name.lower()] = script

        if not jogos_disponiveis:
            print(f" Nenhum jogo com script .py executável foi encontrado em '{pasta_jogos}'.")
            return

        jogo_escolhido = (nome_jogo or "").lower()
        script_alvo = None

        for chave, caminho in jogos_disponiveis.items():
            if jogo_escolhido and (jogo_escolhido in chave or chave in jogo_escolhido):
                script_alvo = caminho
                break

        if not script_alvo:
            print("\n🎮 \033[1;33mJogos Disponíveis:\033[0m")
            lista_jogos = list(jogos_disponiveis.keys())
            for idx, nome in enumerate(lista_jogos, 1):
                print(f"  {idx}. {nome.capitalize()}")
            
            escolha = input("\nEscolha o número ou nome do jogo (ou 'sair'): ").strip().lower()
            if escolha in ["sair", "cancelar", ""]:
                return
            
            if escolha.isdigit() and 1 <= int(escolha) <= len(lista_jogos):
                script_alvo = jogos_disponiveis[lista_jogos[int(escolha) - 1]]
            else:
                for chave, caminho in jogos_disponiveis.items():
                    if escolha in chave:
                        script_alvo = caminho
                        break

        if script_alvo:
            print(f"\n [CacauIA] Iniciando '{script_alvo.parent.name}'...\n")
            spec = importlib.util.spec_from_file_location("modulo_jogo", script_alvo)
            modulo_jogo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo_jogo)

            if hasattr(modulo_jogo, "main"):
                modulo_jogo.main()
            elif hasattr(modulo_jogo, "iniciar"):
                modulo_jogo.iniciar()
        else:
            print("❌ Jogo não encontrado.")

    def saudar(self, nome: str = "Dev"):
        self.exibir_banner()
        print(f"Olá, {nome}! \nEu sou a CacauIA, sua assistente no Linux.\n")

    def despedir(self):
        print("\nDesligando módulos. Até logo! \n")

    def mostrar_relogio(self):
        agora = datetime.now()
        print(f"\n [CacauIA] Data: {agora.strftime('%d/%m/%Y')} | Hora: {agora.strftime('%H:%M:%S')}\n")

    def abrir_aplicativo(self, nome_app: str):
        app = nome_app.lower().strip()
        try:
            subprocess.Popen([app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f" {app.capitalize()} iniciado!")
        except FileNotFoundError:
            print(f" Aplicativo '{app}' não encontrado no sistema.")

    def pesquisar_e_salvar(self, termo: str):
        print(f" [CacauIA] Pesquisando sobre '{termo}'...")
        try:
            with DDGS() as ddgs:
                resultados = list(ddgs.text(termo, max_results=5))
        except Exception as e:
            print(f" Erro na busca: {e}\n")
            return

        if not resultados:
            print(" Nenhum resultado encontrado.\n")
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

        # Printa o resultado direto no terminal para você não ter que dar 'cacau ver'
        print(f"\n Resultado encontrado e salvo em: {caminho_completo}\n")
        print("="*40)
        print(conteudo_final)
        print("="*40 + "\n")

        
    def abrir_arquivo(self, nome_entrada: str):
        nome_limpo = nome_entrada.lower().strip().replace(" ", "_")
        if not nome_limpo.endswith(".txt"):
            nome_limpo += ".txt"

        caminho = os.path.join(self.pasta_output, nome_limpo)
        if os.path.exists(caminho):
            print(f"\n Lendo: {caminho}\n" + "="*40)
            with open(caminho, "r", encoding="utf-8") as f:
                print(f.read())
            print("="*40)
        else:
            print(f" Arquivo '{nome_limpo}' não foi encontrado em output.")

    def excluir_pesquisa(self, termo: str):
        if not os.path.exists(self.pasta_output):
            print(" Nenhuma pesquisa para excluir.")
            return

        termo_limpo = termo.lower().strip()
        if termo_limpo in ["todas", "tudo", "*"]:
            for arq in glob.glob(os.path.join(self.pasta_output, "*.txt")):
                os.remove(arq)
            print(" Todas as pesquisas foram excluídas!")
            return

        nome_arquivo = termo_limpo.replace(" ", "_")
        if not nome_arquivo.endswith(".txt"):
            nome_arquivo += ".txt"

        caminho = os.path.join(self.pasta_output, nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)
            print(f" Arquivo '{nome_arquivo}' removido!")
        else:
            print(f"❌ Arquivo '{nome_arquivo}' não encontrado.")