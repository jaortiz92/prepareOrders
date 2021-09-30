import pandas as pd
import numpy as np
from model.Order import Order
from model.RowOrder import RowOrder
from model.JoinPrices import JoinPrices
from access.controller import *
import os
import re

COLUMNS = ['ID', 'FECHA', 'MES', 'AÑO', 'CLIENTE', 'PEDIDO #',
           'REFERENCIA', 'COLOR', 'TALLAS', 'CANTIDAD', 'PRECIO UND',
           'PRECIO TOTAL', 'LINEA', 'MARCA', 'COLECCIÓN', 'VENDEDOR',
           'COSTO', 'COSTO TOTAL', 'ESTADO']
PATH_NEW_ORDERS = './files/'


def save_file(data: pd.DataFrame):
    writer = pd.ExcelWriter('Ordenes.xlsx',
                            datetime_format='dd-mm-yy')
    data.to_excel(writer, index=False, sheet_name='Data')
    writer.save()
    writer = None


class ServicesAddNewOrders:
    def __init__(self):
        last_id = last_id_orders()
        prices = self.generate_prices()
        final_data = self.generate_data(pd.DataFrame(prices), last_id)
        df = pd.DataFrame(final_data)
        df['ESTADO'] = df['ESTADO'].apply(self.change_status)
        ServicesPandasOrders(df)
        save_file(df)

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

    def generate_data(self, prices, last_id):
        files = os.listdir(PATH_NEW_ORDERS)
        files_order = {}
        extract = re.compile('([0-9]+).*')
        for file in files:
            file_match = extract.match(file)
            files_order[int(file_match.group(1)) - 1] = file

        list_total = []
        Order.request = int(last_number_order())

        for i in range(len(files_order)):
            Order.request += 1
            print(files_order[i])
            data = Order(PATH_NEW_ORDERS + files_order[i], prices, last_id)
            last_id = data.last_id
            list_total.extend(data.data)
        return list_total


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
                           sheet_name='BASE', dtype={'PEDIDO #': str, 'TALLAS': str})

        super().__init__(df)


class ServicesReadOrders():

    def __init__(self, date=None) -> None:
        self.init_process(date)

    def init_process(self, date):
        self.df = pd.DataFrame(read_all_orders(date), columns=COLUMNS)
        save_file(self.df)