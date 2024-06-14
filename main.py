import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import seaborn as sns
import matplotlib.pyplot as plt

# Definir URL da página que o conteúdo seja obtido
page_url = 'https://www.mercadolivre.com.br/ofertas#c_id=/home/promotions-recommendations'

def main():
    # Obter o conteúdo da página da web
    res = req.get(page_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # Extrair dados de produtos com descontos de 15% ou mais
    products = [
        {
            "name": item.select_one(".promotion-item__title").text,
            "price": f"R$ {item.select_one('.andes-money-amount__fraction').text}",
            "discount": int(item.select_one(".promotion-item__discount-text").text.split()[0].strip("%")) if item.select_one(".promotion-item__discount-text") else 0,
            "url": item.select_one("a")['href']
        }
        # Mapear elementos que possuem a classe 'promotion-item' e adicionar seu dict à lista caso o valor de desconto seja maior que 15
        for item in soup.select(".promotion-item")
        if int(item.select_one(".promotion-item__discount-text").text.split()[0].strip("%")) >= 15
    ]

    # Processar e salvar dados
    if products:
        df = pd.DataFrame(products)
        df.sort_values(["name", "discount"], inplace=True)
        
        # Criar arquivos CSV e Excel
        df.to_csv("output/descontos.csv", index=False)
        df.to_excel("output/descontos.xlsx", index=False, sheet_name="Produtos")

        # Criar um boxplot para visualizar a distribuição de descontos
        plt.figure(figsize=(8, 6))
        sns.boxplot(
            x="discount",
            showmeans=True,
            data=df
        )

        plt.title("Distribuição de Descontos no Mercado Livre")
        plt.xlabel("Desconto (%)")
        plt.ylabel("Frequência")
        plt.grid(axis='y')

        plt.show()



main()
