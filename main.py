from functions import pixel_para_texto, dessaturar, escala_da_imagem
from functions import *
from interface import *

def main(nova_largura = int(input("qual a base da imagem? "))):
    path = input("Insira o caminho para a imagem ou arraste para cá. ")
    try:
        imagem = PIL.Image.open(path)
    except:
        print(path, "não é um endereço válido")

    nova_imagem = pixel_para_texto(dessaturar(escala_da_imagem(imagem, nova_largura)))

    contagem_pixel = len(nova_imagem)
    imagem_em_texto = "\n".join(nova_imagem[i:(i+nova_largura)] for i in range(0, contagem_pixel, nova_largura))

    print(imagem_em_texto)

    with open("imagem_em_texto.txt","w") as f:
        f.write(imagem_em_texto)

main()
