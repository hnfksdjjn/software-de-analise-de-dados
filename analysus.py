import pandas as pd

def show_statistics(df):
    """
    Retorna as estatísticas descritivas de um DataFrame.
    """
    if df is None or df.empty:
        raise ValueError("O DataFrame está vazio ou não foi carregado.")
    stats = df.describe().transpose()  # Transforma para facilitar a visualização
    stats["missing_values"] = df.isnull().sum()  # Adiciona contagem de valores ausentes
    return stats.reset_index().rename(columns={"index": "Column"})

def show_correlation_matrix(df):
    """
    Exibe a matriz de correlação de um DataFrame.
    Somente colunas numéricas são consideradas.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    if df is None or df.empty:
        raise ValueError("O DataFrame está vazio ou não foi carregado.")
    numeric_cols = df.select_dtypes(include=["float", "int"])
    if numeric_cols.empty:
        raise ValueError("O DataFrame não contém colunas numéricas.")
    correlation_matrix = numeric_cols.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de Correlação")
    plt.show()
