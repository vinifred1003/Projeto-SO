from tkinter import *

from controller.ProcessController import ProcessController

class Cadastro(Toplevel):
    def __init__(self, janela_classe_visivel, mainClass, userUid =None, dados_registro=None, processPid = None):
        super().__init__(janela_classe_visivel)

        
        self.mainClass = mainClass
        self.userUid = userUid
        self.processPid = processPid
        self.dados_registro = dados_registro
        self.processController = ProcessController(userUid)
    
        self.janela_classe_visivel = janela_classe_visivel
        
        self.run()
        self.insercoes()
        self.botao()
    
        if dados_registro:
            self.preencher_campos(dados_registro)


    def run(self):
        self.title("Cadastrar Sistema")
        self.geometry("600x300")
        self.configure(background="#7092BE")
        self.resizable(True, True)
    
    def preencher_campos(self, dados_registro):
        self.entryPrioridade.delete(0, END)
        self.entryUsoDaCPU.delete(0, END)
        self.entryEstado.delete(0, END)
        self.entryUsoDaMemoria.delete(0, END)
    
        self.entryPrioridade.insert(0, dados_registro["priority"])
        self.entryUsoDaCPU.insert(0, dados_registro["cpu_usage"])
        self.entryEstado.insert(0, dados_registro["state"])
        self.entryUsoDaMemoria.insert(0, dados_registro["memory_space"])

    def insercoes(self):
        self.lbPrioridade = Label(self, text="Prioridade", fg="white", bg="gray")
        self.lbPrioridade.place(relx=0.1, rely=0.15)

        self.entryPrioridade = Entry(self, bd=2, bg="white")
        self.entryPrioridade.place(relx=0.1, rely=0.25)

        self.lbUsoDaCPU = Label(self, text="Uso da CPU", fg="white", bg="gray")
        self.lbUsoDaCPU.place(relx=0.1, rely=0.35)

        self.entryUsoDaCPU = Entry(self, bd=2, bg="white")
        self.entryUsoDaCPU.place(relx=0.1, rely=0.45)

        self.lbEstado = Label(self, text="Estado", fg="white", bg="gray")
        self.lbEstado.place(relx=0.6, rely=0.15)

        self.entryEstado = Entry(self, bd=2, bg="white")
        self.entryEstado.place(relx=0.6, rely=0.25)

        self.lbUsoDaMemoria = Label(self, text="Uso da memória", fg="white", bg="gray")
        self.lbUsoDaMemoria.place(relx=0.6, rely=0.35)

        self.entryUsoDaMemoria = Entry(self, bd=2, bg="white")
        self.entryUsoDaMemoria.place(relx=0.6, rely=0.45)
    
    def Quit(self):
        self.destroy()
    
    def botao(self):
        self.BotaoSalvar = Button(self, bd=2, text="Salvar", command=self.enviar)
        self.BotaoSalvar.place(relx=0.40, rely=0.65, relwidth=0.2, relheight=0.1)
        
    def enviar(self):
        process = {
            "priority": self.entryPrioridade.get(), 
            "cpu_usage": self.entryUsoDaCPU.get(), 
            "state": self.entryEstado.get(), 
            "memory_space": self.entryUsoDaMemoria.get()
        }
        if self.processPid:
            self.processController.update(process, self.processPid, self.userUid)  
            print("Registro atualizado com sucesso.")
        else:
            processId = self.processController.create(self.userUid, process)
            print("Registro criado com sucesso. ID do processo:", processId)
            print(processId)

        self.mainClass.atualizar()
        self.janela_classe_visivel.destroy()