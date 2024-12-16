from tkinter import messagebox

def show_message(title, message, type="info"):
    """
    Exibe uma mensagem de alerta ou informação na interface gráfica.

    Args:
        title (str): Título da mensagem.
        message (str): Texto da mensagem.
        type (str): Tipo da mensagem: "info", "warning", ou "error".
    """
    if type == "info":
        messagebox.showinfo(title, message)
    elif type == "warning":
        messagebox.showwarning(title, message)
    elif type == "error":
        messagebox.showerror(title, message)

def validate_dataframe(df):
    """
    Verifica se um DataFrame é válido para análise.

    Args:
        df (pandas.DataFrame): DataFrame a ser validado.

    Returns:
        bool: True se válido, False caso contrário.
    """
    if df is None or df.empty:
        show_message("Erro", "Nenhum dado carregado ou o arquivo está vazio!", "error")
        return False
    return True

def get_numeric_columns(df):
    """
    Retorna uma lista de colunas numéricas de um DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame para extração de colunas.

    Returns:
        list: Lista de nomes de colunas numéricas.
    """
    return df.select_dtypes(include=["float", "int"]).columns.tolist()
