# software-de-analise-de-dados

Este código implementa um aplicativo de análise de dados utilizando o `tkinter` para a interface gráfica e o `pandas` para o processamento de dados. A seguir, explico as funcionalidades e estrutura do código em detalhes, dividindo-o em suas partes principais.

### Parte 1: Estrutura da Interface Gráfica e Funcionalidades Principais

#### 1. **Classe `DataAnalyzerApp`**:
   - **Inicialização**: A classe `DataAnalyzerApp` define o aplicativo de análise de dados. Ela é inicializada com um objeto `root`, que é a janela principal do Tkinter.
     - O título da janela é definido como "Aplicativo de Análise de Dados".
     - As dimensões da janela são configuradas para 1000x700 pixels.
     - O estilo do aplicativo é personalizado, ajustando fontes, padding e cores para os botões, rótulos e a árvore de dados.

#### 2. **Widgets da Interface**:
   - **Botões de controle**: São criados cinco botões principais para interagir com o aplicativo:
     - **Carregar Arquivo**: Permite ao usuário carregar um arquivo de dados.
     - **Exibir Estatísticas**: Exibe estatísticas do DataFrame carregado.
     - **Matriz de Correlação**: Exibe a matriz de correlação das colunas numéricas.
     - **Agrupar Colunas**: Permite ao usuário agrupar dados por uma coluna e aplicar uma agregação.
     - **Gerar Gráfico**: Cria gráficos a partir dos dados.
   - Todos esses botões inicialmente são desabilitados, exceto o de "Carregar Arquivo", para garantir que o usuário carregue um arquivo antes de realizar qualquer análise.
![ana1](https://github.com/user-attachments/assets/6fa7b9d9-ce66-44c9-937f-c7efb06d9ffd)

   - **Tabela `Treeview`**: Uma tabela de visualização é configurada para exibir os dados do DataFrame carregado. É usada a widget `Treeview` do Tkinter, que permite uma visualização de dados estruturados em formato tabular.
     - Além disso, são adicionados `scrollbars` horizontais e verticais para permitir a navegação pelos dados.


#### 3. **Métodos Principais**:
   - **`update_treeview(data)`**: Atualiza a tabela com os dados fornecidos. Limpa a tabela antes de preencher com novos dados e ajusta as colunas conforme o DataFrame.
   - **`load_file()`**: Usa a função `load_file` (definida na parte 2) para carregar o arquivo de dados e atualiza a interface com as primeiras 5 linhas do DataFrame.
   - **`show_statistics()`**: Exibe as estatísticas descritivas dos dados, incluindo o número de linhas, colunas e valores ausentes.
     - A interface também permite aplicar filtros aos dados com base nas colunas.
   - **`show_correlation_matrix()`**: Exibe a matriz de correlação entre as colunas numéricas do DataFrame. A correlação é visualizada em um gráfico de calor (heatmap) usando `seaborn` e `matplotlib`.
   - **`group_columns()`**: Permite ao usuário agrupar os dados por uma coluna e aplicar uma agregação (média) a outra coluna.
   - **`generate_plot()`**: Gera um gráfico de histograma com base no DataFrame usando `matplotlib`.

### Parte 2: Carregamento de Arquivos

#### Função `load_file()`:
   - **Objetivo**: Carregar um arquivo de dados (CSV, Excel ou JSON) selecionado pelo usuário.
   - **Processo**:
     - Usa a `filedialog.askopenfilename()` para abrir uma janela de seleção de arquivo.
     - Dependendo da extensão do arquivo, os dados são carregados em um DataFrame utilizando o `pandas` (`read_csv`, `read_excel`, ou `read_json`).
     - Se o formato não for suportado ou ocorrer um erro no carregamento, uma mensagem de erro é exibida.
![ana2](https://github.com/user-attachments/assets/c1936041-0847-481e-b546-a548d09d32cd)

### Parte 3: Processamento de Dados

#### Funções de Análise:
   - **`show_statistics(df)`**: Exibe as estatísticas descritivas de um DataFrame, como contagem, média, desvio padrão, etc., e também a quantidade de valores ausentes.
   - ![ana3](https://github.com/user-attachments/assets/b99bd54b-3572-4452-9984-fbbb4eb21c6b)

   - **`show_correlation_matrix(df)`**: Exibe a matriz de correlação entre as colunas numéricas do DataFrame usando o `seaborn` para criar um heatmap.
   - ![ana4](https://github.com/user-attachments/assets/15e7e04b-a03d-49f4-80c5-8c1f2d0915d9)

   
   Ambas as funções recebem um `DataFrame` como entrada, e retornam ou exibem os resultados processados de forma gráfica ou tabular.

### Parte 4: Validação e Exibição de Mensagens

#### Funções Auxiliares:
   - **`show_message(title, message, type)`**: Exibe mensagens de alerta ou informação. A função usa a `messagebox` do Tkinter e pode exibir diferentes tipos de mensagens, como "info", "warning", ou "error".
   - **`validate_dataframe(df)`**: Verifica se o DataFrame carregado não está vazio e se contém dados válidos para análise. Caso contrário, exibe uma mensagem de erro.
   - ![ana5](https://github.com/user-attachments/assets/ba2227b7-0e97-4739-ba02-6b671682933b)

   - **`get_numeric_columns(df)`**: Retorna uma lista das colunas numéricas do DataFrame, usadas, por exemplo, na geração da matriz de correlação.
   - ![ana6](https://github.com/user-attachments/assets/eb56163d-653c-43da-85ef-8b841ef27290)


### Conclusão

Este aplicativo oferece uma interface gráfica simples e interativa para carregar, analisar e visualizar dados em formatos CSV, Excel e JSON. Ele integra funcionalidades de análise estatística e visualização, além de permitir operações como agrupamento e aplicação de filtros. É uma solução bastante útil para usuários que desejam explorar dados de maneira intuitiva e sem a necessidade de código complexo.
