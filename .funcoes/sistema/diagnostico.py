import sys
import py_compile
import requests
import json
import subprocess
from pathlib import Path
import urllib.request

def testar_sintaxe(raiz_projeto):
    """Varre todos os arquivos .py checando se há erros de sintaxe de compilação."""
    erros = []
    for arquivo in raiz_projeto.rglob("*.py"):
        if ".venv" in arquivo.parts or "__pycache__" in arquivo.parts:
            continue
        try:
            py_compile.compile(str(arquivo), doraise=True)
        except py_compile.PyCompileError as e:
            erros.append(f"Sintaxe em {arquivo.name}: {e.msg}")
    return erros

def testar_modulos_e_atributos(raiz_projeto):
    """Executa a classe de ajuda em background para pegar NameErrors em runtime."""
    erros = []
    try:
        comando_teste = "import sys; sys.path.insert(0, '.'); from core.ajuda import AjudaCacauIA; AjudaCacauIA().exibir_ajuda()"
        res = subprocess.run(
            [sys.executable, "-c", comando_teste],
            cwd=raiz_projeto,
            capture_output=True,
            text=True,
            timeout=4
        )
        if res.returncode != 0 or "NameError" in res.stderr or "Traceback" in res.stderr:
            linhas_erro = [l.strip() for l in res.stderr.splitlines() if l.strip()]
            msg_erro = linhas_erro[-1] if linhas_erro else "Falha no menu de ajuda"
            erros.append(f"Erro em ajuda.py/banner.py: {msg_erro}")
    except Exception:
        pass
    return erros

def testar_ollama():
    """Valida o Ollama sem dependência de libs externas."""
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=3) as res:
            if res.status == 200:
                return True, "IA OK"
    except Exception:
        pass
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        resultado = sock.connect_ex(('127.0.0.1', 11434))
        sock.close()
        if resultado == 0:
            return True, "IA OK (Porta 11434)"
    except Exception:
        pass

    return False, "Ollama Indisponivel"

def testar_estrutura(raiz_projeto):
    faltantes = []
    estruturas = [
        raiz_projeto / "core" / "cacau.py",
        raiz_projeto / "core" / "ajuda.py",
        raiz_projeto / "ASCII" / "banner.py",
        raiz_projeto / "main.py"
    ]
    for item in estruturas:
        if not item.exists():
            faltantes.append(item.name)
    return faltantes

def executar_varredura_completa():
    try:
        raiz = Path(__file__).resolve().parent.parent.parent
        cache_dir = raiz / ".funcoes" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        arquivo_cache = cache_dir / "health.json"

        erros_sintaxe = testar_sintaxe(raiz)
        erros_atributos = testar_modulos_e_atributos(raiz)
        ollama_ok, msg_ollama = testar_ollama()
        itens_faltantes = testar_estrutura(raiz)

        todos_erros_codigo = erros_sintaxe + erros_atributos
        sintaxe_ok = len(todos_erros_codigo) == 0
        estrutura_ok = len(itens_faltantes) == 0

        status_geral = "OK" if (sintaxe_ok and ollama_ok and estrutura_ok) else "ALERTA"

        resultado = {
            "status_geral": status_geral,
            "detalhes": {
                "sintaxe": {"ok": sintaxe_ok, "erros": todos_erros_codigo},
                "ollama": {"ok": ollama_ok, "mensagem": msg_ollama},
                "estrutura": {"ok": estrutura_ok, "faltantes": itens_faltantes}
            }
        }

        with open(arquivo_cache, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)

    except Exception as e:
        # Se a própria thread falhar feio, grava o erro no cache em vez de só dar pass
        try:
            with open(arquivo_cache, "w", encoding="utf-8") as f:
                json.dump({
                    "status_geral": "ALERTA",
                    "detalhes": {
                        "sintaxe": {"ok": False, "erros": [f"Erro no scanner: {str(e)}"]},
                        "ollama": {"ok": False, "mensagem": "Scanner falhou"},
                        "estrutura": {"ok": True, "faltantes": []}
                    }
                }, f, indent=2)
        except Exception:
            pass