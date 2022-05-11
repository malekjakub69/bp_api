from Database.Database import Database


class Dones:
    def __init__(self):
        self.database = Database()

    def __del__(self):
        del self.database

    def getAll(self):
        self.database.cursor.execute("SELECT p.id as participant_id, c.id as competence_id, p.name as participant_name,"
                                     " c.name as competence_name FROM Done d "
                                     "LEFT JOIN Participants p ON d.participant_id = p.id "
                                     "LEFT JOIN Competences c ON d.competence_id = c.id;")
        data = self.database.cursor.fetchall()
        return data

    def getAllWhereParticipant(self, participant_id):
        self.database.cursor.execute("SELECT p.id as participant_id, c.id as competence_id, p.name as participant_name,"
                                     " c.name as competence_name FROM Done d "
                                     "LEFT JOIN Participants p ON d.participant_id = p.id "
                                     "LEFT JOIN Competences c ON d.competence_id = c.id "
                                     "WHERE p.id = %s;", (participant_id,))
        data = self.database.cursor.fetchall()
        return data
