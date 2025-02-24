import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from functions import imagem_para_ascii
import cv2
import os
import numpy as np
from colorama import init, Fore
import time

# Inicializa o colorama
init(autoreset=True)

def converter_imagem(caminho, nova_largura):
    # Cria uma pasta com o nome do arquivo processado
    nome_arquivo = os.path.splitext(os.path.basename(caminho))[0]  # Obtém o nome do arquivo sem extensão
    pasta_saida = os.path.join(os.getcwd(), nome_arquivo)  # Cria o caminho da nova pasta
    os.makedirs(pasta_saida, exist_ok=True)  # Cria a pasta se não existir

    if caminho.lower().endswith(('.mp4', '.avi', '.mov')):  # Verifica se é um vídeo
        processar_video(caminho, nova_largura, pasta_saida)
    else:  # Caso contrário, trata como uma imagem
        texto_ascii = imagem_para_ascii(caminho, nova_largura)
        with open(os.path.join(pasta_saida, "imagem_em_texto.txt"), "w") as f:
            f.write(texto_ascii)
        print(f"Conversão concluída! O texto ASCII foi salvo em '{pasta_saida}/imagem_em_texto.txt'.")

def processar_video(caminho_video, nova_largura, pasta_saida):
    cap = cv2.VideoCapture(caminho_video)
    fps = 60  # Quadros por segundo para a captura

    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    frame_count = 0

    # Primeiro, gera os arquivos de texto ASCII
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Sai do loop se não houver mais quadros

        # Redimensiona o quadro
        frame = cv2.resize(frame, (nova_largura, int(frame.shape[0] * nova_largura / frame.shape[1])))

        # Converte o quadro para ASCII
        texto_ascii = imagem_para_ascii(frame, nova_largura)

        # Salva o texto ASCII em um arquivo na pasta de saída
        with open(os.path.join(pasta_saida, f"quadro_{frame_count}.txt"), "w") as f:
            f.write(texto_ascii)

        print(f"Quadro {frame_count} processado e salvo como '{pasta_saida}/quadro_{frame_count}.txt'.")
        frame_count += 1

    cap.release()
    print("Processamento do vídeo concluído.")

    # Agora, lê e exibe os arquivos de texto armazenados na pasta
    fps_display = 120  # Duplicado para 120 quadros por segundo para a exibição
    frame_interval_display = 1 / fps_display  # Intervalo entre quadros em segundos para exibição

    for i in range(frame_count):
        with open(os.path.join(pasta_saida, f"quadro_{i}.txt"), "r") as f:
            texto_ascii = f.read()

        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o console
        print(Fore.WHITE + texto_ascii)  # Exibe o quadro em branco

        # Exibe o quadro duas vezes
        time.sleep(frame_interval_display / 2)  # Espera pela metade do intervalo antes de exibir o próximo quadro
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o console novamente
        print(Fore.WHITE + texto_ascii)  # Exibe o quadro em branco novamente

        # Espera pelo intervalo de tempo antes de exibir o próximo quadro
        time.sleep(frame_interval_display / 2)  # Espera pela outra metade do intervalo

def drop(event):
    global largura_combobox  # Torna largura_combobox acessível na função drop
    caminho = event.data
    largura_selecionada = largura_combobox.get()  # Obtém a largura selecionada na combobox

    if largura_selecionada:  # Verifica se um valor foi selecionado
        try:
            nova_largura = int(largura_selecionada)  # Tenta converter para inteiro
            converter_imagem(caminho, nova_largura)  # Passa a nova largura para a função
        except ValueError:
            print("Erro: A largura selecionada não é um número válido.")
    else:
        print("Erro: Nenhuma largura foi selecionada.")

def iniciar_interface():
    global largura_combobox  # Torna largura_combobox acessível na função drop
    root = TkinterDnD.Tk()
    root.title("Conversor de Imagem para ASCII")
    root.geometry("400x200")

    label = tk.Label(root, text="Arraste e solte uma imagem aqui", padx=10, pady=10)
    label.pack(expand=True, fill=tk.BOTH)

    # Adiciona um rótulo para a largura da imagem
    largura_label = tk.Label(root, text="Selecione a largura desejada:")
    largura_label.pack(pady=5)

    # Lista de resoluções predefinidas
    resolucoes = [128, 256, 512, 1024]

    # Cria uma combobox para selecionar a largura
    largura_combobox = ttk.Combobox(root, values=resolucoes)
    largura_combobox.set(resolucoes[0])  # Define o valor padrão
    largura_combobox.pack(pady=5)

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop)

    root.mainloop()