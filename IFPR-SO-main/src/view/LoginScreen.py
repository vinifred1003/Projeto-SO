import sys
import tkinter as tk

from controller.UserController import userController
from view.viewCadastro import ViewCadastro

class LoginScreen():
    styleConfig = {
        'title': '#e6b400',
        'background':'#222222',
        'entries': '#f4f0e0',
        'errorMessage': 'red',
        'message': 'green'
    }

    def __init__(self):
        self.userController = userController
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)

        self.container = tk.Frame(self.root, bg=self.styleConfig['background'])
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.login()

        self.root.bind('<Escape>', self.close)
        self.root.mainloop()


    def login(self):
        self.loginFrame = tk.Frame(self.container, bg=self.styleConfig['background'])
        self.loginFrame.place(relx=0.5, rely=0.4, anchor='center')

        self.usernameVar = tk.StringVar()
        self.usernameVar.set("Username ou email")
        entryLogin = tk.Entry(self.loginFrame, bg=self.styleConfig['entries'], 
                              text=self.usernameVar, font=('calibre', 18, 'normal'), width=30)
        entryLogin.bind('<FocusIn>', lambda event: self.placeholderOnClick(entryLogin, 'Username ou email', False))
        entryLogin.bind('<FocusOut>', lambda event: self.placeHolderdDefault(entryLogin, 'Username ou email'))
        entryLogin.grid(row=0, column=0, pady=25)

        self.passwordVar = tk.StringVar()
        self.passwordVar.set("Senha")
        entryPassword = tk.Entry(self.loginFrame, bg=self.styleConfig['entries'], 
                                 text=self.passwordVar, font=('calibre', 18, 'normal'), width=30)
        entryPassword.bind('<FocusIn>', lambda event: self.placeholderOnClick(entryPassword, 'Senha', True))
        entryPassword.bind('<FocusOut>', lambda event: self.placeHolderdDefault(entryPassword, 'Senha'))
        entryPassword.grid(row=1, column=0)
        
        buttonCadastrar = tk.Button(self.loginFrame, text="Cadastrar", font=('calibre', 13, 'bold'), command=self.singup)
        buttonCadastrar.grid(row=2, column=0, padx=(200, 0), pady=(15, 0), sticky='w')
        buttonCadastrar.bind("<Enter>", lambda event: self.hoverOn(buttonCadastrar))
        buttonCadastrar.bind("<Leave>", lambda event: self.hoverOut(buttonCadastrar))
        
        buttonEntrar = tk.Button(self.loginFrame, text="Entrar", font=('calibre', 13, 'bold'), command=self.signin)
        buttonEntrar.grid(row=2, column=0, padx=(330, 0), pady=(15, 0), sticky='w')
        buttonEntrar.bind("<Enter>", lambda event: self.hoverOn(buttonEntrar))
        buttonEntrar.bind("<Leave>", lambda event: self.hoverOut(buttonEntrar))

    def singup(self):
        try:
            idUsuario = self.userController.signup(self.usernameVar.get(), self.passwordVar.get())
          
            print(idUsuario)

            self.showMessage("Usuário cadastrado com sucesso")
        except Exception as e:
            self.showError(str(e))

    def signin(self):
        try:
            user = self.userController.signin(self.usernameVar.get(), self.passwordVar.get())
          
            print(user["uid"])

            self.root.destroy()
            ViewCadastro(user["uid"])
            
            
        except Exception as e:
            self.showError(str(e))

    def placeholderOnClick(self, entry, entryText, isPassword):
        if entry.get() == entryText:
            entry.delete(0, tk.END)
            
            if (isPassword):
                entry.configure(show="*")
    
    def placeHolderdDefault(self, entry, entryText):
        if entry.get() == '':
            entry.insert(0, entryText)
            entry.configure(show='')

    def hoverOn(self, widget):
        widget['background'] = 'green'
        
    def hoverOut(self, widget):
        widget['background'] = 'SystemButtonFace'
        
    def showError(self, message):
        labelErro = tk.Label(self.loginFrame, text=message, 
            bg=self.styleConfig['background'], fg=self.styleConfig['errorMessage'], font=('Arial', 15, 'bold'))
        
        labelErro.grid(row=3, column=0, sticky='sw')
        
    def showMessage(self, message):
        print(message)
        labelErro = tk.Label(self.loginFrame, text=message, 
            bg=self.styleConfig['background'], fg=self.styleConfig['message'], font=('Arial', 15, 'bold'))
        
        labelErro.grid(row=3, column=0, sticky='sw')

    def close(self, evento=None):
        sys.exit()


LoginScreen()