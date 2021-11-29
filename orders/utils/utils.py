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

def range_for_paginations(paginator, page_obj, value_range=5):
    value_range = value_range
    value_range_max = paginator.num_pages
    value_min = page_obj.number - value_range
    value_max = page_obj.number + value_range
    return (value_min if value_max < value_range_max else value_range_max -  value_range * 2, value_max if value_min > 0 else value_range * 2)

def select_to_search_order(data):
    to_search = {}
    if data.get('date', None) != '0':
        to_search['date__gte'] = data['date']
    if data.get('id_order', None) != 0:
        to_search['id_order'] = data['id_order']
    if data.get('customer', None) != '0':
        to_search['customer__icontains'] = data['customer']
    if data.get('agent', None) != '0':
        to_search['agent__icontains'] = data['agent']
    return to_search