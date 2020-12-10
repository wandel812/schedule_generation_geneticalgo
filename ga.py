
from model import *

class GeneticAlgorithm:
    def __init__(self, popsize, mutation_rate, crossover_rate, elitismcount, tournamentsize):
        self.populationsize = popsize
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitismcount = elitismcount
        self.tournamentsize = tournamentsize

    def initpopulation(self, timetable):
        return Population(self.populationsize, timetable=timetable)
    
    def is_terminationconditionmet(self, generationscount, maxgenerations):
        return (generationscount > maxgenerations)
    
    def is_terminationcontitionmetpop(self, population):
        return (population.getfittest(0).getfitness() == 1.0)

    def calcfitness(self, indivivdual, timetable):
        #from copy import deepcopy
        threadtimetable = Timetable(timetable=timetable)
        threadtimetable.create_classes(indivivdual)

        clashes = threadtimetable.calc_clashes()
        fitness = 1 / float(clashes + 1)

        indivivdual.setfitness(fitness)

        return fitness

    def evalpopulation(self, population, timetable):
    #    val = sum(self.calcfitness(individual, timetable) for individual in population.getindividuals()) 
        popfitness = 0
        for individual in population.getindividuals():
            popfitness += self.calcfitness(individual, timetable)
        population.setpopulationfitness(popfitness)
    
    def selectparent(self, population):
        tournament = Population(self.tournamentsize)
        population.shuffle()
        for i in range(self.tournamentsize):
            tournamentindividual = population.getindividual(i)
            tournament.setindividual(i, tournamentindividual)
        return tournament.getfittest(0)

    def mutatepopulation(self, population, timetable):
        newpopulation = Population(self.populationsize)        

        for populationindex in range(population.size()):
            individual = population.getfittest(populationindex)
            randomindividual = Individual(timetable=timetable)

            for geneindex in range(individual.getchromosomelength()):
                if populationindex > self.elitismcount:
                    if self.mutation_rate > np.random.random():
                        individual.setgene(geneindex, randomindividual.getgene(geneindex))
            newpopulation.setindividual(populationindex, individual)
        return newpopulation
    
    def crossoverpopulation(self, population):
        newpopulation = Population(population.size())   

        for populationindex in range(population.size()):
            parent1 = population.getfittest(populationindex)

            if self.crossover_rate > np.random.random() and populationindex >= self.elitismcount:
                offspring = Individual(chromosomelength=parent1.getchromosomelength())
                parent2 = self.selectparent(population)

                for geneindex in range(parent1.getchromosomelength()):
                    if 0.5 > np.random.random():
                        offspring.setgene(geneindex, parent1.getgene(geneindex))
                    else:
                        offspring.setgene(geneindex, parent2.getgene(geneindex))
                newpopulation.setindividual(populationindex, offspring)
            else:
                newpopulation.setindividual(populationindex, parent1)
            
        return newpopulation

def init_timetable():
    timetable = Timetable()

    timetable.addroom(1, "A1", 15)
    timetable.addroom(2, "B1", 30)
    timetable.addroom(4, "D1", 20)
    timetable.addroom(5, "F1", 25)

    timetable.addtimeslot(1, "Mon 9:00 - 11:00")
    timetable.addtimeslot(2, "Mon 11:00 - 13:00")
    timetable.addtimeslot(3, "Mon 13:00 - 15:00")
    timetable.addtimeslot(4, "Tue 9:00 - 11:00")
    timetable.addtimeslot(5, "Tue 11:00 - 13:00")
    timetable.addtimeslot(6, "Tue 13:00 - 15:00")
    timetable.addtimeslot(7, "Wed 9:00 - 11:00")
    timetable.addtimeslot(8, "Wed 11:00 - 13:00")
    timetable.addtimeslot(9, "Wed 13:00 - 15:00")
    timetable.addtimeslot(10, "Thu 9:00 - 11:00")
    timetable.addtimeslot(11, "Thu 11:00 - 13:00")
    timetable.addtimeslot(12, "Thu 13:00 - 15:00")
    timetable.addtimeslot(13, "Fri 9:00 - 11:00")
    timetable.addtimeslot(14, "Fri 11:00 - 13:00")
    timetable.addtimeslot(15, "Fri 13:00 - 15:00")

    timetable.addprofessor(1, "Dr P Smith")
    timetable.addprofessor(2, "Mrs E Mitchell")
    timetable.addprofessor(3, "Dr R Williams")
    timetable.addprofessor(4, "Mr A Thompson")

    # timetable.addmodule(1, "cs1", "Computer Science", np.array([1], int))
    # timetable.addmodule(2, "en1", "English", np.array([2], int))
    # timetable.addmodule(3, "ma1", "Maths", np.array([2], int))

    timetable.addmodule(1, "cs1", "Computer Science", np.array([1, 2], int))
    timetable.addmodule(2, "en1", "English", np.array([1, 3], int))
    timetable.addmodule(3, "ma1", "Maths", np.array([1, 2], int))
    timetable.addmodule(4, "ph1", "Physics", np.array([3, 4], int))
    timetable.addmodule(5, "hi1", "History", np.array([4], int))
    timetable.addmodule(6, "dr1", "Drama", np.array([1, 4], int))

    timetable.addgroup(1, 10, np.array([1,3,4], int))
    timetable.addgroup(2, 30, np.array([2, 3, 5, 6], int))
    timetable.addgroup(3, 18, np.array([3, 4, 5], int))
    timetable.addgroup(4, 25, np.array([1, 4], int))
    timetable.addgroup(5, 20, np.array([2, 3, 5], int))
    timetable.addgroup(6, 22, np.array([1, 4, 5], int))
    timetable.addgroup(7, 16, np.array([1, 3], int))
    timetable.addgroup(8, 18, np.array([2, 6], int))
    timetable.addgroup(9, 24, np.array([1, 6], int))
    timetable.addgroup(10, 25, np.array([3, 4], int))

    return timetable

if __name__ == "__main__":
    timetable = init_timetable()
    ga = GeneticAlgorithm(100, 0.01, 0.9, 2, 5)
    population = ga.initpopulation(timetable)
    ga.evalpopulation(population, timetable)
    #print(population.getindividuals()[0].getchromosome())

    generation = 1
    while not ga.is_terminationconditionmet(generation, 1000) \
        and not ga.is_terminationcontitionmetpop(population):

        print(f'G{generation} Best fitness: {population.getfittest(0).getfitness()}')
        #print(f"{population.getfittest(0).getchromosome()}")
        #print(population.getindividuals()[0].getchromosome())
        population = ga.crossoverpopulation(population)
        population = ga.mutatepopulation(population, timetable)
        ga.evalpopulation(population, timetable)

        generation += 1

    timetable.create_classes(population.getfittest(0))
    print(f"""
    Solution found in {generation} generations
    Final solution fitness: {population.getfittest(0).getfitness()}
    Clashes: {timetable.calc_clashes()}
    """)

    classes = timetable.getclasses()
    classindex = 1
    for bestclass in classes:
        print(f"""
        Class: {classindex}
        Module: {timetable.getmodule(bestclass.getmoduleid()).getmodulename()}
        Group: {timetable.getgroup(bestclass.getgroupid()).getgroupid()}
        Room: {timetable.getroom(bestclass.getroomid()).getroom_nmb()}
        Professor: {timetable.getprofessor(bestclass.getprofessorid()).getprofessorname()}
        Time: {timetable.gettimeslot(bestclass.gettimeslotid()).gettimeslot()}
        -----
        """)
        classindex += 1


