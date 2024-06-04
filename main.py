import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import seaborn as sns
import matplotlib.pyplot as plt

page_url = 'https://www.mercadolivre.com.br/ofertas#c_id=/home/promotions-recommendations'


def main():
    res = req.get(page_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    products = [
        {
            "name": item.select_one(".promotion-item__title").text,
            "price": f"R$ {item.select_one(".andes-money-amount__fraction").text}",
            "discount": int(
                item.select_one(".promotion-item__discount-text").text.split()[0].strip("%")) if item.select_one(
                ".promotion-item__discount-text") else 0,
            "url": item.select_one("a")['href']
        }
        for item in soup.select(".promotion-item")
        if int(item.select_one(".promotion-item__discount-text").text.split()[0].strip("%")) >= 15
    ]

    if products:
        df = pd.DataFrame(products)
        df.sort_values(["name", "discount"], inplace=True)

        df.to_csv("output/descontos.csv", index=False)
        df.to_excel("output/descontos.xlsx", index=False, sheet_name="Produtos")

        plt.figure(figsize=(8, 6))
        sns.boxplot(
            x="discount",
            showmeans=True,
            data=df
        )

        plt.title("Distribuição de descontos no Mercado Livre")
        plt.xlabel("Desconto (%)")
        plt.ylabel("Frequência")
        plt.grid(axis='y')

        plt.show()


main()