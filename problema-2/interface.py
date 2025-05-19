import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from pathlib import Path

from src.autenticacao.autenticacao import login, criar_conta
from src.analise.visualizar_dados import visualizar_dados
from relatorios.relatorios import gerar_relatorio

CAMINHO_CONTAS = Path("data/contas.csv")
CAMINHO_DADOS = Path("data/pacientes")

# 🎨 Paleta de cores
COR_FUNDO = "#f0f4f7"
COR_TITULO = "#0a3d62"
COR_BOTAO = "#3c6382"
COR_TEXTO_BOTAO = "white"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Dados Médicos")
        self.root.configure(bg=COR_FUNDO)
        self.frame = tk.Frame(root, bg=COR_FUNDO)
        self.frame.pack(padx=20, pady=20)
        self.menu_principal()

    def limpar_tela(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def menu_principal(self):
        self.limpar_tela()
        self._titulo("Sistema de Gerenciamento de Dados Médicos")
        self._botao("Login", self.menu_login)
        self._botao("Criar Conta", self.menu_criar_conta)
        self._botao("Sair", self.root.quit)

    def menu_login(self):
        email = simpledialog.askstring("Login", "Email:")
        senha = simpledialog.askstring("Login", "Senha:", show="*")
        if email and senha:
            sucesso, msg = login(CAMINHO_CONTAS, email, senha)
            messagebox.showinfo("Login", msg)
            if sucesso:
                if "@medico.com" in email:
                    self.menu_profissional()
                elif email == "admin@admin.com":
                    self.menu_admin()
                else:
                    self.menu_paciente()
        else:
            messagebox.showwarning("Campos vazios", "Preencha todos os campos!")

    def menu_criar_conta(self):
        nome = simpledialog.askstring("Criar Conta", "Nome:")
        email = simpledialog.askstring("Criar Conta", "Email:")
        senha = simpledialog.askstring("Criar Conta", "Senha:")
        if nome and email and senha:
            sucesso, msg = criar_conta(CAMINHO_CONTAS, nome, email, senha)
            messagebox.showinfo("Criar Conta", msg)
        else:
            messagebox.showwarning("Campos vazios", "Preencha todos os campos!")

    def menu_paciente(self):
        self.limpar_tela()
        self._titulo("Área do Paciente")
        self._botao("Visualizar Dados", self.visualizar_csv)
        self._botao("Voltar", self.menu_principal)

    def menu_profissional(self):
        self.limpar_tela()
        self._titulo("Área Médica")
        self._botao("Visualizar Dados", self.visualizar_csv)
        self._botao("Gerar Relatório", self.gerar_relatorio)
        self._botao("Voltar", self.menu_principal)

    def menu_admin(self):
        self.limpar_tela()
        self._titulo("Painel Administrativo")
        self._botao("Criar Conta Manual", self.menu_criar_conta)
        self._botao("Voltar", self.menu_principal)

    def visualizar_csv(self):
        caminho = filedialog.askopenfilename(initialdir=CAMINHO_DADOS, title="Selecione o arquivo CSV")
        if caminho:
            visualizar_dados(Path(caminho), 10)

    def gerar_relatorio(self):
        caminho = filedialog.askopenfilename(initialdir=CAMINHO_DADOS, title="CSV para relatório")
        if caminho:
            formato = simpledialog.askstring("Formato", "csv ou json:")
            if formato in ["csv", "json"]:
                relatorio = gerar_relatorio(list(Path(caminho).read_text().splitlines()), formato)
                messagebox.showinfo("Relatório", f"Relatório gerado: {relatorio}")
            else:
                messagebox.showwarning("Formato inválido", "Use csv ou json.")

    # 🔹 Funções auxiliares para UI
    def _titulo(self, texto):
        tk.Label(self.frame, text=texto, font=("Arial", 16, "bold"), bg=COR_FUNDO, fg=COR_TITULO).pack(pady=10)

    def _botao(self, texto, comando):
        tk.Button(
            self.frame,
            text=texto,
            width=30,
            bg=COR_BOTAO,
            fg=COR_TEXTO_BOTAO,
            font=("Arial", 11),
            relief="raised",
            command=comando
        ).pack(pady=6)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
