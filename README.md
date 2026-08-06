# CacauIA — Assistente Virtual CLI para Linux

A **CacauIA** é uma assistente de linha de comando (CLI) modular para Linux. Ela permite realizar pesquisas rápidas na web, resumir conteúdos utilizando modelos locais via Ollama, controlar atalhos de aplicativos e verificar informações de sistema.

---

## Requisitos Prévios

Antes de instalar, certifique-se de ter os seguintes pacotes instalados no seu sistema:

- **Python 3.10+**
- **Git**
- **Ollama** (opcional, para resumos inteligentes com IA local)

---

## Passo a Passo de Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/ViniciusKpz/Cacau-IA.git
cd Cacau-IA
```

### 2. Criar e ativar o ambiente virtual (venv)
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. (Opcional) Configurar o Ollama para resumos inteligentes
Se quiser que a CacauIA resuma os resultados das pesquisas usando IA local, certifique-se de que o Ollama esteja rodando com o modelo `llama3.2`:

```bash
ollama run llama3.2
```

---

## Criando o Comando Global `cacau`

Para conseguir executar a CacauIA de qualquer diretório no terminal digitando apenas `cacau`, crie o atalho global no sistema:

```bash
cat << 'EOF' | sudo tee /usr/local/bin/cacau > /dev/null
#!/bin/bash
PROJETO_DIR="$(pwd)"
VENV_PYTHON="$PROJETO_DIR/venv/bin/python"

if [ -f "$VENV_PYTHON" ]; then
    $VENV_PYTHON "$PROJETO_DIR/main.py" "$@"
else
    python3 "$PROJETO_DIR/main.py" "$@"
fi
EOF

sudo chmod +x /usr/local/bin/cacau
```

---

## Como Usar

Exemplos de comandos disponíveis:

| Comando | Descrição | Exemplo de Uso |
| :--- | :--- | :--- |
| `oi` | Exibe a mensagem de saudação | `cacau oi` |
| `relogio` | Exibe a data e hora atuais | `cacau relogio` |
| `buscar` | Pesquisa na web e gera um resumo em `output/` | `cacau buscar "arch linux"` |
| `ver` | Lê uma pesquisa já gravada na pasta `output/` | `cacau ver "arch_linux"` |
| `excluir` | Exclui uma pesquisa ou todas (`cacau excluir todas`) | `cacau excluir "arch_linux"` |
| `app` | Abre um aplicativo instalado no sistema em segundo plano | `cacau app firefox` |
| `ajuda` | Exibe o manual de comandos | `cacau ajuda` |

---

## Estrutura do Projeto

```text

.CacauIA/
├── ASCII/
│   ├── __init__.py   
│   └── banner.py     
├── core/
│   ├── ajuda.py
│   ├── cacau.py
│   └── ia.py
├── main.py
...