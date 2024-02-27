import os
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from PIL import Image, ImageTk
from backend import Imagem, Download, Filtro, Principal


class GUI:
    def __init__(self, master):
        self.master = master
        self.principal = principal
        master.title("Aplicação de Filtros")

        self.configurar_tamanho_tela()

        self.frame = tk.Frame(master)
        self.frame.pack(expand=True, fill='both', pady=10)

        lbl_menu_principal = tk.Label(self.frame, text="Menu Principal", font=("Montserrat", 16))
        lbl_menu_principal.pack(pady=10)

        self.opcoes_menu()

        style = ttk.Style()
        style.configure("TButton", font=("Montserrat", 12), padding=10, borderwidth=3)

    def configurar_tamanho_tela(self):
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        x_pos = int((largura_tela - 500) / 2)
        y_pos = int((altura_tela - 300) / 3)
        self.master.geometry(f"500x400+{x_pos}+{y_pos}")

    def opcoes_menu(self):
        btn_carregar = ttk.Button(self.frame, text="Carregar Imagem", command=self.carregar_imagem, width=20)
        btn_carregar.pack(pady=(0, 10), padx=20)

        btn_selecionar_filtro = ttk.Button(self.frame, text="Selecionar Filtro", command=self.selecionar_filtro, width=20)
        btn_selecionar_filtro.pack(pady=10, padx=20)

        btn_mostrar_imagens = ttk.Button(self.frame, text="Mostrar Imagens", command=self.mostrar_imagens, width=20)
        btn_mostrar_imagens.pack(pady=10, padx=20)

        btn_sair = ttk.Button(self.frame, text="Sair", command=self.master.quit, width=10)
        btn_sair.pack(pady=10, padx=20)

    def carregar_imagem(self):
        def carregar():
            caminho = entry_caminho.get()
            try:
                Principal.informar_Caminho(self, caminho) # faz o download e carrega a imagem
                tk.messagebox.showinfo("Sucesso", "Imagem carregada com sucesso :)")
                janela_carregar.destroy()
            except:
                tk.messagebox.showerror("Erro", "Caminho de imagem inválido!\n\nVerifique se a URL é válida ou se você digitou imagens/nome-do-arquivo")

        janela_carregar = tk.Toplevel(self.master)
        janela_carregar.title("Carregar Imagem")
        janela_carregar.geometry("400x200")

        lbl_instrucao = ttk.Label(janela_carregar, text="Insira a URL (local ou externa) da imagem:", font=("Helvetica", 12))
        lbl_instrucao.pack(pady=10)

        entry_caminho = ttk.Entry(janela_carregar, width=50)
        entry_caminho.pack(pady=10)

        btn_carregar = ttk.Button(janela_carregar, text="Prosseguir", command=carregar)
        btn_carregar.pack(pady=5)

        btn_voltar = ttk.Button(janela_carregar, text="Voltar", command=janela_carregar.destroy, width=5)
        btn_voltar.pack(pady=5)

    def selecionar_filtro(self):
        def aplicar_filtro():
            try:
                nome_filtro = filtro_combobox.get()
                filtro_selecionado = filtro_classes[nome_filtro]
                imagem_filtrada = Filtro.aplicar_filtro(filtro_selecionado, self.imagem)
                Imagem(self.caminho).salvar_imagem(imagem_filtrada, filtro_selecionado.__name__)
                tk.messagebox.showinfo("Sucesso", "Filtro aplicado com sucesso!")
                modal.destroy()
            except:
                tk.messagebox.showerror("Erro", "O filtro não pôde ser aplicado por alguma razão.")
                modal.destroy()

        modal = tk.Toplevel(self.master)
        modal.title("Selecionar Filtro")
        modal.geometry("400x200")

        estilo_combobox = ttk.Style()
        estilo_combobox.configure('TCombobox', font=('Helvetica', 12))
        
        filtro_classes = {
            "Escala Cinza": Filtro.EscalaCinza,
            "Preto e Branco": Filtro.PretoBranco,
            "Cartoon": Filtro.Cartoon,
            "Foto Negativa": Filtro.FotoNegativa,
            "Contorno": Filtro.Contorno,
            "Blurred": Filtro.Blurred
        }

        filtro_combobox = ttk.Combobox(modal, values=["Escala Cinza", "Preto e Branco", "Cartoon", "Foto Negativa", "Contorno", "Blurred"], state="readonly")
        filtro_combobox.pack(pady=20)

        estilo_aplicar = ttk.Style()
        estilo_aplicar.configure('EstiloAplicar.TButton', font=('Helvetica', 12), foreground='black', padx=10, pady=5)
        
        aplicar_button = ttk.Button(modal, text="Aplicar", style='EstiloAplicar.TButton')
        aplicar_button.pack()

        aplicar_button.config(command=aplicar_filtro)

        btn_voltar = ttk.Button(modal, text="Voltar", command=modal.destroy, width=5)
        btn_voltar.pack(pady=(20,5))

    def mostrar_imagens(self):
        imagens = self.listar_imagens()
        if imagens:
            self.mostrar_janela_imagens(imagens)
        else:
            tk.messagebox.showinfo("Informação", "Nenhuma imagem disponível no diretório.")

    def listar_imagens(self):
        imagens = []
        for arquivo in os.listdir('imagens'):
            if arquivo.endswith(".jpg") or arquivo.endswith(".png") or arquivo.endswith(".jpeg"):
                imagens.append(arquivo)
        return imagens

    def mostrar_janela_imagens(self, imagens):
        self.janela_imagens = Toplevel(self.master)
        self.janela_imagens.title("Imagens do Diretório")

        self.indice_imagem_atual = 0

        self.imagem_atual = None
        self.label_imagem = tk.Label(self.janela_imagens)
        self.label_imagem.pack(padx=10, pady=10)

        self.label_nome_arquivo = tk.Label(self.janela_imagens, text="", font=("Helvetica", 12))
        self.label_nome_arquivo.pack(pady=5)


        self.btn_anterior = ttk.Button(self.janela_imagens, text="Anterior", command=self.imagem_anterior)
        self.btn_anterior.pack(side="left", padx=10, pady=10)

        self.btn_proxima = ttk.Button(self.janela_imagens, text="Próxima", command=self.proxima_imagem)
        self.btn_proxima.pack(side="right", padx=10, pady=10)

        self.mostrar_nova_imagem(imagens[self.indice_imagem_atual], imagens)

    def mostrar_nova_imagem(self, imagem_atual, imagens):
        imagem_path = os.path.join('imagens', imagem_atual)
        imagem = Image.open(imagem_path)
        imagem.thumbnail((300, 300))
        self.imagem_atual = ImageTk.PhotoImage(imagem)
        self.label_imagem.config(image=self.imagem_atual)

        # Obtém o nome do arquivo atual
        nome_arquivo = os.path.basename(imagem_atual)
        
        # Exibe o nome do arquivo
        self.label_nome_arquivo.config(text=nome_arquivo)

        if self.indice_imagem_atual == 0:
            self.btn_anterior.config(state="disabled")
        else:
            self.btn_anterior.config(state="enabled")

        if self.indice_imagem_atual == len(imagens) - 1:
            self.btn_proxima.config(state="disabled")
        else:
            self.btn_proxima.config(state="enabled")

    def proxima_imagem(self):
        self.indice_imagem_atual += 1
        imagens = self.listar_imagens()
        if self.indice_imagem_atual < len(imagens):
            self.mostrar_nova_imagem(imagens[self.indice_imagem_atual], imagens)
        else:
            # Exibe uma mensagem informando que é a última imagem
            tk.messagebox.showinfo("Informação", "Você chegou à última imagem.")
            # Reduz o índice da imagem atual para exibir a última imagem
            self.indice_imagem_atual = len(imagens) - 1
            self.mostrar_nova_imagem(imagens[self.indice_imagem_atual], imagens)

    def imagem_anterior(self):
        self.indice_imagem_atual -= 1
        imagens = self.listar_imagens()
        if self.indice_imagem_atual >= 0:
            self.mostrar_nova_imagem(imagens[self.indice_imagem_atual], imagens)
        else:
            # Exibe uma mensagem informando que é a primeira imagem
            tk.messagebox.showinfo("Informação", "Você está na primeira imagem.")
            # Define o índice da imagem atual como 0 para exibir a primeira imagem novamente
            self.indice_imagem_atual = 0
            self.mostrar_nova_imagem(imagens[self.indice_imagem_atual], imagens)

if __name__ == "__main__":
    root = tk.Tk()
    principal = Principal()
    gui = GUI(root)
    root.mainloop()
