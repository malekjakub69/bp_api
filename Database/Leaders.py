from Database.Database import Database


class Leaders:
    def __init__(self):
        self.database = Database()

    def __del__(self):
        del self.database

    def getAll(self):
        self.database.cursor.execute("SELECT l.id as id, l.name as name FROM Leaders l")
        data = self.database.cursor.fetchall()
        return data

    def getCount(self):
        self.database.cursor.execute("SELECT COUNT(id) FROM Leaders;")
        data = self.database.cursor.fetch()
        return data

    def create(self, participant_name):
        self.database.cursor.execute('INSERT INTO leaders ("name") VALUES (%s)', (participant_name,))
        self.database.conn.commit()
        self.database.cursor.execute('SELECT id FROM leaders WHERE name = %s LIMIT 1', (participant_name,))
        return self.database.cursor.fetchall()[0]['id']

    def update(self, participant_name, participant_id):
        self.database.cursor.execute('UPDATE leaders SET name = %s WHERE id = %s',
                                     (participant_name, participant_id))
        self.database.conn.commit()

    def delete(self, participant_id):
        self.database.cursor.execute('DELETE FROM leaders WHERE id = %s',
                                     (participant_id,))
        self.database.conn.commit()
