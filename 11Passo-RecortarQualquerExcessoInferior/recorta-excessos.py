from PIL import Image
import os
import shutil

def encontrar_faixa_inferior(imagem, cor_alvo, tolerancia=20):
    """
    Encontra a faixa descrita de baixo para cima
    Retorna a posição Y onde deve ser feito o corte (ACIMA/ANTES da faixa amarela) ou None se não encontrar
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Percorre a imagem de baixo para cima
    for y in range(altura - 1, 15, -1):  # Começa do fundo, precisa de pelo menos 12 pixels
        faixa_encontrada = True
        
        # Verifica os 4 pixels amarelos inferiores (y-11 até y-8)
        for dy in range(4):
            pixel_y = y - 11 + dy
            if pixel_y < 0:
                faixa_encontrada = False
                break
                
            pixel = pixels[largura // 2, pixel_y]
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é amarelo (dentro da tolerância)
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if not faixa_encontrada:
            continue
            
        # Verifica os 4 pixels brancos do meio (y-7 até y-4)
        for dy in range(4):
            pixel_y = y - 7 + dy
            pixel = pixels[largura // 2, pixel_y]
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é branco (dentro da tolerância)
            if (abs(r - 255) > tolerancia or 
                abs(g - 255) > tolerancia or 
                abs(b - 255) > tolerancia):
                faixa_encontrada = False
                break
        
        if not faixa_encontrada:
            continue
            
        # Verifica os 4 pixels amarelos superiores (y-3 até y)
        for dy in range(4):
            pixel_y = y - 3 + dy
            pixel = pixels[largura // 2, pixel_y]
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é amarelo (dentro da tolerância)
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            # Posição calculada para cortar logo acima da faixa inteira (removendo a faixa amarela)
            posicao_corte = y - 11
            print(f"Faixa encontrada! Cortando na posição y={posicao_corte} (removendo a faixa amarela)")
            return posicao_corte
    
    return None

def processar_imagens(pasta_origem, pasta_destino, cor_alvo):
    """
    Processa todas as imagens da pasta origem, recortando as que têm faixa amarela inferior
    e copiando todas para a pasta destino
    """
    # Cria a pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Lista todos os arquivos da pasta origem
    arquivos = [f for f in os.listdir(pasta_origem) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    print(f"Encontrados {len(arquivos)} arquivos para processar")
    
    for arquivo in arquivos:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        
        try:
            # Abre a imagem
            with Image.open(caminho_origem) as imagem:
                print(f"\nProcessando: {arquivo} ({imagem.width}x{imagem.height})")
                
                # Procura pela faixa inferior
                posicao_corte = encontrar_faixa_inferior(imagem, cor_alvo)
                
                if posicao_corte is not None and posicao_corte > 0:
                    # Se encontrou a faixa, recorta a imagem acima dela
                    area_corte = (0, 0, imagem.width, posicao_corte)
                    imagem_recortada = imagem.crop(area_corte)
                    imagem_recortada.save(caminho_destino)
                    print(f"✓ Imagem recortada: {imagem_recortada.width}x{imagem_recortada.height}")
                else:
                    # Se não encontrou faixa, copia a imagem original
                    shutil.copy2(caminho_origem, caminho_destino)
                    print(f"✓ Imagem mantida original (sem faixa detectada)")
                    
        except Exception as e:
            print(f"✗ Erro ao processar {arquivo}: {e}")
            try:
                shutil.copy2(caminho_origem, caminho_destino)
                print(f"✓ Arquivo copiado mesmo com erro")
            except:
                print(f"✗ Não foi possível copiar o arquivo")

# Função principal
if __name__ == "__main__":
    # Configurações
    pasta_origem = "./questoes"
    pasta_destino = "finalizadas"
    cor_alvo = (100, 96, 25)  # RGB amarelo definido
    
    print("Iniciando processamento de imagens...")
    print(f"Pasta origem: {pasta_origem}")
    print(f"Pasta destino: {pasta_destino}")
    print(f"Cor alvo: RGB{cor_alvo}")
    
    # Verifica se a pasta origem existe
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta '{pasta_origem}' não existe!")
        exit(1)
    
    # Executa o processamento
    processar_imagens(pasta_origem, pasta_destino, cor_alvo)
    
    print("\n" + "="*50)
    print("Processamento concluído!")
    print(f"Todas as imagens foram salvas em: {pasta_destino}")