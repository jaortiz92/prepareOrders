import pandas as pd
import numpy as np
from model.Order import Order
from model.RowOrder import RowOrder
from model.JoinPrices import JoinPrices
from access.controller import insert_rows_orders, init_file
import os
import re


class ServicesAddNewOrders:
    PATH = './files/'

    def __init__(self):
        prices = self.generate_prices()
        final_data = self.generate_data(pd.DataFrame(prices))
        df = pd.DataFrame(final_data)
        df['ESTADO'] = df['ESTADO'].apply(self.change_status)
        self.save_file(df)

    def change_status(self, x):
        result = x
        if str(x) == '1':
            result = '15/08/2021'
        elif str(x) == '2':
            result = '30/08/2021'
        elif str(x) == '3':
            result = 'Pte x Existencia'
        return result

    def generate_prices(self):
        prices = JoinPrices('Consolidado_precios.xlsx')
        prices.save('Precios_Kyly')
        prices = prices.data
        return prices

    def generate_data(self, prices):
        files = os.listdir(self.PATH)
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
            data = Order(self.PATH + files_order[i], prices)
            list_total.extend(data.data)
        return list_total

    def save_file(self, data):
        writer = pd.ExcelWriter('Ordenes_unidas.xlsx',
                                datetime_format='dd-mm-yy')
        data.to_excel(writer, index=False)
        writer.save()
        writer = None


class ServicesPandasOrders():
    def __init__(self, df) -> None:
        init_file()
        self.init_process(df)

    def init_process(self, df) -> None:
        list_rows = []

        for i in range(df.shape[0]):

            if isinstance(df['FECHA'][i], pd.Timestamp):
                date = df['FECHA'][i].strftime('%Y-%m-%d %X')
            else:
                date = ''

            row_order = RowOrder(
                id=df['ID'][i],
                reference=df['REFERENCIA'][i],
                color=df['COLOR'][i],
                size=df['TALLAS'][i],
                quantity=df['CANTIDAD'][i],
                line=df['LINEA'][i],
                date=date,
                month=df['MES'][i],
                year=df['AÑO'][i],
                customer=df['CLIENTE'][i],
                request=df['PEDIDO #'][i],
                agent=df['VENDEDOR'][i],
                price=df['PRECIO UND'][i],
                cost=df['COSTO'][i],
                collection=df['COLECCIÓN'][i],
                status=df['ESTADO'][i]
            ).row()
            list_rows.append(row_order)

        insert_rows_orders(list_rows)


class ServicesAddFileOrders(ServicesPandasOrders):
    def __init__(self, nane_file) -> None:
        df = pd.read_excel(nane_file,
                           sheet_name='BASE', dtype={'PEDIDO #': str, 'AÑO': str, 'TALLAS': str})

        super().__init__(df)
