import PIL.Image
# regular
#caracteres = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
# negrito
caracteres = [' ', '.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']

def escala_da_imagem(imagem, nova_largura):
    """Redimensiona a imagem, mantendo a proporção correta."""
    largura, altura = imagem.size
    relacao = altura / largura
    nova_altura = int(nova_largura * relacao * 0.5)  # Ajuste na proporção
    imagem_transformada = imagem.resize((nova_largura, nova_altura))
    return imagem_transformada

def dessaturar(imagem):
    """Converte a imagem para tons de cinza."""
    return imagem.convert('L')

def pixel_para_texto(imagem):
    """Converte os pixels da imagem em caracteres."""
    pixels_da_imagem = imagem.getdata()
    texto = "".join([caracteres[pixel // 25] for pixel in pixels_da_imagem]) # Ajuste na escala de cinza
    return texto

def imagem_para_ascii(caminho_da_imagem, nova_largura):
    """Converte uma imagem em arte ASCII."""
    try:
        imagem = PIL.Image.open(caminho_da_imagem)
    except FileNotFoundError:
        return "Imagem não encontrada."

    imagem_transformada = escala_da_imagem(imagem, nova_largura)
    imagem_dessaturada = dessaturar(imagem_transformada)
    texto_ascii = pixel_para_texto(imagem_dessaturada)

    # Formata o texto para exibir como uma grade
    largura, altura = imagem_transformada.size
    texto_ascii_formatado = "\n".join(texto_ascii[i:(i + largura)] for i in range(0, len(texto_ascii), largura))

    return texto_ascii_formatado