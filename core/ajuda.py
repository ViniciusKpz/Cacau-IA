import os
import sys
import difflib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ASCII.banner import exibir_banner_manual

class AjudaCacauIA:
    def __init__(self):
        self.comandos_map = {
            "status": ["!papai chegou", "!papai_chegou", "status", "operador"],
            "chat": ["chat", "conversar", "ia", "modo_chat"],
            "oi": ["oi", "ola", "saudar"],
            "buscar": ["busca", "buscar", "pesquisa", "pesquisar", "search"],
            "ver": ["abrir", "ler", "ver", "read", "open"],
            "excluir": ["excluir", "deletar", "apagar", "rm", "delete"],
            "relogio": ["relogio", "hora", "horas", "tempo", "date", "time"],
            "app": ["app", "abrir_app", "executar", "run"],
            "ajuda": ["ajuda", "comandos", "help", "manual", "-h", "--help"],
            "sair": ["sair", "exit", "quit", "tchau"]
        }

        self.comandos_info = {
            "status": "Verifica se tudo está em funcionamento.",
            "chat": "Inicia o modo de conversa contínua em linguagem natural.",
            "oi": "Exibe mensagem de saudação.",
            "buscar": "Busca na web e salva em output/<termo>.txt",
            "ver": "Lê um arquivo de pesquisa gravado.",
            "excluir": "Exclui uma pesquisa ou 'todas'.",
            "relogio": "Exibe data e hora atuais.",
            "app": "Abre um aplicativo do sistema em segundo plano.",
            "ajuda": "Exibe o manual de uso.",
            "sair": "Fecha a Cacau IA. "
        }

    def exibir_ajuda(self):
        exibir_banner_manual()
        print("\n=======================================================")
        print(" CACAU IA - Manual de Comandos CLI")
        print("=======================================================\n")
        for cmd, desc in self.comandos_info.items():
            print(f"📌 {cmd:<10} -> {desc}")
        print("\n=======================================================\n")

    def sugerir_comando(self, comando_errado: str) -> bool:
        todas_variacoes = [cmd for lista in self.comandos_map.values() for cmd in lista]
        correspondencias = difflib.get_close_matches(comando_errado, todas_variacoes, n=1, cutoff=0.5)

        if correspondencias:
            sugestao = correspondencias[0]
            print(f" Acho que você quis dizer '{sugestao}'?")
            print(f" Exemplo: cacau {sugestao}")
            return True
        return False