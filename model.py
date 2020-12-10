from typing import NoReturn
from typing import NewType
import numpy as np
from numpy import random

class Class:
    # Initialize new Class
    def __init__(self, classid: int, groupid: int, moduleid: int):
        self.classid: int = classid
        self.groupid: int = groupid
        self.moduleid: int = moduleid

    def setprofessor(self, professorid: int) -> NoReturn:
        self.professorid: int = professorid

    def settimeslot(self, timeslotid: int) -> NoReturn:
        self.timeslotid: int = timeslotid

    def setroomid(self, roomid: int) -> NoReturn:
        self.roomid: int = roomid

    def getclassid(self) -> int:
        return self.classid

    def getgroupid(self) -> int:
        return self.groupid

    def getmoduleid(self) -> int:
        return self.moduleid

    def getprofessorid(self) -> int:
        return self.professorid
    
    def gettimeslotid(self) -> int:
        return self.timeslotid
    
    def getroomid(self) -> int:
        return self.roomid
   
class Group:
    def __init__(self, idd, size, moduleids):
        self.groupid = idd
        self.groupsize = size
        self.moduleids = moduleids

    def getgroupid(self):
        return self.groupid

    def getgroupsize(self):
        return self.groupsize

    def getmoduleids(self):
        return self.moduleids

class Individual:

    def __init__(self, timetable=None, chromosomelength=None, chromosome=None):
        self.fitness = -1.0

        if timetable is not None:
            numclasses = timetable.getnumclasses()
            chlen = numclasses * 3

            newchromosome = np.zeros(chlen, int) 
            chromosomeindex = 0
            for group in timetable.getgroups_as_array():
                for moduleid in group.getmoduleids():
                    timeslotid = timetable.getrandtimeslot().gettimeslotid()
                    newchromosome[chromosomeindex] = timeslotid
                    chromosomeindex += 1

                    roomid = timetable.getrandroom().getroomid()
                    newchromosome[chromosomeindex] = roomid
                    chromosomeindex += 1

                    module = timetable.getmodule(moduleid)
                    newchromosome[chromosomeindex] = module.getrandprofessorid()
                    chromosomeindex += 1
            self.chromosome = newchromosome
        elif chromosomelength is not None:
            self.chromosome = np.array([i for i in range(chromosomelength)], int)   
        elif chromosome is not None:
            self.chromosome = chromosome
    
    def getchromosome(self):
        return self.chromosome

    def getchromosomelength(self):
        return self.chromosome.size

    def setgene(self, offset, gene):
        self.chromosome[offset] = gene

    def getgene(self, offset):
        return self.chromosome[offset]
    
    def setfitness(self, fitness):
        self.fitness = fitness

    def getfitness(self):
        return self.fitness

    def __str__(self):
        output = [gene for gene in self.chromosome]
        return " ".join(output)

    def containgene(self, gene):
        for chrom in self.chromosome:
            if chrom == gene:
                return True
        return False

class Module:
    def __init__(self, moduleid, modulecode, module, professorids):
        self.moduleid = moduleid
        self.modulecode = modulecode
        self.module = module
        self.professorids = professorids

    def getmoduleid(self):
        return self.moduleid

    def getmodulecode(self):
        return self.modulecode

    def getmodulename(self):
        return self.module
    
    def getrandprofessorid(self):
        return np.random.choice(self.professorids)

class Population:
    def __init__(self, populationsize, timetable=None, chromosomelength=None):
        self.population_fitness = -1.0
        self.population = np.empty(populationsize, object)

        if timetable is not None:
            for i in range(populationsize):
                self.population[i] = Individual(timetable=timetable)
        elif chromosomelength is not None:
            self.population = np.array([Individual(chromosomelength=chromosomelength) for i in range(populationsize)], object)
            
    
    def getindividuals(self):   
        return self.population

    def getfittest(self, offset):
        poplist = self.population.tolist()
        self.population = np.array(sorted(poplist, key=lambda item: item.getfitness() if item is not None else 0, reverse=True), object)
        return self.population[offset]

    def setpopulationfitness(self, fitness):
        self.population_fitness = fitness

    def getpopulationfitness(self):
        return self.population_fitness

    def size(self):
        return self.population.size

    def setindividual(self, offset, individual):
        self.population[offset] = individual

    def getindividual(self, offset):
        return self.population[offset]

    def shuffle(self):
        np.random.shuffle(self.population)
        

class Professor:
    def __init__(self, professorid, professorname):
        self.professorid = professorid
        self.professorname = professorname

    def getprofessorid(self):
        return self.professorid
    
    def getprofessorname(self):
        return self.professorname

