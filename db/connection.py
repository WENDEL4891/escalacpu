import sqlite3

class Connection:
    def __init__(self):
        self.conn = sqlite3.connect('./db/escalaCPU.db')        

    def getConnection(self):
        return self.conn