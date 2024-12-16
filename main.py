import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from data_loader import load_file
from analysus import show_statistics, show_correlation_matrix
from utils import validate_dataframe
import matplotlib.pyplot as plt

class DataAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicativo de Análise de Dados")
        self.root.geometry("1000x700")

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=5)
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("TCombobox", font=("Helvetica", 12))

        # Variáveis principais
        self.df = None

        # Interface gráfica
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Botões de controle
        self.btn_load = ttk.Button(frame, text="Carregar Arquivo", command=self.load_file)
        self.btn_load.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        self.btn_stats = ttk.Button(frame, text="Exibir Estatísticas", command=self.show_statistics, state="disabled")
        self.btn_stats.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.btn_corr = ttk.Button(frame, text="Matriz de Correlação", command=self.show_correlation_matrix, state="disabled")
        self.btn_corr.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        self.btn_group = ttk.Button(frame, text="Agrupar Colunas", command=self.group_columns, state="disabled")
        self.btn_group.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.btn_plot = ttk.Button(frame, text="Gerar Gráfico", command=self.generate_plot, state="disabled")
        self.btn_plot.grid(row=4, column=0, pady=10, padx=10, sticky="ew")

        # Tabela Treeview para exibição de dados
        self.tree_frame = ttk.Frame(frame)
        self.tree_frame.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbars da tabela
        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscroll=scrollbar_x.set)

        # Configuração de grid para expandir
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5, weight=1)

    def update_treeview(self, data):
        """
        Atualiza a tabela Treeview com os dados do DataFrame.
        """
        # Limpa a tabela existente
        self.tree.delete(*self.tree.get_children())

        # Configura as colunas
        self.tree["columns"] = list(data.columns)
        for col in data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Insere os dados na tabela
        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def load_file(self):
        self.df = load_file()
        if self.df is not None:
            self.update_treeview(self.df.head())  # Mostra as primeiras 5 linhas na tabela
            self.btn_stats["state"] = "normal"
            self.btn_corr["state"] = "normal"
            self.btn_group["state"] = "normal"
            self.btn_plot["state"] = "normal"

    def show_statistics(self):
        if not validate_dataframe(self.df):
            return

        # Número de linhas e colunas
        num_rows, num_cols = self.df.shape

        # Mostra estatísticas
        stats = show_statistics(self.df)  # Retorna as estatísticas como DataFrame
        stats_info = f"Linhas: {num_rows} | Colunas: {num_cols}\n\n" + stats.to_string()

        # Criação da janela de estatísticas
        stats_window = tk.Toplevel()
        stats_window.title("Estatísticas")
        stats_window.geometry("800x600")

        # Exibição do resumo estatístico
        stats_tree = ttk.Treeview(stats_window, show="headings", height=10)
        stats_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        stats_tree["columns"] = stats.columns.tolist()
        for col in stats.columns:
            stats_tree.heading(col, text=col)
            stats_tree.column(col, anchor="center", width=150)

        for _, row in stats.iterrows():
            stats_tree.insert("", "end", values=list(row))

        # Filtros
        filter_frame = ttk.Frame(stats_window)
        filter_frame.pack(pady=10)

        filter_label = ttk.Label(filter_frame, text="Filtrar por coluna e valor:")
        filter_label.grid(row=0, column=0, padx=10, pady=5)

        # Combox de coluna e campo de valor para filtro
        filter_col_var = tk.StringVar()
        filter_col_combo = ttk.Combobox(filter_frame, textvariable=filter_col_var, values=self.df.columns.tolist(), width=25)
        filter_col_combo.grid(row=0, column=1, padx=10, pady=5)

        filter_val_var = tk.StringVar()
        filter_val_entry = ttk.Entry(filter_frame, textvariable=filter_val_var, width=25)
        filter_val_entry.grid(row=0, column=2, padx=10, pady=5)

        def apply_filter():
            filter_col = filter_col_var.get()
            filter_value = filter_val_var.get()

            if not filter_col or not filter_value:
                messagebox.showerror("Erro", "Selecione uma coluna e forneça um valor para filtro!")
                return

            try:
                # Aplica o filtro
                filtered_data = self.df[self.df[filter_col].astype(str) == filter_value]
                if filtered_data.empty:
                    messagebox.showinfo("Resultado", "Nenhuma linha encontrada para esse filtro.")
                else:
                    self.update_treeview(filtered_data)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao aplicar filtro: {str(e)}")

        # Botão para aplicar o filtro
        filter_button = ttk.Button(filter_frame, text="Aplicar Filtro", command=apply_filter)
        filter_button.grid(row=0, column=3, padx=10, pady=5)

        # Opção para exibir determinadas colunas
        column_label = tk.Label(stats_window, text="Escolher colunas para exibir:")
        column_label.pack(pady=10)

        columns_var = tk.StringVar()
        columns_combo = ttk.Combobox(stats_window, textvariable=columns_var, values=self.df.columns.tolist(), state="readonly", width=25)
        columns_combo.pack(pady=5)

        def show_columns_data():
            col = columns_var.get()
            if not col:
                messagebox.showerror("Erro", "Selecione uma coluna para exibir!")
                return
            column_data = self.df[col]
            self.update_treeview(column_data)

        # Botão para exibir dados de colunas
        show_column_button = ttk.Button(stats_window, text="Exibir Coluna", command=show_columns_data)
        show_column_button.pack(pady=10)

    def show_correlation_matrix(self):
        if not validate_dataframe(self.df):
            return
        show_correlation_matrix(self.df)

    def group_columns(self):
        if not validate_dataframe(self.df):
            return
        self.group_columns_window(self.df)

    def group_columns_window(self, df):
        def group_columns():
            # Obtém as colunas selecionadas pelo usuário
            group_by_col = group_col_var.get()
            agg_col = agg_col_var.get()

            # Verifica se o usuário escolheu ambas as colunas
            if not group_by_col or not agg_col:
                messagebox.showerror("Erro", "Por favor, selecione ambas as colunas para agrupar!")
                return

            try:
                # Verifica se as colunas selecionadas são numéricas
                if df[group_by_col].dtype not in ['int64', 'float64'] or df[agg_col].dtype not in ['int64', 'float64']:
                    messagebox.showerror("Erro", "A coluna de agregação deve ser numérica!")
                    return

                # Agrupando os dados pela coluna selecionada
                grouped_df = df.groupby(group_by_col)[agg_col].mean()  # Média como função de agregação
                grouped_df = grouped_df.reset_index()  # Reseta o índice para melhor visualização

                # Exibe o dataframe agrupado
                messagebox.showinfo("Sucesso", f"Dados agrupados por {group_by_col}:\n{grouped_df}")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao agrupar colunas: {str(e)}")

        # Criação da janela de agrupamento de colunas
        window = tk.Toplevel()
        window.title("Agrupar Colunas")

        # Label informando sobre a seleção da coluna
        label = tk.Label(window, text="Selecione a coluna para agrupar:")
        label.pack(pady=10)

        # Criação de um combo box com as colunas do dataframe
        group_col_var = tk.StringVar()
        group_col_combo = ttk.Combobox(window, textvariable=group_col_var, values=df.columns.tolist())
        group_col_combo.pack(pady=10)
        group_col_combo.set("")

        label_agg = tk.Label(window, text="Selecione a coluna para agregação:")
        label_agg.pack(pady=10)

        # Coluna para a função de agregação
        agg_col_var = tk.StringVar()
        agg_col_combo = ttk.Combobox(window, textvariable=agg_col_var, values=df.columns.tolist())
        agg_col_combo.pack(pady=10)
        agg_col_combo.set("")

        # Botão para aplicar o agrupamento
        btn_group_apply = ttk.Button(window, text="Agrupar", command=group_columns)
        btn_group_apply.pack(pady=10)

    def generate_plot(self):
        if not validate_dataframe(self.df):
            return
        # Exemplo de gráfico
        self.df.hist(figsize=(10, 6))
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalyzerApp(root)
    root.mainloop()
