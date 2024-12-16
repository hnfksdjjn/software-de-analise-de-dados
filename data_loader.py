from tkinter import filedialog, messagebox
import pandas as pd

def load_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("JSON files", "*.json")]
    )
    if not file_path:
        return None

    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path)
        elif file_path.endswith(".json"):
            return pd.read_json(file_path)
        else:
            messagebox.showerror("Erro", "Formato de arquivo não suportado!")
            return None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")
        return None
