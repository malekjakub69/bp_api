from collections import Counter

from Database.Database import Database
from Database.Leaders import Leaders
from Database.Particiapnts import Participants
from Database.TimeBlocks import TimeBlocks
from Database.Verification import Verification


class ScheduleData:
    def __init__(self):
        self.database = Database()

    def __del__(self):
        del self.database

    def getAll(self, schedule_id):
        self.database.cursor.execute("SELECT sd.id as id, l.name as leader_name, p.name as participant_name, sd.color as color, "
                                     "c.name as competence_name, l.id as leader_id, p.id as participant_id, timeblock_id "
                                     "FROM Scheduledata sd "
                                     "LEFT JOIN leaders l on l.id = sd.leader_id "
                                     "LEFT JOIN competences c on c.id = sd.competence_id "
                                     "LEFT JOIN participants p on p.id = sd.participant_id "
                                     " WHERE sd.schedule_id = %s", (schedule_id,))
        data = self.database.cursor.fetchall()
        return data

    def getAllId(self, schedule_id):
        self.database.cursor.execute("SELECT * FROM Scheduledata sd "
                                     " WHERE sd.schedule_id = %s", (schedule_id,))
        data = self.database.cursor.fetchall()
        return data

    def saveData(self, participant_data, data, schedule_id):
        self.database.cursor.execute('INSERT INTO scheduledata ('
                                     '"competence_id", "timeblock_id", "leader_id", "participant_id", "schedule_id") VALUES(%s, %s, %s, %s, %s)',
                                     (participant_data[data[0]]["competence_id"], data[2], data[1], participant_data[data[0]]["participant_id"], schedule_id))
        self.database.conn.commit()

    def updateColor(self, color, schedule_data_id):
        self.database.cursor.execute('UPDATE scheduledata SET color = %s WHERE id = %s',
                                     (color, schedule_data_id))
        self.database.conn.commit()

    def updateColorParticipant(self, color, schedule_id, time_id, participant_id):
        self.database.cursor.execute('UPDATE scheduledata SET color = %s WHERE id = %s',
                                     (color, schedule_data_id))
        self.database.conn.commit()

    def checkColission(self, schedule_id):
        data = self.getAllId(schedule_id)
        verifications = Verification()
        verifications = verifications.getAll()
        times = TimeBlocks()
        participants = Participants()
        # leader x competence collision
        for item in data:
            conflict = True
            for verification in verifications:
                if verification["leader_id"] == item["leader_id"] and verification["competence_id"] == item["competence_id"]:
                    conflict = False
                    break
            if conflict:
                self.updateColor("#FFBBBB", item["id"])
            elif item['color'] == "#FFBBBB":
                self.updateColor("", item["id"])
        # participant colision
        for time in times.getAll(40):
            for participant in participants.getAll():
                my_array = []
                for item in data:
                    if item['color'] != "":
                        self.updateColor("", item["id"])
                    if item['participant_id'] == participant['id'] and item['timeblock_id'] == time['id']:
                        my_array.append(item['id'])
                if len(my_array) > 1:
                    for change_id in my_array:
                        self.updateColor("#FF9999", change_id)

    def updateItem(self, item_id, time_id, leader_id):
        self.database.cursor.execute('UPDATE scheduledata SET timeblock_id = %s, leader_id = %s, color = \'\' WHERE id = %s',
                                     (time_id, leader_id, item_id))
        self.database.conn.commit()

