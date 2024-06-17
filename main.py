# Importações das bibliotecas necessárias
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Definindo URL da página
page_url = "https://www.mercadolivre.com.br/ofertas#c_id=/home/promotions-recommendations"

# Declarando função principal
def main():
    # Requisitando conteúdo HTML da url definida
    res = req.get(page_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # Criando lista de produtos
    products = [
        # Modelo do dict de cada item
        {
            "name": item.select_one(".promotion-item__title").text,
            "price": f"R$ {item.select_one(".andes-money-amount__fraction").text}",
            "discount": int(
                item.select_one(".promotion-item__discount-text").text.split()[0].strip("%")) if item.select_one(
                ".promotion-item__discount-text") else 0,
            "url": item.select_one("a")['href']
        }
        # Iterando por elementos e adicionando seu respectivo conteúdo ao dict
        for item in soup.select(".promotion-item")
        # Filtrando elementos que possuem o desconto menor que 15
        if int(item.select_one(".promotion-item__discount-text").text.split()[0].strip("%")) >= 15
    ]

    # Processamento dos dados coletados
    if products:
        RenderData(products)



#Definindo função do processamento dos dados coletados
def RenderData(products):
    # Criando DataFrame usando pandas
    df = pd.DataFrame(products)
    df.sort_values(["name", "discount"], inplace=True)

    # Exportando dados para arquivo .csv e .xlsx (Excel) no diretório './output'
    df.to_csv("output/descontos.csv", index=False)
    df.to_excel("output/descontos.xlsx", index=False, sheet_name="Produtos")

    # Calculando Q's, Mediana e Média
    qs = np.percentile(df['discount'].dropna(), [25, 50, 75])
    median = np.median(df['discount'])
    mean = df['discount'].mean()

    # Criando boxplot com os dados armazenados no DataFrame
    plt.figure(figsize=(8, 6))
    # Criando boxplot com os dados do DataFrame
    sns.boxplot(df["discount"])

    # Adicionando marcação dos cálculos feitos anteriormente
    plt.text(0.1, mean, f'Média: {mean:.2f}%', horizontalalignment='center', color='blue', weight='semibold')
    plt.text(0.1, median, f'Mediana: {median:.2f}%', horizontalalignment='center', color='yellow', weight='semibold')
    plt.text(0.5, qs[0], f'Q1: {qs[0]:.2f}%', horizontalalignment='center', color='red', weight='semibold')
    plt.text(0.5, qs[1], f'Q2: {qs[1]:.2f}%', horizontalalignment='center', color='purple', weight='semibold')
    plt.text(0.5, qs[2], f'Q3: {qs[2]:.2f}%', horizontalalignment='center', color='orange', weight='semibold')

    # Definindo configuração da boxplot
    plt.title("Distribuição de descontos no Mercado Livre")
    plt.ylabel("Desconto (%)")
    plt.xlabel("Frequência")
    plt.grid(axis='y')

    plt.show()


main()
