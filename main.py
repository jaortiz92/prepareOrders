import os
import pandas as pd
from model.JoinPrices import JoinPrices
from model.Order import Order
import re
import os

PATH = './files/'


def run():
    prices = generate_prices()
    final_data = generate_data(pd.DataFrame(prices))
    df = pd.DataFrame(final_data)
    df['ESTADO'] = df['ESTADO'].apply(change_status)
    save_file(df)


def change_status(x):
    result = x
    if str(x) == '1':
        result = '15/08/2021'
    elif str(x) == '2':
        result = '30/08/2021'
    elif str(x) == '3':
        result = 'Pte x Existencia'
    return result


def generate_prices():
    prices = JoinPrices('Consolidado_precios.xlsx')
    prices.save('Precios_Kyly')
    prices = prices.data
    return prices


def generate_data(prices):
    files = os.listdir(PATH)
    files_order = {}
    extract = re.compile('([0-9]+).*')
    for file in files:
        file_match = extract.match(file)
        files_order[int(file_match.group(1)) - 1] = file

    list_total = []

    while(Order.request == 0):
        last_request = input('Ingrese numero del ultimo pedido: ')
        if last_request.isnumeric():
            Order.request = int(last_request)

    for i in range(len(files_order)):
        Order.request += 1
        print(files_order[i])
        data = Order(PATH + files_order[i], prices)
        list_total.extend(data.data)
    return list_total


def save_file(data):
    writer = pd.ExcelWriter('Ordenes_unidas.xlsx', datetime_format='dd-mm-yy')
    data.to_excel(writer, index=False)
    writer.save()
    writer = None


if __name__ == '__main__':
    run()
