from access.ServicesOrders import ServicesAddFileOrdersOrigin
from access.controller import *
from view.ViewMain import ViewMain

PATH = './files/'


def run():
    # delete_all()
    # ServicesAddFileOrdersOrigin('PEDIDOS-RECOPIILACION DE PEDIDOS 2019 A HOY.xls')
    ViewMain()


if __name__ == '__main__':
    run()
