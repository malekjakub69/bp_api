import math
import random

from collections import Counter

from pygad import pygad

from Database.ScheduleData import ScheduleData
from Database.Schedules import Schedules
from GeneticAlgorithm.GetData import myGAData
from GeneticAlgorithm.myFunctions import *
from GeneticAlgorithm.saveData import saveData, createNewSchedule, updateSchedule

my_data = myGAData()

leaders_id = []
timeblocks_id = []


# Function for inti Popualation
def InitPopulation(count_time):
    my_data.InitData(count_time)
    if len(my_data.mustDones) > len(my_data.time_blocks) * len(my_data.leaders):
        return False

    for item in my_data.leaders:
        leaders_id.append(item["id"])
    for item in my_data.time_blocks:
        timeblocks_id.append(item["id"])

    for i in range(500):
        chromosome = []
        for mustDone in range(len(my_data.mustDones)):
            chromosome.append(encodeNumbers((mustDone,  # every item from Cartesian
                                             leaders_id[random.randint(0, len(leaders_id) - 1)],  # random leaders
                                             timeblocks_id[random.randint(0, len(timeblocks_id) - 1)])))  # random time
        #           every chromosome save to array with their fitness value
        my_data.init_population.append(chromosome)
    return True


# Fitness function
def FitnessFunc(chromosome, index_of):
    decodeChromosome = []
    for gen in chromosome:
        decodeChromosome.append(decodeNumber(gen))

    moreBlocksInOnCell = MoreBlocksInOneCell(decodeChromosome)  # 0.2

    participantCollision = ParticipantCollision(decodeChromosome)  # 0.2

    wrongLeaderCompetenceCombination = WrongLeaderCompetenceCombination(decodeChromosome)  # 0.2

    spaceBetweenLeader = SpaceBetweenLeader(decodeChromosome)  # 0.05

    spaceBetweenParticipant = SpaceBetweenParticipant(decodeChromosome)  # 0.05

    return moreBlocksInOnCell * 0.33 + participantCollision * 0.30 + wrongLeaderCompetenceCombination * 0.33 + spaceBetweenLeader * 0.02 + spaceBetweenParticipant * 0.02


# 1. rule for fitness function
def MoreBlocksInOneCell(chromosome):
    toReturnValue = 0
    countFull = 0
    for leader in my_data.leaders:
        for time_block in my_data.time_blocks:
            fitness_value = 1
            match = False
            for gen in chromosome:
                # leader_id is index 1 time_id is index 2
                if gen[1] == leader["id"] and gen[2] == time_block["id"]:
                    if match:
                        fitness_value *= 0.5
                    match = True
            if match:
                toReturnValue += fitness_value
                countFull += 1
    # value of every fill cell divided their count
    if countFull == 0:
        return 1
    return toReturnValue/countFull


# 2. rule for fitness function
def ParticipantCollision(chromosome):
    toReturn = 0
    for participant in my_data.participants:
        times = []
        for gen in chromosome:
            # mustDone is index 0
            if my_data.mustDones[gen[0]]["participant_id"] == participant["id"]:
                # time_id is index 2
                times.append(gen[2])
        counter = Counter(times)
        participant_duplicities = list([counter[item] - 1 for item in counter if counter[item] > 1])
        if len(participant_duplicities) == 0:
            toReturn += 1
        else:
            toReturn += math.pow(0.5, sum(participant_duplicities))
    return toReturn / len(my_data.participants)


# 3. rule for fitness function
def WrongLeaderCompetenceCombination(chromosome):
    countCorrect = 0
    for gen in chromosome:
        correct = False
        # mustDone_id is index 0
        competence_id = my_data.mustDones[gen[0]]["competence_id"]
        # leader_id is index 1
        leader_id = gen[1]
        for verification in my_data.verifications:
            if verification["leader_id"] == leader_id and verification["competence_id"] == competence_id:
                correct = True
                break
        if correct:
            countCorrect += 1
    toReturn = math.pow(0.5, len(chromosome) - countCorrect)
    return toReturn


