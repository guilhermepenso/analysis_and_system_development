import tkinter as tk
from tkinter import messagebox
import random
import string
import tkinter.simpledialog
import itertools
from datetime import datetime
import time


# Função para gerar caracteres sequenciais pelo itertools

def process_name_generator():
    size = 1
    while True:
        for s in itertools.product(string.ascii_uppercase, repeat = size):
            yield "".join(s)
        size += 1
        
# Classe que engloba toda a parte do gerenciamento e lógica da memória

class memory_manager:
    
    # Função com declarações self
    
    def __init__(self, master):
        self.master = master
        self.grid = []
        self.selected = []
        self.groups = {}
        self.process = {}
        self.chars = process_name_generator()
        self.create_grid()

    # Função para criação da tabela para alocar os processamentos de forma visual e lógica
    
    def create_grid(self):
        frame = tk.Frame(self.master)
        frame.pack(expand=True)
        for i in range(10):
            row = []
            for j in range(10):
                label = tk.Label(frame, bg="white", width=3, height=1, relief="solid", borderwidth=1)
                label.grid(row=i, column=j)
                label.bind("<Button-1>", self.select)
                row.append(label)
            self.grid.append(row)

    def allocate(self):
        n = tkinter.simpledialog.askinteger("Entrada", "Qual o tamanho do processo a ser alocado?")
        free_blocks = []
        total_free = 0
        best_fit = None
        for i in range(10):
            for j in range(10):
                if self.grid[i][j]['background'] == "white":
                    total_free += 1
                    free_blocks.append((i, j))
                else:
                    if len(free_blocks) >= n:
                        if best_fit is None or len(best_fit) > len(free_blocks):
                                best_fit = list(free_blocks)
                        free_blocks = []
        if len(free_blocks) >= n and (best_fit is None or len(best_fit) > len(free_blocks)):
            best_fit = list(free_blocks)
        if total_free < n:
            messagebox.showinfo("Erro", "Sem espaço, precisa liberar espaço!")
            return
        if best_fit is None:
            messagebox.showinfo("Erro", "Sem espaço sequencial, realocar os processos!")
            return
        color= "#{:06x}".format(random.randint(0, 0xFFFFFF))
        id_group = next(self.chars)
        for k in range(n):
            self.grid[best_fit[k][0]][best_fit[k][1]]["background"] = color
            self.grid[best_fit[k][0]][best_fit[k][1]]["text"] = id_group
        self.groups[id_group] = color
        self.process[id_group] = {'size': n, 'alocation_time': datetime.now(), 'deallocation_time': None}
               
    def select(self, event):
        if event.widget['text'] != "":
            id_group = event.widget['text']
            color = self.groups[id_group]
            for i in range(10):
                for j in range(10):
                    if self.grid[i][j]["text"] == id_group:
                        if self.grid[i][j]["background"] == color:
                            self.grid[i][j]["background"] = "orange"
                            self.selected.append(self.grid[i][j])
                        else:
                            self.grid[i][j]["background"] = color
                            self.selected.append(self.grid[i][j]) ###n seiiiiii##   
                                           
    def deallocate(self):
        for widget in self.selected:
            id_group = widget["text"]
            if id_group in self.process:
                self.process[id_group]["deallocation_time"] = datetime.now()
            widget['background'] = "white"
            widget['text'] = ""
        self.selected = []

    def reallocate(self):
        memory_blocks = []
        for i in range(10):
            for j in range(10):
                if self.grid[i][j]['background'] != "white":
                    memory_blocks.append((i, j, self.grid[i][j]["text"], self.grid[i][j]["background"]))
                    self.grid[i][j]['background'] = "white"
                    self.grid[i][j]['text'] = ""
        index = 0
        x, y = 0, 0
        for i in range(10):
            for j in range(10):
                if index < len(memory_blocks):
                    if y == 10:
                        x += 1
                        y = 0
                    self.grid[x][y].grid(row=i, column=j)
                    self.grid[x][y]['background'] = memory_blocks[index][3]
                    self.grid[x][y]['text'] = memory_blocks[index][2]
                    index += 1
                root.update()
                y += 1

root = tk.Tk()
root.geometry("400x350")  # Fixa o tamanho da janela
root.resizable(0, 0)  # Desativa a opção de tela cheia

title = tk.Label(root, text="", font=("Arial", 20))  # Adiciona um título
title.pack(pady=10)  # Posiciona o título acima da grade

mm = memory_manager(root)

button_frame = tk.Frame(root)  # Cria um novo frame para os botões
button_frame.pack(side="top", fill="x", pady=20)  # Adiciona preenchimento vertical

allocate_button = tk.Button(button_frame, text="Alocar", command=mm.allocate, height=2, width=10)
allocate_button.pack(side="left", padx=10)

deallocate_button = tk.Button(button_frame, text="Desalocar", command=mm.deallocate, height=2, width=10)
deallocate_button.pack(side="left", padx=10)

reallocate_button = tk.Button(button_frame, text="Realocar", command=mm.reallocate, height=2, width=10)
reallocate_button.pack(side="left", padx=10)

root.mainloop()