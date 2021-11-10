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
        extract = re.compile('([0-9]+).*')
        for file in files:
            file_match = extract.match(file)
            files_order[int(file_match.group(1)) - 1] = file

        list_total = []

        for file in files_order.values():
            print(file)
            data = JoinOrder(PATH_NEW_ORDERS, file, prices)
            list_total.append(data.data)
        return list_total


class ServicesAddPandasOrders():
    def __init__(self, df) -> None:
        # init_file()
        self.init_process(df)

    def init_process(self, df) -> None:
        list_rows = []
        for i in range(df.shape[0]):

            if isinstance(df['FECHA'][i], pd.Timestamp):
                date = df['FECHA'][i].strftime('%Y-%m-%d %X')
            elif isinstance(df['FECHA'][i], str):
                date = df['FECHA'][i]
            else:
                date = ''

            # row_order = RowOrder(
            #     id=df['ID'][i],
            #     reference=df['REFERENCIA'][i],
            #     color=df['COLOR'][i],
            #     size=df['TALLAS'][i],
            #     quantity=df['CANTIDAD'][i],
            #     line=df['LINEA'][i],
            #     date=date,
            #     month=df['MES'][i],
            #     year=df['AÑO'][i],
            #     customer=df['CLIENTE'][i],
            #     request=df['PEDIDO #'][i],
            #     agent=df['VENDEDOR'][i],
            #     price=df['PRECIO UND'][i],
            #     cost=df['COSTO'][i],
            #     collection=df['COLECCIÓN'][i],
            #     status=df['ESTADO'][i]
            # ).row()
            # list_rows.append(row_order)

        # insert_rows_orders(list_rows)


class ServicesAddFileOrdersOrigin(ServicesAddPandasOrders):
    def __init__(self, nane_file) -> None:
        df = pd.read_excel(nane_file,
                           sheet_name='BASE', dtype={'PEDIDO #': str, 'TALLAS': str,  'COLOR': str})

        super().__init__(df)


class ServicesAddFileOrders(ServicesAddPandasOrders):
    def __init__(self, nane_file) -> None:
        df = pd.read_excel(nane_file, dtype={
                           'PEDIDO #': str, 'TALLAS': str, 'COLOR': str})
        min_value = min(df['ID'])
        max_value = max(df['ID'])
        # delete_range(min_value=min_value, max_value=max_value)
        super().__init__(df)


class ServicesReadOrders():

    def __init__(self, date=None) -> None:
        self.init_process(date)

    def init_process(self, date) -> None:
        # self.df = pd.DataFrame(read_all_orders(date), columns=COLUMNS)
        # save_file(self.df, NAME_FILE_ORDERS)
        pass


class ServicesDeleteRange():
    def __init__(self, min_value, max_value) -> None:
        # delete_range(min_value=min_value, max_value=max_value)
        pass


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
        df = df.fillna(0)
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