# 4. rule for fitness function
def SpaceBetweenLeader(chromosome):
    toReturn = 0
    for leader in my_data.leaders:
        verifications = []
        time = []
        for gen in chromosome:
            # leader_id is index 1
            if gen[1] == leader["id"]:
                if gen[2] not in time:
                    verifications.append(gen)
                    time.append(gen[2])
        verifications.sort(key=TakeTime)
        if len(verifications) > 1:
            diff = verifications[-1][2] - verifications[0][2] + 1
            toReturn += (len(verifications) / diff)
        else:
            toReturn += 1
    return toReturn / len(my_data.leaders)


# 4. rule for fitness function
def SpaceBetweenParticipant(chromosome):
    toReturn = 0
    for participant in my_data.participants:
        verifications = []
        time = []
        for gen in chromosome:
            # mustDone is index 0
            if my_data.mustDones[gen[0]]["participant_id"] == participant["id"]:
                if gen[2] not in time:
                    verifications.append(gen)
                    time.append(gen[2])
        verifications.sort(key=TakeTime)
        if len(verifications) > 1:
            diff = verifications[-1][2] - verifications[0][2] + 1
            toReturn += (len(verifications) / diff)
        else:
            toReturn += 1
    return toReturn / len(my_data.participants)


# Function for Mutation
def FindDuplicity(chromosome):
    duplicity_index = []
    for leader in my_data.leaders:
        for time_block in my_data.time_blocks:
            counts = []
            for gen in chromosome:
                # leader_id is index 1 time_id is index 2
                if gen[1] == leader["id"] and gen[2] == time_block["id"]:
                    counts.append(gen)
            if len(counts) > 1:
                for count in counts:
                    duplicity_index.append(count[0])
    return duplicity_index


# Function for Mutation
def FindLeaderCompetencesCollision(chromosome):
    collision_index = []
    for gen in chromosome:
        conflict = True
        for verification in my_data.verifications:
            if verification["leader_id"] == gen[1] and verification["competence_id"] == my_data.mustDones[gen[0]]["competence_id"]:
                conflict = False
                break
        if conflict:
            collision_index.append(gen[0])
    return collision_index


# Mutation function
def MutationFunc(offspring, ga_instance):
    toReturnOffspring = []
    for chromosome in offspring:
        decodeChromosome = []
        for gen in chromosome:
            decodeChromosome.append(decodeNumber(gen))
        duplicity = FindDuplicity(decodeChromosome)
        leader_competences_collision = FindLeaderCompetencesCollision(decodeChromosome)

        if len(duplicity) > 0:
            item = duplicity[random.randint(0, len(duplicity) - 1)]
            rnd = random.random()
            if rnd < 0.3:
                decodeChromosome[item][1] = leaders_id[random.randint(0, len(leaders_id) - 1)]  # random leaders
            elif rnd < 0.6:
                decodeChromosome[item][2] = timeblocks_id[random.randint(0, len(timeblocks_id) - 1)]  # random time
            else:
                decodeChromosome[item][1] = leaders_id[random.randint(0, len(leaders_id) - 1)]  # random leaders
                decodeChromosome[item][2] = timeblocks_id[random.randint(0, len(timeblocks_id) - 1)]  # random time
        elif len(leader_competences_collision) > 0:
            item = leader_competences_collision[random.randint(0, len(leader_competences_collision) - 1)]
            for verification in my_data.verifications:
                if verification["competence_id"] == my_data.mustDones[decodeChromosome[item][0]]["competence_id"]:
                    decodeChromosome[item][1] = verification["leader_id"]
                    if random.random() > 0.5:
                        decodeChromosome[item][2] = timeblocks_id[random.randint(0, len(timeblocks_id) - 1)]  # random time
                        break
        if len(duplicity) == 0 and len(leader_competences_collision) == 0:
            item = random.randint(0, len(my_data.mustDones) - 1)
            rnd = random.random()
            if rnd < 0.3:
                decodeChromosome[item][1] = leaders_id[random.randint(0, len(leaders_id) - 1)]  # random leaders
            elif rnd < 0.6:
                decodeChromosome[item][2] = timeblocks_id[random.randint(0, len(timeblocks_id) - 1)]  # random time
            else:
                decodeChromosome[item][1] = leaders_id[random.randint(0, len(leaders_id) - 1)]  # random leaders
                decodeChromosome[item][2] = timeblocks_id[random.randint(0, len(timeblocks_id) - 1)]  # random time
        toReturnChromosome = []
        for gen in decodeChromosome:
            toReturnChromosome.append(encodeNumbers(gen))
        toReturnOffspring.append(toReturnChromosome)
    return toReturnOffspring


