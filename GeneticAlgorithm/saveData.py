import random

from Database.Schedules import Schedules
from Database.ScheduleData import ScheduleData


def getScheduleName():
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    randomString = ''
    for i in range(4):
        randomString += characters[random.randint(0, len(characters) - 1)]
    return "schedule_" + randomString


def createNewSchedule():
    schedule = Schedules()
    scheduleName = getScheduleName()
    return schedule.createNew(scheduleName)


def updateSchedule(schedule_id, state, fitness=0):
    schedule = Schedules()
    schedule.update(schedule_id, state)
    schedule.updateFitness(fitness, schedule_id)


def saveData(must_done, solution, schedule_id):
    scheduleData = ScheduleData()

    for item in solution:
        scheduleData.saveData(must_done, item, schedule_id)

    return schedule_id
