from Database.Database import Database


class Verification:
    def __init__(self):
        self.database = Database()

    def __del__(self):
        del self.database

    def getAll(self):
        self.database.cursor.execute("SELECT * FROM Verification")
        data = self.database.cursor.fetchall()
        return data

    def getAllWhereLeader(self, leader_id):
        self.database.cursor.execute("SELECT * FROM Verification WHERE leader_id = %s", (leader_id, ))
        data = self.database.cursor.fetchall()
        return data

    def delete(self, leader_id, competence_id):
        self.database.cursor.execute('DELETE FROM verification WHERE leader_id = %s AND competence_id = %s',
                                     (leader_id, competence_id))
        self.database.conn.commit()

    def create(self, leader_id, competence_id):
        self.database.cursor.execute('INSERT INTO verification ("leader_id", "competence_id") VALUES (%s, %s)', (leader_id, competence_id))
        self.database.conn.commit()
    