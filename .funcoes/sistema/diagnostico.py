import sys
import py_compile
import requests
import json
from pathlib import Path

def testar_sintaxe(raiz_projeto):
    """Varre todos os scripts .py em busca de erros de sintaxe."""
    erros = []
    pastas = [raiz_projeto / "core", raiz_projeto / ".funcoes"]
    
    for pasta in pastas:
        if not pasta.exists():
            continue
        for script in pasta.rglob("*.py"):
            try:
                py_compile.compile(script, doraise=True)
            except py_compile.PyCompileError as e:
                erros.append(f"Sintaxe em {script.name}: {e.msg}")
            except Exception as e:
                erros.append(f"Erro ao ler {script.name}: {str(e)}")
    return erros

def testar_ollama():
    """Testa se o Ollama está respondendo requisições HTTP locais."""
    try:
        res = requests.get("http://localhost:11434/api/tags", timeout=1.5)
        if res.status_code == 200:
            return True, "Ollama ativo (HTTP 200)"
        return False, f"Ollama respondeu status {res.status_code}"
    except Exception:
        return False, "Ollama fora do ar ou timeout"

def testar_estrutura(raiz_projeto):
    """Verifica se os diretórios e arquivos vitais estão no lugar."""
    faltantes = []
    estruturas = [
        raiz_projeto / "core" / "cacau.py",
        raiz_projeto / "main.py",
        raiz_projeto / ".funcoes" / "navegar" / "analise.py"
    ]
    for item in estruturas:
        if not item.exists():
            faltantes.append(item.name)
    return faltantes

def executar_varredura_completa():
    """Roda todos os testes em segundo plano e grava o cache em JSON."""
    raiz = Path(__file__).resolve().parent.parent.parent
    cache_dir = raiz / ".funcoes" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    arquivo_cache = cache_dir / "health.json"

    # 1. Testes
    erros_sintaxe = testar_sintaxe(raiz)
    ollama_ok, msg_ollama = testar_ollama()
    itens_faltantes = testar_estrutura(raiz)

    # 2. Compilação do Diagnóstico
    status_geral = "OK" if (not erros_sintaxe and ollama_ok and not itens_faltantes) else "ALERTA"

    resultado = {
        "status_geral": status_geral,
        "detalhes": {
            "sintaxe": {"ok": len(erros_sintaxe) == 0, "erros": erros_sintaxe},
            "ollama": {"ok": ollama_ok, "mensagem": msg_ollama},
            "estrutura": {"ok": len(itens_faltantes) == 0, "faltantes": itens_faltantes}
        }
    }

    # 3. Escrita em Cache
    try:
        with open(arquivo_cache, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
    except Exception:
        pass