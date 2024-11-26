import pandas as pd
import os

input_csv = "../dados/brutos/BD_Logistica.csv"  # Entrada
output_csv = "../dados/tratados/logistica.csv"  # Saída

# Verificar se o arquivo de entrada existe
if not os.path.exists(input_csv):
    print(f"Erro: O arquivo {input_csv} não foi encontrado.")
    exit()

# Carrega o dataset
df = pd.read_csv(input_csv)

# Converte colunas de datas para datetime
for col in ["Data Emissão Pedido", "Data Entrega Prevista", "Saída para Entrega", "Data Entrega Real"]:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Ajusta a coluna de faturamento para decimal com vírgula, arredonda para 2 casas decimais e formata como moeda
df["R$ Faturados"] = (
    df["R$ Faturados"]
    .astype(str)  # Garante que os valores sejam strings
    .str.replace(",", ".", regex=False)  # Substitui vírgulas por pontos
    .astype(float)  # Converte para float (decimal)
    .round(2)  # Arredonda para 2 casas decimais
    .apply(lambda x: f"{x:,.2f}".replace(",", "x").replace(".", ",").replace("x", "."))  # Formata com vírgula
)

# Separa a coluna "Cliente - Motorista" em duas colunas
df[['Cliente', 'Motorista']] = df["Cliente - Motorista"].str.split("-", expand=True)

# Cria novas métricas
df["Atraso (dias)"] = (df["Data Entrega Real"] - df["Data Entrega Prevista"]).dt.days
df["Entrega no Prazo"] = df["Atraso (dias)"].apply(lambda x: "Sim" if x <= 0 else "Não")

# Remove a coluna original "Cliente - Motorista"
df.drop(columns=["Cliente - Motorista"], inplace=True)

# Salva os dados tratados mantendo as colunas originais e as novas métricas
output_dir = os.path.dirname(output_csv)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df.to_csv(output_csv, index=False, sep=',')

print(f"Dados tratados salvos em: {output_csv}")
