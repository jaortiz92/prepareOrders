import pandas as pd
import re
from typing import List, Any, Callable, Dict
from datetime import datetime


class JoinOrder:

    def __init__(self, PATH, file: str, prices) -> None:
        self.file: str = file
        self.filePATH = PATH + file
        self.prices = prices
        self.data = {
            'order': self.header(),
            'productsOrder': self.body()
        }

    def header(self):
        df_header = pd.read_excel(
            self.filePATH, dtype={'COLOR': str, 'REFERENCIA': str}).iloc[:4]
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

        return {
            'date': self.date,
            'customer': self.customer,
            'agent': self.agent,
            'file_name': self.file
        }

    def body(self):
        df = pd.read_excel(self.filePATH, header=5, dtype={
                           'COLOR': str, 'REFERENCIA': str}).loc[:, :'TOTAL'].iloc[:-1, :]
        try:
            df_1 = pd.read_excel(self.filePATH, header=5, dtype={
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
        return self.select_data(df)

    def select_data(self, df):
        start: int = 2
        end: int = df.shape[1] - 2

        list_rows = []
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

                    row_order = {
                        'reference': reference,
                        'color': color,
                        'size': size,
                        'quantity': quantity,
                        'line': line,
                        'brand': dif_brand(reference, line),
                        'price': price,
                        'total_price': price * quantity,
                        'cost': cost,
                        'total_cost': cost * quantity,
                        'collection': collection,
                        'status': status
                    }
                    list_rows.append(row_order)
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


def dif_brand(reference, line):
    codigo = str(reference)

    if line == 'GIVEC':
        bagoraz = re.compile('[(BA)(TB)]')
        kalisson = re.compile('[(DI)(KA)]')
        le_cabestan = re.compile('[(LC)]')

        if bagoraz.match(codigo):
            result = 'BAGORAZ'
        elif kalisson.match(codigo):
            result = 'KALISSON'
        elif le_cabestan.match(codigo):
            result = 'LE CABESTAN'
        else:
            result = 'Otro'
    elif line == 'GRUPO KYLY':
        kyly = re.compile('[0-9]{6}')
        nanai = re.compile('60[0-9]{4}')
        lemon = re.compile('8[0-9]{4}')
        amora = re.compile('5[0-9]{4}')
        millon = re.compile('1[0-9]{4}')
        millon2 = re.compile('[0-9]{4}')
        millon3 = re.compile("M[0-9]{4,}.*")

        if nanai.match(codigo):
            result = 'NANAI'
        elif kyly.match(codigo):
            result = 'KYLY'
        elif lemon.match(codigo):
            result = 'LEMON'
        elif amora.match(codigo):
            result = 'AMORA'
        elif millon.match(codigo) or millon2.match(codigo) or millon3.match(codigo):
            result = 'MILLON'
        else:
            result = 'Otro'
    elif line == 'TINTA STYLE':
        result = 'TINTA STYLE'
    else:
        result = 'Otro'
    return result
