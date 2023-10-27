import tkinter as tk
from tkinter import Menu
from tkinter import *
from tkinter import ttk
import sys
from view.cadastro import Cadastro
from controller.ProcessController import ProcessController

class ViewCadastro():
    def __init__(self, user_uid):
        self.userUid = user_uid
        self.root = tk.Tk()  
        self.root.attributes('-fullscreen', True)

        self.processController = ProcessController(user_uid) 
        self.processController.deleteAll()
        
        self.run()
        self.menus()
        self.Registros()
        self.botoes()
        self.excluir()
        self.editar()
        
        self.root.after(5000, self.atualizar_periodicamente) 
        
        self.root.bind('<Escape>', self.close)
        self.root.mainloop() 
    
    def run(self):
        self.root.title("Cadastros do Sistema")
        self.root.geometry("600x400")
        self.root.configure(background="gray")
        self.root.resizable(True, True)
    
    def CadastroNovo(self):
        self.root2 = Toplevel()
        self.root2.withdraw() 
        Cadastro(self.root2, self, self.userUid)

    def chamarCadastro(self, process_id):  
        self.root2 = Toplevel()
        self.root2.withdraw() 
        
        dados_processo = self.processController.getProcesso(process_id)
        
        Cadastro(self.root2, self, self.userUid, dados_processo, process_id)
        
        self.atualizar()

    def atualizar(self):
        self.listR.delete(*self.listR.get_children())
        dados = self.processController.list(self.userUid)
        for item in dados:
            self.listR.insert("", "end", values=item)


    def Registros(self):
      self.FrameRegistros = Frame(self.root, bd=4, bg='white')
      self.FrameRegistros.place(relx=0, rely=0, relwidth=1, relheight=0.9)
      
      self.listR = ttk.Treeview(self.FrameRegistros, height=4, column=("col1, col2, col3, col4, col5, col6"))
      self.listR.heading("#0", text="")
      self.listR.heading("#1", text="PID")
      self.listR.heading("#2", text="Nome")
      self.listR.heading("#3", text="Prioridade")
      self.listR.heading("#4", text="Uso da CPU")
      self.listR.heading("#5", text="Estado")
      self.listR.heading("#6", text="Uso Da Memória")

      self.listR.column("#0", width=1)
      self.listR.column("#1", width=50)
      self.listR.column("#2", width=50)
      self.listR.column("#3", width=200)
      self.listR.column("#4", width=125)
      self.listR.column("#5", width=125)
      self.listR.column("#6", width=50)
      
      self.listR.place(relx=0, rely=0, relwidth=1, relheight=1)
      
      self.scrollListR = Scrollbar(self.FrameRegistros, orient_='vertical')
      self.listR.configure(yscroll=self.scrollListR.set)
      self.scrollListR.place(relx=0.98, rely=0.05, relwidth=0.015, relheight=0.9)

    def menus(self):
        menubar = Menu(self.root)  
        self.root.config(menu=menubar)
        fileMenu = Menu(menubar, tearoff=0)  

        def quit_app():
            self.root.destroy()  

        menubar.add_cascade(label="Opções", menu=fileMenu)

        fileMenu.add_command(label="Cadastrar", command=self.CadastroNovo)  
        fileMenu.add_command(label="Sair", command=quit_app)  
        
    def botoes(self):
        self.FrameBotoes = Frame(self.root, bd=4, bg='white')
        self.FrameBotoes.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)   
       
        self.BotaoExcluir = Button(self.FrameBotoes, bd=2, text="Excluir",command=self.excluir)
        self.BotaoExcluir.place(relx=0.40, rely=0.65, relwidth=0.2, relheight=0.4)

        self.lbId = Label(self.FrameBotoes, text="PID", fg="white", bg="gray")
        self.lbId.place(relx=0.1, rely=0.15)

        self.entryId = Entry(self.FrameBotoes, bd=2, bg="white")
        self.entryId.place(relx=0.1, rely=0.50)

        self.BotaoUpdate = Button(self.FrameBotoes, bd=2, text="Editar", command=self.editar)
        self.BotaoUpdate.place(relx=0.20, rely=0.65, relwidth=0.2, relheight=0.4)

    def excluir(self):
        process_id_selecionado = self.entryId.get()
    
        self.processController.delete(process_id_selecionado, self.userUid)

        self.atualizar()
    
    def editar(self):
        process_id_selecionado = self.entryId.get()
        if process_id_selecionado:
            self.chamarCadastro(process_id_selecionado)
        else:    
            pass
        
    def close(self, evento=None):
        sys.exit()
        

    def atualizar_periodicamente(self):
        print("ENTROU - FRONT")
        self.processController.mudarEstadosDosProcessos(self.userUid)
        self.atualizar()
        self.root.after(5000, self.atualizar_periodicamente) 
