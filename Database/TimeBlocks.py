from Database.Database import Database


class TimeBlocks:
    def __init__(self):
        self.database = Database()

    def __del__(self):
        del self.database

    def getAll(self, count_time):
        self.database.cursor.execute('SELECT * FROM TimeBlocks ORDER BY id limit %s', (count_time,))
        data = self.database.cursor.fetchall()
        return data
