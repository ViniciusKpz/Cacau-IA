import sys
from core.cacau import CacauIA
from interface.app import CacauApp

def main():
    bot = CacauIA()
    
    if len(sys.argv) < 2:
        app = CacauApp(bot_instance=bot)
        app.run()
        return

    comando_completo = " ".join(sys.argv[1:]).lower().strip()
    comando = sys.argv[1].lower()
    argumentos = sys.argv[2:]

    comandos_operador = ["!papai chegou", "papai chegou", "!papai_chegou", "papai_chegou", "status", "operador"]

    if comando_completo in comandos_operador:
        bot.exibir_status()

    elif comando in bot.ajuda.comandos_map["ajuda"]:
        bot.ajuda.exibir_ajuda()

    elif comando in bot.ajuda.comandos_map["oi"]:
        nome = " ".join(argumentos) if argumentos else "Dev"
        bot.saudar(nome)

    elif comando in bot.ajuda.comandos_map["sair"]:
        bot.despedir()

    elif comando in bot.ajuda.comandos_map["relogio"]:
        bot.mostrar_relogio()

    elif comando in bot.ajuda.comandos_map["app"]:
        if argumentos:
            bot.abrir_aplicativo(" ".join(argumentos))
        else:
            print(" Uso: python main.py app <nome_do_app>")

    elif comando in bot.ajuda.comandos_map["buscar"]:
        if argumentos:
            bot.pesquisar_e_salvar(" ".join(argumentos))
        else:
            print(" Uso: python main.py buscar <termo>")

    elif comando in bot.ajuda.comandos_map["ver"]:
        if argumentos:
            bot.abrir_arquivo(" ".join(argumentos))
        else:
            print(" Uso: python main.py ver <nome_do_arquivo>")

    elif comando in bot.ajuda.comandos_map["excluir"]:
        if argumentos:
            bot.excluir_pesquisa(" ".join(argumentos))
        else:
            print(" Uso: python main.py excluir <termo_ou_todas>")

    elif comando in bot.ajuda.comandos_map.get("chat", ["chat"]):
        bot.iniciar_chat()

    elif comando in bot.ajuda.comandos_map.get("jogar", ["jogar"]):
        nome_jogo = " ".join(argumentos) if argumentos else None
        bot.jogar(nome_jogo)

    else:
        if not bot.ajuda.sugerir_comando(comando):
            bot.saudar(" ".join(sys.argv[1:]))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Aplicação encerrada pelo usuário.")