from access.ServicesOrders import *
from access.controller import *

PATH = './files/'


def run():
    # delete_all()
    # ServicesAddFileOrders('PEDIDOS-RECOPIILACION DE PEDIDOS 2019 A HOY.xls')
    print(read_all_orders())


if __name__ == '__main__':
    run()
