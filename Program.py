import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Toplevel
import cv2
import numpy as np
from PIL import Image, ImageTk
import math

class VisualizadorDeImagemInterativo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Paint 2.0")

        self.canvas = tk.Canvas(self.root, bg="#7f7f7f")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Cria o menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Cria o submenu "Arquivo"
        self.submenu_arquivo = tk.Menu(self.menu)
        self.menu.add_cascade(label="Arquivo", menu=self.submenu_arquivo)
        self.submenu_arquivo.add_command(label="Abrir Imagem", command=self.abrir_imagem)
        self.submenu_arquivo.add_command(label="Salvar Imagem", command=self.salvar_imagem)

        # Cria o submenu "Editar"
        self.submenu_editar = tk.Menu(self.menu)
        self.menu.add_cascade(label="Editar", menu=self.submenu_editar)
        self.submenu_editar.add_command(label="Criar Negativo", command=self.criar_negativo)
        self.submenu_editar.add_command(label="Inverter Horizontalmente", command=self.inverter_horizontalmente)
        self.submenu_editar.add_command(label="Inverter Verticalmente", command=self.inverter_verticalmente)
        self.submenu_editar.add_command(label="Rotacionar Esquerda", command=self.rotacionar_esquerda)
        self.submenu_editar.add_command(label="Rotacionar Direita", command=self.rotacionar_direita)
        self.submenu_editar.add_command(label="Definir Escala", command=self.definir_escala)
        self.submenu_editar.add_command(label="Deslocar Para Direita", command=self.deslocar_direita)
        self.submenu_editar.add_command(label="Deslocar Para Esquerda", command=self.deslocar_esquerda)

        # Cria o submenu "Matriz"
        self.submenu_matriz = tk.Menu(self.menu)
        self.menu.add_command(label="Gerar Matriz", command=self.criar_matriz)

        # Adiciona uma barra de status
        self.status = tk.Label(self.root, text="Pronto", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.imagem_original = None
        self.imagem = None
        self.imagem_path = None
        self.imagem_criada = None

        # Fator de escala padrão
        self.escala = 0.9

    def deslocar_direita(self):
        if self.imagem:
            amplitude = 50  # Amplitude do movimento
            periodo = 60  # Período do movimento (em frames)
            largura_imagem, _ = self.imagem_original.size
            for t in range(periodo):
                deslocamento = int(amplitude * math.sin(2 * math.pi * t / periodo))
                self.canvas.move(self.imagem_criada, deslocamento, 0)
                self.root.update()  # Atualiza a janela
                self.root.after(50)  # Aguarda 50 milissegundos antes de atualizar o próximo frame

    def deslocar_esquerda(self):
        if self.imagem:
            amplitude = 50  # Amplitude do movimento
            periodo = 60  # Período do movimento (em frames)
            largura_imagem, _ = self.imagem_original.size
            for t in range(periodo):
                deslocamento = int(amplitude * math.sin(2 * math.pi * t / periodo))
                self.canvas.move(self.imagem_criada, -deslocamento, 0)
                self.root.update()  # Atualiza a janela
                self.root.after(50)  # Aguarda 50 milissegundos antes de atualizar o próximo frame

    def abrir_imagem(self):
        self.imagem_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if self.imagem_path:
            self.carregar_imagem(self.imagem_path)
            self.status.config(text="Imagem aberta: " + self.imagem_path)

    def carregar_imagem(self, caminho_imagem):
        imagem_original = cv2.imread(caminho_imagem)
        imagem_original = cv2.cvtColor(imagem_original, cv2.COLOR_BGR2RGB)
        self.imagem_original = Image.fromarray(imagem_original)
        self.atualizar_imagem()

    def atualizar_imagem(self):
        largura_canvas = self.canvas.winfo_width()
        altura_canvas = self.canvas.winfo_height()

        largura_imagem = int(self.imagem_original.width * self.escala)
        altura_imagem = int(self.imagem_original.height * self.escala)

        x = (largura_canvas - largura_imagem) // 2
        y = (altura_canvas - altura_imagem) // 2

        self.imagem = ImageTk.PhotoImage(self.imagem_original.resize((largura_imagem, altura_imagem)))
        self.canvas.config(width=largura_canvas, height=altura_canvas)
        self.imagem_criada = self.canvas.create_image(x, y, anchor=tk.NW, image=self.imagem)

    def criar_negativo(self):
        if self.imagem_original:
            imagem_negativa = cv2.bitwise_not(np.array(self.imagem_original))
            self.imagem_original = Image.fromarray(imagem_negativa)
            self.atualizar_imagem()

    def inverter_horizontalmente(self):
        if self.imagem_original:
            imagem_invertida = cv2.flip(np.array(self.imagem_original), 1)
            self.imagem_original = Image.fromarray(imagem_invertida)
            self.atualizar_imagem()

    def inverter_verticalmente(self):
        if self.imagem_original:
            imagem_invertida = cv2.flip(np.array(self.imagem_original), 0)
            self.imagem_original = Image.fromarray(imagem_invertida)
            self.atualizar_imagem()

    def rotacionar_esquerda(self):
        if self.imagem_original:
            imagem_rotacionada = np.rot90(np.array(self.imagem_original))
            self.imagem_original = Image.fromarray(imagem_rotacionada)
            self.atualizar_imagem()

    def rotacionar_direita(self):
        if self.imagem_original:
            imagem_rotacionada = np.rot90(np.array(self.imagem_original), 3)
            self.imagem_original = Image.fromarray(imagem_rotacionada)
            self.atualizar_imagem()

    def definir_escala(self):
        escala = simpledialog.askfloat("Definir Escala", "Digite a escala (porcentagem):", initialvalue=self.escala)
        if escala is not None:
            self.escala = escala / 100
            self.atualizar_imagem()
            self.status.config(text=f"Escala definida para {self.escala * 100}%")

    def salvar_imagem(self):
        if self.imagem_original:
            caminho_salvar = filedialog.asksaveasfilename(defaultextension=".png",
                                                           filetypes=[("Imagem PNG", "*.png"), ("Todos os arquivos", "*.*")])
            if caminho_salvar:
                self.imagem_original.save(caminho_salvar)
                self.status.config(text="Imagem salva como: " + caminho_salvar)

    def criar_matriz(self):
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja gerar a matriz?")
        if resposta:
            if self.imagem_original:
                matriz = np.array(self.imagem_original)
                self.mostrar_matriz(matriz)

    def mostrar_matriz(self, matriz):
        nova_janela = Toplevel(self.root)
        nova_janela.title("Matriz da Imagem")

        texto_matriz = tk.Text(nova_janela, wrap=tk.WORD)
        texto_matriz.pack(expand=True, fill=tk.BOTH)

        # Construindo a representação textual da matriz
        altura, largura, _ = matriz.shape
        for y in range(altura):
            linha_texto = ""
            for x in range(largura):
                coordenada = f"({y}, {x})"
                cor = matriz[y][x]
                linha_texto += f"{coordenada}: {cor};\t"
            texto_matriz.insert(tk.END, linha_texto + "\n")

    def iniciar(self):
        self.root.mainloop()

# Exemplo de uso:
visualizador = VisualizadorDeImagemInterativo()
visualizador.iniciar()
