from Database.Competences import Competences
from Database.Dones import Dones
from Database.Leaders import Leaders
from Database.Particiapnts import Participants
from Database.TimeBlocks import TimeBlocks
from Database.Verification import Verification


class GetData:

    def __init__(self):
        self.dones = Dones()
        self.participants = Participants()
        self.competences = Competences()
        self.timeBlocks = TimeBlocks()
        self.leaders = Leaders()
        self.verifications = Verification()

    def __del__(self):
        del self.dones
        del self.participants
        del self.competences
        del self.timeBlocks
        del self.leaders
        del self.verifications

    def GetDones(self):
        dones = self.dones.getAll()
        toReturn = []
        # return only id of participant (index 0) and competeces (index 1)
        for done in dones:
            toReturn.append((dict(participant_id=done["participant_id"], competence_id=done["competence_id"])))
        return toReturn

    def GetAllParticipantWithCompetences(self):
        participants = self.participants.getAll()
        competences = self.competences.getAll()

        # [participant, competences]
        returnValue = []
        for participant in participants:
            for competence in competences:
                returnValue.append((dict(participant_id=participant["id"], competence_id=competence["id"])))

        return returnValue

    def GetDataForGA(self):
        allCombination = self.GetAllParticipantWithCompetences()
        reduce = self.GetDones()
        for reducing in reduce:
            allCombination.remove(reducing)
        return allCombination

    def GetTimeBlocksForSchedule(self, count_time):
        return self.timeBlocks.getAll(count_time)

    def GetCountOfLeaders(self):
        return self.leaders.getCount()

    def GetCountOfParticipant(self):
        return self.participants.getCount()

    def GetLeaders(self):
        return self.leaders.getAll()

    def GetParticipants(self):
        return self.participants.getAll()

    def GetCompetences(self):
        return self.competences.getAll()

    def GetVerifications(self):
        return self.verifications.getAll()


class myGAData:
    def __init__(self):
        self.verifications = None
        self.competences = None
        self.leaders = None
        self.init_population = None
        self.time_blocks = None
        self.participants = None
        self.mustDones = None

    def InitData(self, count_time):
        data = GetData()
        self.mustDones = data.GetDataForGA()
        self.time_blocks = data.GetTimeBlocksForSchedule(count_time)
        self.init_population = []
        self.leaders = data.GetLeaders()
        self.competences = data.GetCompetences()
        self.participants = data.GetParticipants()
        self.verifications = data.GetVerifications()
        del data
