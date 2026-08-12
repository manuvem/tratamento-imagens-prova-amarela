import os
from PIL import Image

# Permite carregar imagens gigantescas sem travar
Image.MAX_IMAGE_PIXELS = None


def cor_similar(pixel, cor_alvo, tolerancia=20):
    """Verifica se a cor RGB de um pixel está dentro da tolerância."""
    if isinstance(pixel, int):
        return False
    
    r, g, b = pixel[:3]
    return (
        abs(r - cor_alvo[0]) <= tolerancia
        and abs(g - cor_alvo[1]) <= tolerancia
        and abs(b - cor_alvo[2]) <= tolerancia
    )


def validar_faixa(
    pixels, x, y_inicio, altura_imagem, altura_min, altura_max, cor_alvo, tolerancia=20
):
    """Avança verticalmente no pixel (x, y) verificando a extensão da cor."""
    y = y_inicio
    altura_encontrada = 0

    while y < altura_imagem:
        if cor_similar(pixels[x, y], cor_alvo, tolerancia):
            altura_encontrada += 1
            y += 1
            if altura_encontrada > altura_max:
                return 0
        else:
            break

    if altura_encontrada >= altura_min:
        return altura_encontrada
    return 0


def encontrar_padroes_corte(imagem, tolerancia=20):
    """
    Varre as últimas colunas da direita buscando o padrão visual de 4 faixas amarelas.
    Retorna a lista com as alturas (y) de corte.
    """
    largura, altura = imagem.size
    pixels = imagem.load()

    # Cores alvo RGB (Amarelo Forte e Amarelo Claro)
    cor_amarelo_forte = (255, 245, 64)
    cor_amarelo_claro = (255, 251, 179)

    posicoes_corte = []
    
    # Testa as últimas 10 colunas da direita para evitar falsos negativos por bordas
    colunas_teste = [largura - 1 - i for i in range(10) if (largura - 1 - i) >= 0]

    y = 0
    while y < altura:
        padrao_encontrado_neste_y = False

        for coluna_x in colunas_teste:
            # 1ª Faixa: Amarelo Forte (9 a 13px)
            h1 = validar_faixa(pixels, coluna_x, y, altura, 9, 13, cor_amarelo_forte, tolerancia)
            if h1 > 0:
                # 2ª Faixa: Amarelo Claro (5 a 9px)
                h2 = validar_faixa(pixels, coluna_x, y + h1, altura, 5, 9, cor_amarelo_claro, tolerancia)
                if h2 > 0:
                    # 3ª Faixa: Amarelo Forte (1 a 5px)
                    h3 = validar_faixa(pixels, coluna_x, y + h1 + h2, altura, 1, 5, cor_amarelo_forte, tolerancia)
                    if h3 > 0:
                        # 4ª Faixa: Amarelo Claro (7 a 11px)
                        h4 = validar_faixa(pixels, coluna_x, y + h1 + h2 + h3, altura, 7, 11, cor_amarelo_claro, tolerancia)
                        if h4 > 0:
                            # Padrão confirmado! 
                            # Corta 10px acima do início do padrão para dar folga ao texto
                            posicao_corte = max(0, y - 10)
                            posicoes_corte.append(posicao_corte)
                            
                            print(f"Padrão detectado na linha y={y} (coluna {coluna_x}). Ponto de corte definido em y={posicao_corte}")

                            # Salta toda a extensão do padrão para continuar a busca abaixo
                            y += h1 + h2 + h3 + h4
                            padrao_encontrado_neste_y = True
                            break # Sai do loop de colunas e avança no eixo Y
        
        if not padrao_encontrado_neste_y:
            y += 1

    return posicoes_corte


def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    if not os.path.exists(caminho_imagem):
        print(f"Erro: O arquivo '{caminho_imagem}' não foi encontrado!")
        return

    # Força a conversão para RGB pura
    imagem = Image.open(caminho_imagem).convert("RGB")
    largura, altura = imagem.size

    print(f"--- Processando imagem: {largura}x{altura} pixels ---")

    # Localiza todas as alturas de corte
    posicoes_corte = encontrar_padroes_corte(imagem)

    if not posicoes_corte:
        print("Nenhum padrão de faixa amarela foi encontrado para realizar os cortes.")
        return

    os.makedirs(pasta_saida, exist_ok=True)

    posicao_anterior = 0
    contador = 1
import os
from PIL import Image

# Permite carregar imagens gigantescas sem travar
Image.MAX_IMAGE_PIXELS = None


def cor_similar(pixel, cor_alvo, tolerancia=20):
    """Verifica se a cor RGB de um pixel está dentro da tolerância."""
    if isinstance(pixel, int):
        return False
    
    r, g, b = pixel[:3]
    return (
        abs(r - cor_alvo[0]) <= tolerancia
        and abs(g - cor_alvo[1]) <= tolerancia
        and abs(b - cor_alvo[2]) <= tolerancia
    )


