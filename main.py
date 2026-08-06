import sys
from core.cacau import CacauIA

def main():
    bot = CacauIA()

    if len(sys.argv) < 2:
        bot.ajuda.exibir_ajuda()
        return

    comando = sys.argv[1].lower()
    argumentos = sys.argv[2:]

    if comando in bot.ajuda.comandos_map["ajuda"]:
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
            print("⚠️ Uso: python main.py app <nome_do_app>")

    elif comando in bot.ajuda.comandos_map["buscar"]:
        if argumentos:
            bot.pesquisar_e_salvar(" ".join(argumentos))
        else:
            print("⚠️ Uso: python main.py buscar <termo>")

    elif comando in bot.ajuda.comandos_map["ver"]:
        if argumentos:
            bot.abrir_arquivo(" ".join(argumentos))
        else:
            print("⚠️ Uso: python main.py ver <nome_do_arquivo>")

    elif comando in bot.ajuda.comandos_map["excluir"]:
        if argumentos:
            bot.excluir_pesquisa(" ".join(argumentos))
        else:
            print("⚠️ Uso: python main.py excluir <termo_ou_todas>")
    
    elif comando in bot.ajuda.comandos_map.get("chat", ["chat"]):
        bot.iniciar_chat()

    else:
        if not bot.ajuda.sugerir_comando(comando):
            bot.saudar(" ".join(sys.argv[1:]))

if __name__ == "__main__":
    main()