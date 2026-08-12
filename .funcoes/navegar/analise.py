import os

def analisar_caminho(caminho_relativo: str) -> str:
    """
    Expande o caminho (suporta '~') e verifica se é pasta ou arquivo,
    retornando um texto formatado com o conteúdo/estrutura.
    """
    caminho = os.path.expanduser(caminho_relativo.strip())

    if not os.path.exists(caminho):
        return f" O caminho '{caminho_relativo}' não existe no sistema."

    # Se for um DIRETÓRIO (pasta)
    if os.path.isdir(caminho):
        estrutura = []
        total_arquivos = 0
        total_pastas = 0

        for root, dirs, files in os.walk(caminho):
            # Limita a profundidade para não ler pastas gigantes como node_modules ou .git de forma recursiva infinita
            nivel = root.replace(caminho, '').count(os.sep)
            if nivel > 2:
                continue
            
            subpasta = os.path.basename(root)
            if subpasta.startswith('.') and root != caminho:
                continue  # Pula pastas ocultas profundas

            indent = '  ' * nivel
            estrutura.append(f"{indent} {os.path.basename(root)}/")
            
            for f in files:
                if not f.startswith('.'):
                    estrutura.append(f"{indent}   {f}")
                    total_arquivos += 1
            total_pastas += len(dirs)

        resumo_arvore = "\n".join(estrutura[:40]) # Limita linhas para economizar contexto
        return (
            f"=== ANÁLISE DO DIRETÓRIO: {caminho_relativo} ===\n"
            f"Total de arquivos encontrados: {total_arquivos}\n"
            f"Estrutura de pastas:\n{resumo_arvore}\n"
        )

    # Se for um ARQUIVO
    elif os.path.isfile(caminho):
        try:
            # Tenta ler como texto (código, txt, md, json, etc.)
            with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                linhas = f.readlines()
                conteudo = "".join(linhas[:150]) # Lê as primeiras 150 linhas
                
            return (
                f"=== CONTEÚDO DO ARQUIVO: {caminho_relativo} ===\n"
                f"Total de linhas: {len(linhas)}\n\n"
                f"{conteudo}\n"
            )
        except Exception as e:
            return f" Não foi possível ler o arquivo '{caminho_relativo}': {e}"

    return "⚠️ Tipo de arquivo não suportado."