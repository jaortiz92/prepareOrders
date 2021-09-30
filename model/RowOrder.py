import pandas as pd
import re
from typing import List, Any, Callable, Dict
from datetime import datetime
import numpy as np


class RowOrder():
    id = 0

    def __init__(self, reference: str, color: str, size: str, quantity: int, line: str, date: datetime, month: str, year: int,
                 customer: str, request: str, agent: str, price: int, cost: int, collection: str, status: str, id: int = None) -> None:
        self.reference: str = reference
        self.color: str = color
        self.size: str = size
        self.quantity: int = int(quantity)
        self.line: str = line
        self.brand: str = self.dif_brand()
        self.date: datetime = date
        self.customer: str = customer
        self.request: str = request
        self.agent: str = agent
        self.month: str = month
        self.year: int = int(year)
        self.collection: str = collection
        self.status: str = status
        if id:
            self.id = id
        if not np.isnan(price):
            self.price: int = int(price)
        else:
            self.price: int = 0
        if not np.isnan(cost):
            self.cost: int = int(cost)
        else:
            self.cost: int = 0

    def row(self) -> Dict[str, Any]:
        row = {
            'ID': int(self.id),
            'FECHA': self.date,
            'MES': self.month,
            'AÑO': self.year,
            'CLIENTE': self.customer,
            'PEDIDO #': self.request,
            'REFERENCIA': self.reference,
            'COLOR': self.color,
            'TALLAS': self.size,
            'CANTIDAD': self.quantity,
            'PRECIO UND': self.price,
            'PRECIO TOTAL': self.price * self.quantity,
            'LINEA': self.line,
            'MARCA': self.brand,
            'COLECCIÓN': self.collection,
            'VENDEDOR': self.agent,
            'COSTO': self.cost,
            'COSTO TOTAL': self.cost * self.quantity,
            'ESTADO': self.status
        }
        return row

    def dif_brand(self):
        codigo = str(self.reference)

        if self.line == 'GIVEC':
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
        elif self.line == 'GRUPO KYLY':
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
        elif self.line == 'TINTA STYLE':
            result = 'TINTA STYLE'
        else:
            result = 'Otro'
        return result

    def __str__(self) -> str:
        return str(self.row())
