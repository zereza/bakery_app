class Order:
    def __init__(self, table_no, order, status):
        self.table_no = table_no
        self.order = []
        self.status = False

    def recieve_order(self):