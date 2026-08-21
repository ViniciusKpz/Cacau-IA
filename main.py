import sys
import queue
import threading
import time
import os
import io
import contextlib
import warnings
import re

# Silencia avisos do Pygame e Runtime
warnings.filterwarnings("ignore", category=RuntimeWarning)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from core.cacau import CacauIA
from interface.app import CacauApp

# Filas de comunicação bidirecional
fila_gui = queue.Queue()       # Terminal/Engine -> GUI
fila_comandos = queue.Queue()  # GUI -> Terminal/Engine

def enviar_para_gui(tipo, conteudo):
    """Envia mensagens formatadas para a interface visual."""
    fila_gui.put({"tipo": tipo, "conteudo": conteudo})

def processar_comando_gui(bot, texto):
    """Executa o comando digitado na GUI e retorna a resposta capturando stdout ou return."""
    texto_limpo = texto.strip()
    if not texto_limpo:
        return

    partes = texto_limpo.split()
    comando_completo = texto_limpo
    comando = partes[0].lower()
    argumentos = partes[1:]

    if comando == "cacau" and argumentos:
        comando = argumentos[0].lower()
        argumentos = argumentos[1:]
        comando_completo = " ".join([comando] + argumentos)

    output_buffer = io.StringIO()
    resultado_retornado = None

    with contextlib.redirect_stdout(output_buffer):
        comandos_operador = ["!papai chegou", "papai chegou", "!papai_chegou", "papai_chegou", "status", "operador"]

        if comando_completo.lower() in comandos_operador:
            resultado_retornado = bot.exibir_status()

        elif comando in bot.ajuda.comandos_map.get("ajuda", ["ajuda", "help"]):
            resultado_retornado = bot.ajuda.exibir_ajuda()

        elif comando in bot.ajuda.comandos_map.get("oi", ["oi", "ola"]):
            nome = " ".join(argumentos) if argumentos else "Dev"
            resultado_retornado = bot.saudar(nome)

        elif comando in bot.ajuda.comandos_map.get("relogio", ["relogio", "horas"]):
            resultado_retornado = bot.mostrar_relogio()

        elif comando in bot.ajuda.comandos_map.get("buscar", ["buscar", "pesquisar"]):
            if argumentos:
                resultado_retornado = bot.pesquisar_e_salvar(" ".join(argumentos))

        elif comando in bot.ajuda.comandos_map.get("app", ["app", "abrir"]):
            if argumentos:
                resultado_retornado = bot.abrir_aplicativo(" ".join(argumentos))

        else:
            if hasattr(bot, "responder_chat"):
                resultado_retornado = bot.responder_chat(comando_completo)
            elif hasattr(bot, "chat"):
                resultado_retornado = bot.chat(comando_completo)
            else:
                resultado_retornado = bot.saudar(comando_completo)

    resposta_print = output_buffer.getvalue().strip()
    
    resposta_final = ""
    if resposta_print:
        resposta_final = resposta_print
    elif resultado_retornado and isinstance(resultado_retornado, str):
        resposta_final = resultado_retornado.strip()

    if resposta_final:
        enviar_para_gui("resposta", resposta_final)
    else:
        enviar_para_gui("resposta", "[CACAU]: Comando processado.")

def escutar_comandos_gui(bot):
    """Thread em segundo plano que processa os comandos assim que chegam da GUI."""
    while True:
        try:
            texto_comando = fila_comandos.get()
            processar_comando_gui(bot, texto_comando)
            fila_comandos.task_done()
        except Exception as e:
            enviar_para_gui("resposta", f"[ERRO]: {str(e)}")

def main():
    bot = CacauIA()
    
    if len(sys.argv) < 2:
        # Inicia a escuta da GUI em segundo plano
        threading.Thread(target=escutar_comandos_gui, args=(bot,), daemon=True).start()

        enviar_para_gui("resposta", "Conexão estabelecida com a engine principal!")
        
        # Executa o status uma única vez na inicialização da GUI
        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            bot.exibir_status()
        
        status_inicial = output_buffer.getvalue().strip()
        if status_inicial:
            enviar_para_gui("metricas", status_inicial)

        app = CacauApp(fila_comunicacao=fila_gui, fila_comandos=fila_comandos)
        app.run()
        return

    # Processamento de comandos CLI via argumentos do terminal
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

def limpar_ansi(texto):
    """Remove caracteres de controle de cor do terminal (ANSI escape codes)."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', texto)

    resposta_final = limpar_ansi(resposta_final)

    if resposta_final:
        enviar_para_gui("resposta", resposta_final)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Aplicação encerrada pelo usuário.")