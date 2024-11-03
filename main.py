import tkinter as tk
import os
import sys

class ProporcaoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculadora de Proporção")

        # Inicializa as variáveis V e F
        self.V = None
        self.F = None

        # Dicionário para rastrear o número de cliques em cada botão
        self.button_clicks = {}
        self.buttons = []  # Lista para armazenar referências aos botões

        self.label = tk.Label(master, text="Pressione um número de 0 a 9 para definir V e F.")
        self.label.pack(pady=10)

        self.result_label = tk.Label(master, text="")
        self.result_label.pack(pady=10)

        self.master.bind_all("<Key>", self.on_key_press)  # Captura eventos de tecla em toda a aplicação

        self.quit_button = tk.Button(master, text="Sair", command=master.quit)
        self.quit_button.pack(pady=5)

        self.restart_button = tk.Button(master, text="Reiniciar", command=self.restart_program)
        self.restart_button.pack(pady=5)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        # Configura a janela para estar sempre no canto superior esquerdo
        self.master.geometry("300x200+0+0")  # Largura x Altura + X + Y
        self.master.attributes("-topmost", True)  # Mantém a janela sempre visível

    def on_key_press(self, event):
        if event.char.isdigit():
            num = int(event.char)
            if self.V is None:
                self.V = num
                self.label.config(text=f"V definido como {self.V}. Pressione um número para F.")
            elif self.F is None:
                self.F = num
                self.label.config(text=f"F definido como {self.F}.")
                self.calculate_proporcao()
                self.create_button_matrix()  # Cria a matriz de botões após definir V e F
        elif event.char == 'v' and self.V is not None:
            self.highlight_smallest_button('V')  # Destaca o menor botão
        elif event.char == 'f' and self.F is not None:
            self.highlight_smallest_button('F')  # Destaca o menor botão

    def calculate_proporcao(self):
        proporcao = self.V / (self.V + self.F) if (self.V + self.F) != 0 else 0
        self.result_label.config(text=f"Proporção P = {proporcao:.2f} (V = {self.V}, F = {self.F})")

    def create_button_matrix(self):
        """Cria uma matriz de botões com 1 de altura e comprimento igual a T (V + F)."""
        # Limpa botões antigos
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        T = self.V + self.F  # Soma de V e F
        self.buttons = []  # Limpa a lista de botões
        for i in range(T):
            button = tk.Button(self.button_frame, text=f"{i+1}", bg='white', command=lambda i=i: self.on_button_click(i))
            button.pack(side=tk.LEFT, padx=2)
            self.button_clicks[i] = 0  # Inicializa o contador de cliques para cada botão
            self.buttons.append(button)  # Armazena a referência do botão

        # Ajusta o tamanho da janela automaticamente
        self.master.update_idletasks()
        self.master.geometry(f"{self.master.winfo_width()}x{self.master.winfo_height()}+0+0")  # Mantém a posição no canto superior esquerdo

    def highlight_smallest_button(self, action):
        """Destaca o menor botão que não está preto, mudando sua cor para preto."""
        if self.buttons:
            smallest_button_index = None
            for i in range(len(self.buttons)):
                if self.buttons[i].cget("bg") != 'black':  # Verifica se o botão não está preto
                    if smallest_button_index is None or self.button_clicks[i] < self.button_clicks[smallest_button_index]:
                        smallest_button_index = i

            # Muda a cor do menor botão que não está preto para preto
            if smallest_button_index is not None:
                # Reseta a cor de todos os botões que não estão pretos
                for i, button in enumerate(self.buttons):
                    if button.cget("bg") != 'black':
                        if self.button_clicks[i] == 1:
                            button.config(bg='red')  # Muda para vermelho
                        elif self.button_clicks[i] == 2:
                            button.config(bg='blue')  # Muda para azul
                        else:
                            button.config(bg='white')  # Volta à cor padrão

                # Verifica se o botão que deve ficar preto é vermelho ou azul
                if self.buttons[smallest_button_index].cget("bg") in ['red', 'blue']:
                    # Desfaz a subtração de V ou F
                    if self.buttons[smallest_button_index].cget("bg") == 'red':
                        self.V += 1
                    else:
                        self.F += 1

                self.buttons[smallest_button_index].config(bg='black')  # Destaca o menor botão
                if action == 'V':
                    self.V -= 1  # Diminui V em 1
                elif action == 'F':
                    self.F -= 1  # Diminui F em 1
                self.calculate_proporcao()  # Atualiza a proporção

    def on_button_click(self, index):
        """Ação a ser realizada quando um botão da matriz é clicado."""
        current_color = self.buttons[index].cget ("bg")  # Obtém a cor atual do botão
        self.button_clicks[index] += 1  # Incrementa o contador de cliques

        if self.button_clicks[index] == 1:
            self.buttons[index].config(bg='red')  # Muda para vermelho
            self.V -= 1  # Diminui V em 1
        elif self.button_clicks[index] == 2:
            self.buttons[index].config(bg='blue')  # Muda para azul
            self.F -= 1  # Diminui F em 1
            self.V += 1  # Desfaz a subtração de V
        elif self.button_clicks[index] == 3:
            self.F += 1  # Desfaz a subtração de F
            self.buttons[index].config(bg='white')  # Volta à cor padrão
            self.button_clicks[index] = 0  # Reseta o contador

        self.calculate_proporcao()  # Atualiza a proporção


    def restart_program(self):
        """Reinicia o programa."""
        self.master.destroy()  # Destroi a janela atual
        root = tk.Tk()
        app = ProporcaoApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProporcaoApp(root)
    root.mainloop()