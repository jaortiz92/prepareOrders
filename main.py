import os
import pandas as pd
from Order import Order
from JoinPrices import JoinPrices

PATH = './files/'


def run():
    prices = generate_prices()
    final_data = generate_data(pd.DataFrame(prices))
    save_file(pd.DataFrame(final_data))


def generate_prices():
    prices = JoinPrices('Consolidado_precios.xlsx')
    prices.save('Precios_Kyly')
    prices = prices.data
    return prices


def generate_data(prices):
    files = os.listdir(PATH)
    list_total = []
    Order.request = 93
    for file in files:
        Order.request += 1
        print(file)
        data = Order(PATH + file, prices)
        list_total.extend(data.data)
    return list_total


def save_file(data):
    writer = pd.ExcelWriter('Ordenes_unidas.xlsx', datetime_format='dd-mm-yy')
    data.to_excel(writer, index=False)
    writer.save()
    writer = None


if __name__ == '__main__':
    run()