class Room:
    def __init__(self, roomid, room_nmb, capacity):
        self.roomid = roomid
        self.room_nmb = room_nmb
        self.capacity = capacity
    
    def getroomid(self):
        return self.roomid

    def getroom_nmb(self):
        return self.room_nmb

    def getcapacity(self):
        return self.capacity

class Timeslot:
    def __init__(self, timeslotid, timeslot):
        self.timeslotid = timeslotid
        self.timeslot = timeslot

    def gettimeslotid(self):
        return self.timeslotid

    def gettimeslot(self):
        return self.timeslot

class Timetable:

    def __init__(self, timetable=None):
        self.numclasses = 0
        self.rooms = {}
        self.professors = {}
        self.modules = {}
        self.groups = {}
        self.timeslots = {}
        self.classes = np.empty(0, object)

        if timetable is not None:
            self.rooms = timetable.getrooms()
            self.professors = timetable.getprofessors()
            self.modules = timetable.getmodules()
            self.groups = timetable.getgroups()
            self.timeslots = timetable.gettimeslots()

    def getgroups(self):
        return self.groups
    
    def getprofessors(self):
        return self.professors

    def getmodules(self):
        return self.modules

    def gettimeslots(self):
        return self.timeslots

    def addroom(self, roomid, roomname, capacity):
        self.rooms[roomid] = Room(roomid, roomname, capacity)

    def addprofessor(self, professorid, professorname):
        self.professors[professorid] = Professor(professorid, professorname)
    
    def addmodule(self, moduleid, modulecode, module, professorsids):
        self.modules[moduleid] = Module(moduleid, modulecode, module, professorsids)

    def addgroup(self, groupid, groupsize, moduleids):
        self.groups[groupid] = Group(groupid, groupsize, moduleids)
        self.numclasses = 0

    def addtimeslot(self, timeslotid, timeslot):
        self.timeslots[timeslotid] = Timeslot(timeslotid, timeslot)

    def create_classes(self, individual):
        classes = np.empty(self.getnumclasses(), object)

        chromosome = individual.getchromosome()
        chromosomepos = 0
        classindex = 0

        for group in self.getgroups_as_array():
            moduleids = group.getmoduleids()
            for moduleid in moduleids:
                classes[classindex] = Class(classindex, group.getgroupid(), moduleid)

                classes[classindex].settimeslot(chromosome[chromosomepos])
                chromosomepos += 1

                classes[classindex].setroomid(chromosome[chromosomepos])
                chromosomepos += 1

                classes[classindex].setprofessor(chromosome[chromosomepos])
                chromosomepos += 1

                classindex += 1
        
        self.classes = classes

    def getroom(self, roomid):
        if (roomid not in self.rooms.keys()):
            print(f"Rooms doesn'r contain key: {roomid}")
        return self.rooms[roomid]

    def getrooms(self):
        return self.rooms

    def getrandroom(self):
        return np.random.choice(np.array(list(self.rooms.values()), object))
    
    def getprofessor(self, professorid):
        return self.professors[professorid]

    def getmodule(self, moduleid):
        return self.modules[moduleid]

    def getgroupmodules(self, groupid):
        return self.groups[groupid].getmoduleids()

    def getgroup(self, groupid):
        return self.groups[groupid]

    def getgroups_as_array(self):
        return np.array(list(self.groups.values()), object)

    def gettimeslot(self, timeslotid):
        return self.timeslots[timeslotid]

    def getrandtimeslot(self):
        return np.random.choice(np.array(list(self.timeslots.values())))

    def getclasses(self):
        return self.classes
    
    def getnumclasses(self):
        if self.numclasses > 0:
            return self.numclasses
        
        self.numclasses = sum(group.getmoduleids().size for group in list(self.groups.values()))
        return self.numclasses

    def calc_clashes(self):
        clashes = 0

        for class_a in self.classes:
            roomcapacity = self.getroom(class_a.getroomid()).getcapacity()
            groupsize = self.getgroup(class_a.getgroupid()).getgroupsize()

            if roomcapacity < groupsize:
                clashes += 1

            for class_b in self.classes: 
                if class_a.getroomid() == class_b.getroomid() \
                    and class_a.gettimeslotid() == class_b.gettimeslotid() \
                    and class_a.getclassid() != class_b.getclassid():
                    clashes += 1
                    break

            for class_b in self.classes:
                if class_a.getprofessorid() == class_b.getprofessorid() \
                    and class_a.gettimeslotid() == class_b.gettimeslotid() \
                    and class_a.getclassid() != class_b.getclassid():
                    clashes += 1
                    break

        return clashes
