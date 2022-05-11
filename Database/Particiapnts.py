from Database.Database import Database


class Participants:
    def __init__(self):
        self.database = Database()

    def __del__(self):
        del self.database

    def getAll(self):
        self.database.cursor.execute("SELECT id as id, id as key, name as name FROM Participants")
        data = self.database.cursor.fetchall()
        return data

    def getCount(self):
        self.database.cursor.execute("SELECT COUNT(id) FROM Participants;")
        data = self.database.cursor.fetch()
        return data

    def getOne(self, participant_id):
        self.database.cursor.execute("SELECT * FROM Participants WHERE id = %s;", (participant_id,))
        data = self.database.cursor.fetchone()
        return data

    def create(self, participant_name):
        self.database.cursor.execute('INSERT INTO participants ("name") VALUES (%s)', (participant_name,))
        self.database.conn.commit()

    def update(self, participant_name, participant_id):
        self.database.cursor.execute('UPDATE participants SET name = %s WHERE id = %s',
                                     (participant_name, participant_id))
        self.database.conn.commit()

    def delete(self, participant_id):
        self.database.cursor.execute('DELETE FROM participants WHERE id = %s',
                                     (participant_id, ))
        self.database.conn.commit()
