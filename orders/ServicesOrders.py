# import pdb
import pandas as pd
from orders.utils import JoinOrder
from orders.utils import JoinPrices
# from access.controller import *
from orders.utils.utils import *
import os
import re

COLUMNS = ['ID', 'FECHA', 'MES', 'AÑO', 'CLIENTE', 'PEDIDO #',
           'REFERENCIA', 'COLOR', 'TALLAS', 'CANTIDAD', 'PRECIO UND',
           'PRECIO TOTAL', 'LINEA', 'MARCA', 'COLECCIÓN', 'VENDEDOR',
           'COSTO', 'COSTO TOTAL', 'ESTADO']
PATH_NEW_ORDERS = './files/'
NAME_FILE_ORDERS = 'Ordenes.xlsx'
NAME_FILE_QUERIES = 'Consulta.xlsx'


class ServicesAddNewOrders:
    def __init__(self):
        prices = self.generate_prices()
        self.data = self.generate_data(pd.DataFrame(prices))

    def generate_prices(self):
        prices = JoinPrices('Consolidado_precios.xlsx')
        prices.save('Precios_Kyly')
        prices = prices.data
        return prices

    def generate_data(self, prices):
        files = os.listdir(PATH_NEW_ORDERS)
        files_order = {}
        extract = re.compile('^([0-9]+).*')
        for file in files:
            file_match = extract.match(file)
            if file_match:
                files_order[int(file_match.group(1)) - 1] = file
        list_total = []

        for file in files_order.values():
            data = JoinOrder(PATH_NEW_ORDERS, file, prices)
            list_total.append(data.data)
        return list_total


class ServicesReadPivot():

    def __init__(self, orders, products) -> None:
        self.df = pd.DataFrame(
            products).astype(dtype={'id_order_id': str, 'reference': str, 'color': str})
        self.init_process()
        self.df_orders = pd.DataFrame(orders).astype(dtype={'id_order': str})

    def init_process(self) -> None:
        df = pd.pivot_table(self.df, values=['quantity'], index=[
                            'id_order_id', 'reference', 'color'], columns=['size'], aggfunc=sum)

        df.columns = df.columns.droplevel()
        list_sizes = sort_sizes(df.columns)
        df = df[list_sizes]
        df = df.reset_index()
        df = df.sort_values(
            ['id_order_id', 'reference', 'color'])
        # Change nan for "" before it was for 0
        df = df.fillna("")
        df['total'] = df.iloc[:, 3:].sum(axis=1)
        df.rename(columns={
            'id_order_id': 'ID Pedido',
            'reference': 'Referencia',
            'color': 'Color',
            'total': 'Total'
        }, inplace=True)
        self.df = df

    def data(self):
        data = []
        for order in pd.unique(self.df_orders['id_order']):
            data.append({
                'order': self.df_orders[self.df_orders['id_order'] == order].to_dict(orient='records'),
                'products_order': self.df[self.df['ID Pedido'] == order].to_dict(orient='records'),
                'columns': self.df.columns
            })
        return data


class ServicesReadPivotSize():
    def __init__(self, products) -> None:
        self.df = pd.DataFrame(
            products).astype(dtype={'id_order_id': str, 'reference': str, 'color': str})
        self.init_process()

    def init_process(self) -> None:
        df = pd.pivot_table(self.df, values=['quantity'], index=[
                            'line', 'brand'], columns=['size'], aggfunc=sum)

        df.columns = df.columns.droplevel()
        list_sizes = sort_sizes(df.columns)
        df = df[list_sizes]
        df = df.reset_index()
        df = df.sort_values(
            ['line', 'brand'])
        df = df.fillna(0)
        df['total'] = df.iloc[:, 3:].sum(axis=1)
        df.rename(columns={
            'line': 'Linea',
            'brand': 'Marca',
            'total': 'Total'
        }, inplace=True)
        self.df = df

    def data(self):
        data = []
        for line in pd.unique(self.df['Linea']):
            data.append({
                'line': line,
                'products_order': self.df[self.df['Linea'] == line].iloc[:, 1:].to_dict(orient='records'),
                'columns': self.df.columns[1:]
            })
        return data