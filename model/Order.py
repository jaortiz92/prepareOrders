from access.controller import last_id_orders
import pandas as pd
import re
from typing import List, Any, Callable, Dict
from datetime import datetime
from model.RowOrder import RowOrder


class Order:
    request: int = 0

    def __init__(self, file: str, prices, last_id) -> None:
        self.file: str = file
        self.prices = prices
        self.last_id = last_id
        self.request_str()
        self.header()
        self.data()

    def request_str(self) -> str:
        string: str = str(self.request)
        n: int = 5 - len(string)
        self.request_str: str = '0' * n + string
        return self.request_str

    def header(self):
        df_header = pd.read_excel(
            self.file, dtype={'COLOR': str, 'REFERENCIA': str}).iloc[:4]
        i = 17
        try:
            while not isinstance(df_header.iloc[1, i], datetime):
                i += 1
        except:
            print('Error con la fecha en el archivo {}'.format(self.file))

        try:
            self.date: datetime = df_header.iloc[1, i]
            self.month: str = self.date.strftime('%b')
            self.year: int = self.date.year
        except:
            print('Error con la fecha en el archivo {}'.format(self.file))

        try:
            self.customer: str = df_header.columns[4].upper()
        except:
            print('Error con nombre de compañia en el archivo {}'.format(self.file))

        try:
            self.agent: str = df_header.iloc[0, i].upper()
        except:
            print('Error con nombre del vendedor en el archivo {}'.format(self.file))

    def data(self):
        df = pd.read_excel(self.file, header=5, dtype={
                           'COLOR': str, 'REFERENCIA': str}).loc[:, :'TOTAL'].iloc[:-1, :]
        try:
            df_1 = pd.read_excel(self.file, header=5, dtype={
                                 'Estado': str}).loc[:, 'Estado']
        except:
            print('Columna Estado no encontrada en el archivo {}'.format(self.file))

        df = pd.concat([df, df_1], axis=1)
        # just keep correct values
        df = df[df['TOTAL'].apply(is_number)].reset_index(drop=True)
        # Fill nan values
        df['REFERENCIA'].fillna(method='ffill', inplace=True)
        df['COLOR'].fillna('SURTIDO', inplace=True)
        print('Cantidad de filas', df.shape[0])
        self.data = self.select_data(df)

    def select_data(self, df) -> List[RowOrder]:
        RowOrder.id = self.last_id
        start: int = 2
        end: int = df.shape[1] - 2

        list_rows: List[RowOrder] = []
        line = dif_line(df.iloc[0, 0])

        for i in range(df.shape[0]):
            for j in range(start, end):
                if str(df.iloc[i, j]) != 'nan':
                    reference = str(df.iloc[i, 0])
                    color = df.iloc[i, 1]
                    size = str(df.columns[j]).upper()
                    quantity = df.iloc[i, j]
                    status = df.iloc[i, -1]
                    try:
                        df_filter = self.prices[(self.prices['REFERENCIA'] == reference) & (
                            self.prices['TALLAS'] == size)]
                        price = df_filter.iloc[-1, 3]
                        collection = df_filter.iloc[-1, 4]
                        cost = df_filter.iloc[-1, 5]
                    except IndexError as e:
                        print('\tReferencia: {} con talla {}, no se encontro el precio'.format(
                            reference, size))
                        price = 0
                        collection = ''
                        cost = 0

                    RowOrder.id += 1
                    row_order = RowOrder(
                        reference=reference,
                        color=color,
                        size=size,
                        quantity=quantity,
                        line=line,
                        date=self.date,
                        month=self.month,
                        year=self.year,
                        customer=self.customer,
                        request=self.request_str,
                        agent=self.agent,
                        price=price,
                        cost=cost,
                        collection=collection,
                        status=status
                    )
                    list_rows.append(row_order.row())
        self.last_id = RowOrder.id
        return list_rows


def is_number(x: object) -> bool:
    filter_numbre: re = re.compile('^[0-9]+.?[0-9]?$')
    flag: bool = False
    if filter_numbre.match(str(x)) and int(x) > 0:
        flag = True
    return flag


def dif_line(x: object) -> str:
    '''Definir a que linea pertenece el producto'''

    givec = re.compile('[A-Za-z]{2,}[0-9]{2,}.*')
    givec2 = re.compile('[VB][0-9]{3}')
    kyly = re.compile('[0-9]{4,}.*')
    kyly2 = re.compile('M[0-9]{4,}.*')
    tinta = re.compile('[A-Za-z]{3,}.*')
    tinta2 = re.compile('M-[A-Za-z]{2,}')
    x = str(x)
    if givec.match(x) or givec2.match(x):
        line = 'GIVEC'
    elif tinta.match(x) or tinta2.match(x):
        line = 'TINTA STYLE'
    elif kyly.match(x) or kyly2.match(x):
        line = 'GRUPO KYLY'
    else:
        line = 'Otro'
    return line
