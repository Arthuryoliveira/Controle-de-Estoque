import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# Caminho do arquivo onde o estoque será salvo
ARQUIVO_ESTOQUE = "estoque.csv"

# Cria o arquivo de estoque se ainda não existir
def inicializar_arquivo():
    if not os.path.exists(ARQUIVO_ESTOQUE):
        with open(ARQUIVO_ESTOQUE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Nome", "Quantidade"])

# Lê os dados do arquivo e devolve como lista
def carregar_dados():
    with open(ARQUIVO_ESTOQUE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        return list(reader)

# Salva todos os dados no arquivo, sobrescrevendo o anterior
def salvar_dados(dados):
    with open(ARQUIVO_ESTOQUE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Nome", "Quantidade"])
        writer.writerows(dados)

# Atualiza a tabela da interface com os dados mais recentes
def atualizar_tabela():
    for row in tree.get_children():
        tree.delete(row)

    dados = carregar_dados()
    dados.sort(key=lambda x: x[0].lower())  # Ordena pelo nome, ignorando maiúsculas/minúsculas

    for index, item in enumerate(dados):
        if index % 2 == 0:
            tree.insert("", tk.END, values=item, tags=("cinza",))  # Linha com fundo cinza
        else:
            tree.insert("", tk.END, values=item, tags=("branco",))  # Linha com fundo branco

# Adiciona um novo item ao estoque
def adicionar_item():
    nome = entry_nome.get().strip()
    quantidade = entry_quantidade.get().strip()

    if not nome or not quantidade.isdigit():
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        return

    salvar_item(nome, quantidade)
    atualizar_tabela()
    limpar_campos()

# Grava um item novo no final do arquivo CSV
def salvar_item(nome, quantidade):
    with open(ARQUIVO_ESTOQUE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([nome, quantidade])

# Altera a quantidade de um item já existente
def editar_quantidade():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um item para editar.")
        return

    novo_valor = entry_quantidade.get().strip()
    if not novo_valor.isdigit():
        messagebox.showerror("Erro", "A quantidade deve ser um número válido.")
        return

    item = tree.item(selecionado)
    nome = item["values"][0]

    dados = carregar_dados()
    for linha in dados:
        if linha[0] == nome:
            linha[1] = novo_valor  # Atualiza a quantidade
            break

    salvar_dados(dados)
    atualizar_tabela()
    limpar_campos()

# Soma a quantidade informada ao item já existente (ou cria novo)
def registrar_entrada():
    nome = entry_nome.get().strip()
    quantidade = entry_quantidade.get().strip()

    if not nome or not quantidade.isdigit():
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        return

    quantidade = int(quantidade)
    dados = carregar_dados()
    for linha in dados:
        if linha[0] == nome:
            linha[1] = str(int(linha[1]) + quantidade)
            break
    else:
        dados.append([nome, str(quantidade)])

    salvar_dados(dados)
    atualizar_tabela()
    limpar_campos()

# Subtrai a quantidade informada do item, se possível
def registrar_retirada():
    nome = entry_nome.get().strip()
    quantidade = entry_quantidade.get().strip()

    if not nome or not quantidade.isdigit():
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        return

    quantidade = int(quantidade)
    dados = carregar_dados()
    for linha in dados:
        if linha[0] == nome:
            nova_quantidade = int(linha[1]) - quantidade
            if nova_quantidade < 0:
                messagebox.showerror("Erro", "Quantidade insuficiente em estoque.")
                return
            linha[1] = str(nova_quantidade)
            break
    else:
        messagebox.showerror("Erro", "Item não encontrado no estoque.")
        return

    salvar_dados(dados)
    atualizar_tabela()
    limpar_campos()

# Limpa os campos de entrada na tela
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)

# Cria o arquivo se ainda não existir
inicializar_arquivo()

# Janela principal
app = tk.Tk()
app.title("Estoque Resíduos")

# Bloco de entrada de dados (formulário)
frame_form = tk.Frame(app)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nome do Item:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5)
entry_quantidade = tk.Entry(frame_form)
entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

entry_quantidade.bind("<Return>", lambda event: adicionar_item())

tk.Button(frame_form, text="Registrar Entrada", command=registrar_entrada).grid(row=2, column=0, padx=5, pady=10)
tk.Button(frame_form, text="Adicionar", command=adicionar_item).grid(row=3, column=0, padx=5, pady=10)
tk.Button(frame_form, text="Editar Quantidade", command=editar_quantidade).grid(row=3, column=1, padx=5, pady=10)
tk.Button(frame_form, text="Registrar Retirada", command=registrar_retirada).grid(row=3, column=2, padx=5, pady=10)

# Tabela onde os itens são mostrados
columns = ("Nome", "Quantidade")
tree = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.tag_configure("branco", background="white")
tree.tag_configure("cinza", background="#D3D3D3")

tree.pack(pady=10)

# Preenche a tabela com os dados atuais
atualizar_tabela()

app.mainloop()