def validar_faixa(
    pixels, x, y_inicio, altura_imagem, altura_min, altura_max, cor_alvo, tolerancia=20
):
    """Avança verticalmente no pixel (x, y) verificando a extensão da cor."""
    y = y_inicio
    altura_encontrada = 0

    while y < altura_imagem:
        if cor_similar(pixels[x, y], cor_alvo, tolerancia):
            altura_encontrada += 1
            y += 1
            if altura_encontrada > altura_max:
                return 0
        else:
            break

    if altura_encontrada >= altura_min:
        return altura_encontrada
    return 0


def encontrar_padroes_corte(imagem, tolerancia=20):
    """
    Varre as últimas colunas da direita buscando o padrão visual de 4 faixas amarelas.
    Retorna a lista com as alturas (y) de corte.
    """
    largura, altura = imagem.size
    pixels = imagem.load()

    # Cores alvo RGB (Amarelo Forte e Amarelo Claro)
    cor_amarelo_forte = (255, 245, 64)
    cor_amarelo_claro = (255, 251, 179)

    posicoes_corte = []
    
    # Testa as últimas 10 colunas da direita para evitar falsos negativos por bordas
    colunas_teste = [largura - 1 - i for i in range(10) if (largura - 1 - i) >= 0]

    y = 0
    while y < altura:
        padrao_encontrado_neste_y = False

        for coluna_x in colunas_teste:
            # 1ª Faixa: Amarelo Forte (9 a 13px)
            h1 = validar_faixa(pixels, coluna_x, y, altura, 9, 13, cor_amarelo_forte, tolerancia)
            if h1 > 0:
                # 2ª Faixa: Amarelo Claro (5 a 9px)
                h2 = validar_faixa(pixels, coluna_x, y + h1, altura, 5, 9, cor_amarelo_claro, tolerancia)
                if h2 > 0:
                    # 3ª Faixa: Amarelo Forte (1 a 5px)
                    h3 = validar_faixa(pixels, coluna_x, y + h1 + h2, altura, 1, 5, cor_amarelo_forte, tolerancia)
                    if h3 > 0:
                        # 4ª Faixa: Amarelo Claro (7 a 11px)
                        h4 = validar_faixa(pixels, coluna_x, y + h1 + h2 + h3, altura, 7, 11, cor_amarelo_claro, tolerancia)
                        if h4 > 0:
                            # Padrão confirmado! 
                            # Corta 10px acima do início do padrão para dar folga ao texto
                            posicao_corte = max(0, y - 10)
                            posicoes_corte.append(posicao_corte)
                            
                            print(f"Padrão detectado na linha y={y} (coluna {coluna_x}). Ponto de corte definido em y={posicao_corte}")

                            # Salta toda a extensão do padrão para continuar a busca abaixo
                            y += h1 + h2 + h3 + h4
                            padrao_encontrado_neste_y = True
                            break # Sai do loop de colunas e avança no eixo Y
        
        if not padrao_encontrado_neste_y:
            y += 1

    return posicoes_corte


def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    if not os.path.exists(caminho_imagem):
        print(f"Erro: O arquivo '{caminho_imagem}' não foi encontrado!")
        return

    # Força a conversão para RGB pura
    imagem = Image.open(caminho_imagem).convert("RGB")
    largura, altura = imagem.size

    print(f"--- Processando imagem: {largura}x{altura} pixels ---")

    # Localiza todas as alturas de corte
    posicoes_corte = encontrar_padroes_corte(imagem)

    if not posicoes_corte:
        print("Nenhum padrão de faixa amarela foi encontrado para realizar os cortes.")
        return

    os.makedirs(pasta_saida, exist_ok=True)

    posicao_anterior = 0
    contador = 1

    # Realiza os cortes horizontais de ponta a ponta na largura
    for posicao_corte in posicoes_corte:
        if posicao_corte <= posicao_anterior:
            continue

        # Caixa do corte: (esquerda, topo, direita, base)
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)

        nome_arquivo = f"parte_{contador:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"-> Salvo: {nome_arquivo} [{secao.width}x{secao.height}px]")

        posicao_anterior = posicao_corte
        contador += 1

    # Salva o último pedaço restante (da última faixa até o final da imagem)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)

        nome_arquivo = f"parte_{contador:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"-> Salvo bloco final: {nome_arquivo} [{secao.width}x{secao.height}px]")


if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"
    pasta_saida = "saida_questoes"

    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    print("\nProcesso de divisão concluído com sucesso!")
    # Realiza os cortes horizontais de ponta a ponta na largura
    for posicao_corte in posicoes_corte:
        if posicao_corte <= posicao_anterior:
            continue

        # Caixa do corte: (esquerda, topo, direita, base)
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)

        nome_arquivo = f"parte_{contador:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"-> Salvo: {nome_arquivo} [{secao.width}x{secao.height}px]")

        posicao_anterior = posicao_corte
        contador += 1

    # Salva o último pedaço restante (da última faixa até o final da imagem)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)

        nome_arquivo = f"parte_{contador:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"-> Salvo bloco final: {nome_arquivo} [{secao.width}x{secao.height}px]")


if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"
    pasta_saida = "saida_questoes"

    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    print("\nProcesso de divisão concluído com sucesso!")