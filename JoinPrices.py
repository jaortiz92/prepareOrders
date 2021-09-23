import pandas as pd
import re
from typing import List, Any, Callable, Dict
from Prices import Prices


class JoinPrices:
    def __init__(self, file):
        self.file = file
        self.data = self.generate_data()

    def generate_data(self):
        df = pd.read_excel(self.file)
        df = df[~df['Precio Ajustado'].isna()].reset_index(drop=True)

        list_prices: List[Prices] = []
        for i in range(df.shape[0]):
            sizes: List[str] = str(df.loc[i, 'Talla']).replace(',', '').split()
            for size in sizes:
                Prices.id += 1
                list_prices.append(
                    Prices(
                        reference=str(df.loc[i, 'Producto']),
                        size=size,
                        collection=df.loc[i, 'Colección'],
                        price=df.loc[i, 'Precio Ajustado'],
                        cost=df.loc[i, 'COSTO']
                    ).row()
                )

        return list_prices

    def save(self, name_file):
        pd.DataFrame(self.data).to_csv(
            'Prueba.csv', index=False, encoding='utf-8')
