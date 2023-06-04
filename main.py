from model.double7 import DoubleZero7
from model.order import Order
from model.search import Search

if __name__ == '__main__':
    s = Search()
    s.run("123123123123")

    o = Order()
    o.run()

    d = DoubleZero7()
    d.run()
