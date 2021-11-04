import pandas as pd
from typing import List, Any

SIZES_ALPHA = ['XS', 'S', 'RN', 'P', 'M', 'G', 'L', 'XL', 'XXL']


def save_file(data: pd.DataFrame, name_file):
    writer = pd.ExcelWriter(name_file,
                            datetime_format='dd-mm-yy')
    data.to_excel(writer, index=False, sheet_name='Data')
    writer.save()
    writer = None


def sort_sizes(list_sizes: List[str]):
    list_size_numeric: List[int] = []
    list_size_alpha: List[str] = []
    aux: List[str] = []

    for size in list_sizes:
        value = size
        if value.isnumeric():
            value = int(value)
            list_size_numeric.append(value)
        else:
            list_size_alpha.append(value)

    for i in range(len(SIZES_ALPHA)):
        if SIZES_ALPHA[i] in list_size_alpha:
            aux.append(SIZES_ALPHA[i])

    list_size_alpha = aux
    list_size_numeric.sort()
    list_size: List[Any] = list_size_alpha + list_size_numeric
    list_size = list(map(str, list_size))
    return list_size
