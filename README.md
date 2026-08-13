# CacauIA — Assistente Virtual CLI para Linux

A CacauIA e uma assistente de linha de comando (CLI) modular para Linux. Ela permite realizar pesquisas rapidas na web, resumir conteudos utilizando modelos locais via Ollama, analisar arquivos e diretorios locais, controlar atalhos de aplicativos e verificar informacoes do sistema.

---

## Requisitos Previos

Antes de instalar, certifique-se de ter os seguintes pacotes instalados no seu sistema:

- Python 3.10+
- Git
- Ollama (para resumos inteligentes e interpretacao em linguagem natural com IA local)

---

## Passo a Passo de Instalacao

### 1. Clonar o repositorio
```bash
git clone https://github.com/ViniciusKpz/Cacau-IA.git
cd Cacau-IA
```

### 2. Criar e ativar o ambiente virtual (venv)
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar o Ollama para resumos e chat inteligente
Para que a CacauIA utilize o modelo local de IA, certifique-se de ter o Ollama rodando com o modelo llama3.2:

```bash
ollama run llama3.2
```

---

## Criando o Comando Global cacau

Para conseguir executar a CacauIA de qualquer diretorio no terminal digitando apenas cacau, crie o atalho global no sistema:

```bash
cat << 'EOF' | sudo tee /usr/local/bin/cacau > /dev/null
#!/bin/bash
PROJETO_DIR="$HOME/.CacauIA"
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

Exemplos de comandos disponiveis na CLI:

| Comando | Descricao | Exemplo de Uso |
| :--- | :--- | :--- |
| chat | Inicia o modo de chat interativo com linguagem natural | cacau chat |
| oi | Exibe a mensagem de saudacao | cacau oi |
| relogio | Exibe a data e hora atuais | cacau relogio |
| buscar | Pesquisa na web e gera um resumo em output/ | cacau buscar "arch linux" |
| ver | Le um relatorio de pesquisa gravado na pasta output/ | cacau ver "arch_linux" |
| excluir | Exclui uma pesquisa ou todas (cacau excluir todas) | cacau excluir "arch_linux" |
| app | Abre um aplicativo instalado no sistema em segundo plano | cacau app firefox |
| ajuda | Exibe o manual de comandos | cacau ajuda |

---

## Recursos do Modo Chat Interativo (cacau chat)

No modo Chat, voce conversa em linguagem natural e a IA identifica e executa acoes do sistema automaticamente:

- Analise de Arquivos e Pastas:
  - "oq tem em ~/Jogos"
  - "analisa a pasta ~/.CacauIA"
  - "oq tem no arquivo README.md"
- Pesquisas Web:
  - "pesquise sobre o kernel linux"
- Controle de Apps e Sistema:
  - "abre o spotify"
  - "que horas sao?"

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
├── .funcoes/
│   └── navegar/
│       ├── __init__.py
│       └── analise.py
├── output/
├── main.py
└── requirements.txt
```

---

## Licenca

Projeto desenvolvido para uso pessoal e aprendizado. Livre para modificacoes e melhorias!