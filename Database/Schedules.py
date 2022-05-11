from Database.Database import Database


class Schedules:
    def __init__(self):
        self.database = Database()

    def __del__(self):
        del self.database

    def getAll(self):
        self.database.cursor.execute("SELECT * FROM Schedules")
        data = self.database.cursor.fetchall()
        return data

    def createNew(self, name):
        self.database.cursor.execute('INSERT INTO schedules ("name", "state") VALUES (%s, %s)', (name, "Připravuje se"))
        self.database.conn.commit()

        self.database.cursor.execute('SELECT id FROM schedules WHERE "name" = %s', (name,))
        item = self.database.cursor.fetchone()
        return item["id"]

    def getNames(self):
        self.database.cursor.execute("SELECT id, name, fitness, state FROM Schedules")
        names = self.database.cursor.fetchall()
        return names

    def updateFitness(self, fitness, schedule_id):
        self.database.cursor.execute('UPDATE schedules SET fitness = %s WHERE id = %s',
                                     (fitness, schedule_id))
        self.database.conn.commit()

    def update(self, schedule_id, state):
        self.database.cursor.execute('UPDATE schedules SET state = %s WHERE id = %s',
                                     (state, schedule_id))
        self.database.conn.commit()

    def delete(self, schedule_id):
        self.database.cursor.execute('DELETE FROM schedules WHERE id = %s',
                                     (schedule_id,))
        self.database.conn.commit()