# Crossover function
def CrossoverFunc(parents, offspring_size, ga_instance):
    toReturn = []
    for chromosomeA, chromosomeB in zip(parents[0::2], parents[1::2]):

        parentLen = len(chromosomeA) // 4

        for i in range(2):
            childA = []  # [AABB]
            childA.extend(chromosomeA[:parentLen])
            childA.extend(chromosomeA[parentLen:2 * parentLen])
            childA.extend(chromosomeB[2 * parentLen:3 * parentLen])
            childA.extend(chromosomeB[3 * parentLen:])

            childB = []  # [ABAB]
            childB.extend(chromosomeA[:parentLen])
            childB.extend(chromosomeB[parentLen:2 * parentLen])
            childB.extend(chromosomeA[2 * parentLen:3 * parentLen])
            childB.extend(chromosomeB[3 * parentLen:])

            childC = []  # [AAAB]
            childC.extend(chromosomeA[:parentLen])
            childC.extend(chromosomeA[parentLen:2 * parentLen])
            childC.extend(chromosomeA[2 * parentLen:3 * parentLen])
            childC.extend(chromosomeB[3 * parentLen:])

            childD = []  # [ABBB]
            childD.extend(chromosomeA[:parentLen])
            childD.extend(chromosomeB[parentLen:2 * parentLen])
            childD.extend(chromosomeB[2 * parentLen:3 * parentLen])
            childD.extend(chromosomeB[3 * parentLen:])

            chromosomeA, chromosomeB = chromosomeB, chromosomeA

            toReturn.append(childA)
            toReturn.append(childB)
            toReturn.append(childC)
            toReturn.append(childD)
    return toReturn


def updateFitness(schedule_id):
    my_data.InitData(0)

    schedule_data = ScheduleData()
    schedule_data = schedule_data.getAllId(schedule_id)
    chromozome = []
    for data in schedule_data:
        index_of_data = next(
            (index for (index, d) in enumerate(my_data.mustDones) if d["participant_id"] == data["participant_id"] and d["competence_id"] == data["competence_id"]), None)
        chromozome.append((index_of_data, data["leader_id"], data["timeblock_id"]))

    moreBlocksInOnCell = MoreBlocksInOneCell(chromozome)  # 0.2
    participantCollision = ParticipantCollision(chromozome)  # 0.2
    # leaderCollision = LeaderCollision(chromozome)  # 0.2
    wrongLeaderCompetenceCombination = WrongLeaderCompetenceCombination(chromozome)  # 0.2
    spaceBetweenLeader = SpaceBetweenLeader(chromozome)  # 0.05
    spaceBetweenParticipant = SpaceBetweenParticipant(chromozome)  # 0.05

    fitness = moreBlocksInOnCell * 0.33 + participantCollision * 0.30 + wrongLeaderCompetenceCombination * 0.33 + spaceBetweenLeader * 0.02 + spaceBetweenParticipant * 0.02

    schedules = Schedules()
    schedules.updateFitness(fitness, schedule_id)


def Run(time):
    schedule_id = createNewSchedule()

    if not InitPopulation(time):
        updateSchedule(schedule_id, "chyba-málo místa")
        return False

    ga = pygad.GA(num_generations=500,
                  num_parents_mating=100,
                  fitness_func=FitnessFunc,
                  num_genes=len(my_data.init_population[0]),
                  initial_population=my_data.init_population,
                  crossover_type=CrossoverFunc,
                  mutation_type=MutationFunc,
                  gene_type=int,
                  stop_criteria="saturate_30"
                  )

    ga.run()

    solution, solution_fitness, solution_idx = ga.best_solution()

    decodeSolution = []
    for i in solution:
        decodeSolution.append(decodeNumber(i))

    updateSchedule(schedule_id, "hotovo", solution_fitness)
    schedule_id = saveData(my_data.mustDones, decodeSolution, schedule_id)

    return schedule_id
