import sqlite3
import pandas as pd
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Toplevel, ttk
from datetime import datetime

# Função para conectar ao banco de dados SQLite
def connect_db():
    return sqlite3.connect('sistema_gado.db')

# Função para criar a tabela de gado
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            data_nascimento DATE,
            vacina TEXT,
            alimentacao TEXT,
            outros_cuidados TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar um novo gado
def add_gado(nome, data_nascimento, vacina, alimentacao, outros_cuidados):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO gado (nome, data_nascimento, vacina, alimentacao, outros_cuidados)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, data_nascimento, vacina, alimentacao, outros_cuidados))
    conn.commit()
    conn.close()

# Função para ler todos os registros de gado
def read_gado():
    conn = connect_db()
    query = 'SELECT * FROM gado'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Função para atualizar um registro de gado
def update_gado(id, nome, data_nascimento, vacina, alimentacao, outros_cuidados):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE gado
        SET nome = ?, data_nascimento = ?, vacina = ?, alimentacao = ?, outros_cuidados = ?
        WHERE id = ?
    ''', (nome, data_nascimento, vacina, alimentacao, outros_cuidados, id))
    conn.commit()
    conn.close()

# Função para deletar um registro de gado
def delete_gado(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM gado WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Função para gerar relatórios sumarizados
def generate_report():
    df = read_gado()
    report = df.describe(include='all')
    return report

# Função chamada quando o botão de adicionar é pressionado
def submit_data():
    nome = nome_var.get()
    data_nascimento = data_nascimento_var.get()
    vacina = vacina_var.get()
    alimentacao = alimentacao_var.get()
    outros_cuidados = outros_cuidados_var.get()
    
    ##validação de data
    try:
        datetime.strptime(data_nascimento, '%Y-%m-%d')  # Valida a data
        add_gado(nome, data_nascimento, vacina, alimentacao, outros_cuidados)
        messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
        open_management_screen()  # Abre a tela de gerenciamento
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Use AAAA-MM-DD.")

# Função para exibir dados em uma nova janela
def show_data():
    # Cria uma nova janela
    top = Toplevel()
    top.title("Dados do Gado")

    # Obtém os dados
    df = read_gado()

    # Cria a tabela de visualização
    tree = ttk.Treeview(top, columns=list(df.columns), show='headings')
    tree.pack(fill='both', expand=True)

    # Define as colunas
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='w')

    # Adiciona as linhas
    for index, row in df.iterrows():
        tree.insert('', 'end', values=list(row))

    # Adiciona um botão para fechar a janela
    Button(top, text="Fechar", command=top.destroy).pack(pady=10)

# Função para abrir a tela de gerenciamento
def open_management_screen():
    # Fecha a janela principal
    root.withdraw()

    # Cria uma nova janela para o gerenciamento
    management_window = Toplevel()
    management_window.title("Gerenciamento de Gado")

    Button(management_window, text="Novo Animal", command=lambda: open_registration_screen(management_window)).pack(pady=10)
    Button(management_window, text="Deletar Animal", command=lambda: delete_animal(management_window)).pack(pady=10)
    Button(management_window, text="Atualizar Animal", command=lambda: update_animal(management_window)).pack(pady=10)
    Button(management_window, text="Visualizar Dados", command=show_data).pack(pady=10)
    Button(management_window, text="Sair", command=lambda: exit_app(management_window)).pack(pady=10)

# Função para abrir a tela de registro de novos animais
def open_registration_screen(previous_window):
    previous_window.destroy()
    create_gui()

# Função para deletar um animal
def delete_animal(previous_window):
    # Cria uma nova janela para deletar animal
    delete_window = Toplevel()
    delete_window.title("Deletar Animal")

    Label(delete_window, text="ID do Animal para Deletar:").pack(pady=10)
    delete_id_var = StringVar()
    Entry(delete_window, textvariable=delete_id_var).pack(pady=10)

    def delete_action():
        id = delete_id_var.get()
        if id.isdigit():
            delete_gado(int(id))
            messagebox.showinfo("Sucesso", "Animal deletado com sucesso!")
            delete_window.destroy()
            open_management_screen()
        else:
            messagebox.showerror("Erro", "ID inválido.")

    Button(delete_window, text="Deletar", command=delete_action).pack(pady=10)
    Button(delete_window, text="Cancelar", command=lambda: [delete_window.destroy(), open_management_screen()]).pack(pady=10)

# Função para atualizar um animal
def update_animal(previous_window):
    # Cria uma nova janela para atualizar animal
    update_window = Toplevel()
    update_window.title("Atualizar Animal")

    Label(update_window, text="ID do Animal para Atualizar:").pack(pady=10)
    update_id_var = StringVar()
    Entry(update_window, textvariable=update_id_var).pack(pady=10)

    Label(update_window, text="Novo Nome do Gado:").pack(pady=10)
    new_nome_var = StringVar()
    Entry(update_window, textvariable=new_nome_var).pack(pady=10)

    Label(update_window, text="Nova Data de Nascimento (DD-MM-AAAA):").pack(pady=10)
    new_data_nascimento_var = StringVar()
    Entry(update_window, textvariable=new_data_nascimento_var).pack(pady=10)

    Label(update_window, text="Nova Vacina:").pack(pady=10)
    new_vacina_var = StringVar()
    Entry(update_window, textvariable=new_vacina_var).pack(pady=10)

    Label(update_window, text="Nova Alimentação:").pack(pady=10)
    new_alimentacao_var = StringVar()
    Entry(update_window, textvariable=new_alimentacao_var).pack(pady=10)

    Label(update_window, text="Novos Cuidados:").pack(pady=10)
    new_outros_cuidados_var = StringVar()
    Entry(update_window, textvariable=new_outros_cuidados_var).pack(pady=10)

    def update_action():
        id = update_id_var.get()
        nome = new_nome_var.get()
        data_nascimento = new_data_nascimento_var.get()
        vacina = new_vacina_var.get()
        alimentacao = new_alimentacao_var.get()
        outros_cuidados = new_outros_cuidados_var.get()
        if id.isdigit():
            try:
                datetime.strptime(data_nascimento, '%d-%m-%y')  # Valida a data
                update_gado(int(id), nome, data_nascimento, vacina, alimentacao, outros_cuidados)
                messagebox.showinfo("Sucesso", "Animal atualizado com sucesso!")
                update_window.destroy()
                open_management_screen()
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido. Use AAAA-MM-DD.")
        else:
            messagebox.showerror("Erro", "ID inválido.")

    Button(update_window, text="Atualizar", command=update_action).pack(pady=10)
    Button(update_window, text="Cancelar", command=lambda: [update_window.destroy(), open_management_screen()]).pack(pady=10)

# Função para sair do aplicativo
def exit_app(window):
    window.destroy()
    root.destroy()

# Criação da interface gráfica
def create_gui():
    global nome_var, data_nascimento_var, vacina_var, alimentacao_var, outros_cuidados_var

    # Inicializa a janela principal
    global root
    root = Tk()
    root.title("Cadastro de Gado")

    # Configura o layout da janela
    Label(root, text="Nome do Gado:").grid(row=0, column=0, padx=10, pady=10)
    Label(root, text="Data de Nascimento (AAAA-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
    Label(root, text="Vacina:").grid(row=2, column=0, padx=10, pady=10)
    Label(root, text="Alimentação:").grid(row=3, column=0, padx=10, pady=10)
    Label(root, text="Outros Cuidados:").grid(row=4, column=0, padx=10, pady=10)

    nome_var = StringVar()
    data_nascimento_var = StringVar()
    vacina_var = StringVar()
    alimentacao_var = StringVar()
    outros_cuidados_var = StringVar()

    Entry(root, textvariable=nome_var).grid(row=0, column=1, padx=10, pady=10)
    Entry(root, textvariable=data_nascimento_var).grid(row=1, column=1, padx=10, pady=10)
    Entry(root, textvariable=vacina_var).grid(row=2, column=1, padx=10, pady=10)
    Entry(root, textvariable=alimentacao_var).grid(row=3, column=1, padx=10, pady=10)
    Entry(root, textvariable=outros_cuidados_var).grid(row=4, column=1, padx=10, pady=10)

    Button(root, text="Adicionar Gado", command=submit_data).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

# Executar funções de exemplo
if __name__ == "__main__":
    create_table()  # Cria a tabela se não existir
    create_gui()  # Inicia a interface gráfica
