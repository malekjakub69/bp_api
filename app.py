import json
from multiprocessing import Process

from flask import Flask
from flask import request
from flask_cors import CORS

from Database.Competences import Competences
from Database.Database import DecimalEncoder
from Database.Leaders import Leaders
from Database.Particiapnts import Participants
from Database.ScheduleData import ScheduleData
from Database.Schedules import Schedules
from Database.Verification import Verification
from GeneticAlgorithm.myGA import Run, updateFitness

app = Flask(__name__)
CORS(app)


# --------------------------------
# |        RIGHT API             |
# --------------------------------


# --------------------------------
#           SCHEDULES
# --------------------------------
@app.route("/get_schedule_names", methods=['GET'])
def getScheduleNames():
    schedules = Schedules()
    return json.dumps(schedules.getNames(), cls=DecimalEncoder)


@app.route("/get_schedule/<schedule_id>", methods=['GET'])
def getSchedule(schedule_id):
    schedule_data = ScheduleData()
    return json.dumps(schedule_data.getAll(schedule_id))


@app.route("/generate_schedule", methods=['POST'])
def generateSchedule():
    time = request.json.get('time')
    p = Process(target=processGenerate, args=(time,))
    p.start()
    return ""


def processGenerate(time):
    schedule_id = Run(time)
    if schedule_id:
        scheduleData = ScheduleData()
        scheduleData.checkColission(schedule_id)


@app.route("/change_schedule", methods=['POST'])
def changeSchedule():
    scheduleData = ScheduleData()
    item1 = request.json.get('item_1')
    item2 = request.json.get('item_2')
    schedule_id = request.json.get('schedule_id')
    if item1['item_id'] != -1:
        scheduleData.updateItem(item_id=item1['item_id'], time_id=item2['time_id'], leader_id=item2['leader_id'])
    if item2['item_id'] != -1:
        scheduleData.updateItem(item_id=item2['item_id'], time_id=item1['time_id'], leader_id=item1['leader_id'])
    scheduleData.checkColission(schedule_id)
    updateFitness(schedule_id)
    return ""


@app.route("/delete_schedule/<schedule_id>", methods=['DELETE'])
def deleteSchedule(schedule_id):
    schedules = Schedules()
    schedules.delete(schedule_id)
    return ""


# --------------------------------
#            PARTICIPANTS
# --------------------------------

@app.route("/participants", methods=['GET'])
def getParticipants():
    participants = Participants()
    return json.dumps(participants.getAll())


@app.route("/create_participant", methods=['POST'])
def createParticipant():
    name = request.json.get('name')
    participants = Participants()
    participants.create(name)
    return ""


@app.route("/update_participant", methods=['POST'])
def updateParticipant():
    name = request.json.get('name')
    participant_id = request.json.get('id')
    participants = Participants()
    participants.update(name, participant_id)
    return ""


@app.route("/delete_participant/<participant_id>", methods=['DELETE'])
def deleteParticipant(participant_id):
    participants = Participants()
    participants.delete(participant_id)
    return ""


# --------------------------------
#           LEADERS
# --------------------------------

@app.route("/leaders", methods=['GET'])
def getLeaders():
    leaders = Leaders()
    return json.dumps(leaders.getAll())


@app.route("/create_leader", methods=['POST'])
def createLeader():
    name = request.json.get('name')
    competences = request.json.get('competences_id')
    leaders = Leaders()
    leader_id = leaders.create(name)
    verification = Verification()
    for comeptence in competences:
        verification.create(comeptence['id'], leader_id)
    return ""


@app.route("/update_leader", methods=['POST'])
def updateLeader():
    name = request.json.get('name')
    leader_id = request.json.get('id')
    leaders = Leaders()
    leaders.update(name, leader_id)
    return ""


@app.route("/delete_leader/<leader_id>", methods=['DELETE'])
def deleteLeader(leader_id):
    leaders = Leaders()
    leaders.delete(leader_id)
    return ""


# --------------------------------
#          VERIFICATIONS
# --------------------------------

@app.route("/competences", methods=['GET'])
def getCompetences():
    competences = Competences()
    return json.dumps(competences.getAll())


@app.route("/verifications/<leader_id>", methods=['GET'])
def getVerifications(leader_id):
    verifications = Verification()
    return json.dumps(verifications.getAllWhereLeader(leader_id))


@app.route("/create_verification", methods=['POST'])
def createVerification():
    leader_id = request.json.get('leader_id')
    competence_id = request.json.get('competence_id')
    verifications = Verification()
    verifications.create(leader_id, competence_id)
    return ""


@app.route("/delete_verification", methods=['POST'])
def deleteVerification():
    leader_id = request.json.get('leader_id')
    competence_id = request.json.get('competence_id')
    verifications = Verification()
    verifications.delete(leader_id, competence_id)
    return ""


if __name__ == '__main__':
    app.run()
