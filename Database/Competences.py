from Database.Database import Database


class Competences:
    def __init__(self):
        self.database = Database()

    def __del__(self):
        del self.database

    def getAll(self):
        self.database.cursor.execute("SELECT * FROM Competences")
        data = self.database.cursor.fetchall()
        return data

    def getOne(self, competence_id):
        self.database.cursor.execute("SELECT * FROM Competences WHERE id = %s;", (competence_id,))
        data = self.database.cursor.fetchone()
        return data
