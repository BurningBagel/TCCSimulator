from itertools import combinations
import random
from defs import *







class ConsumidorBDI:
    evals = []
    desires = []

    #Our "beliefs" module. Receives evaluations from outside and forwards them to the desire generator.
    def __init__(self,evals):
        self.evals = [item for item in evals]
        self.instinct = INSTINCT
        self.confidence = CONFIDENCE
        self.confidenceReset = self.confidence/CONFIDENCE_RESET
        self.instMod = INSTMOD
        self.confMod = CONFMOD
        self.instinctThreshold = INSTINCT_THRESHOLD
        self.indexAcquired = []
        self.intention = []
        self.desires = []
        self.numBought = 0
        self.plan = 0
        self.planSize = PLAN_SIZE
        if MERCY: self.mercyCounter = 10
        # random.seed(29092021)

    def run(self):
        self.desireGenerator()
        self.planner()
        #self.printResults()

    def printResults(self):
        print(f"Total lootboxes purchased: {self.numBought}")
        print(f"Instinct mode executed? {self.instinct < self.instinctThreshold}")
        print(f"Final plan count: {self.plan}")
        print(f"Unique items acquired: {self.indexAcquired}")

    #Desires are situations where the consumer would be happy, represented by the combined value of the items obtained
        # being higher than the amount spent obtaining it. A desire here is a large tuple containing tuples of index, evaluation pairs


    def subsetSum(self,subset):
        result = 0
        for item in subset:
            result += item[1]
        return result


    def desireGenerator(self):
        # for i in range(1,len(self.evals)+1):
        i = self.planSize
        
        for subset in combinations(enumerate(self.evals),i):
            total = self.subsetSum(subset) / i #Value of desire is tempered by amount of lootboxes required
            # if len(subset) == 0: 
            #     pass
            if total > PRICE * 1.5 and len(subset[0]) > 0:
                t = (list(subset),total)
                self.desires.append(t)
        
        #Gotta go through the evals vector to generate all combinations of evals, including their sum
        self.desires = sorted(self.desires, key = lambda tup: tup[1])
        self.desires.reverse()
        

    #Gives the next desire in order. Use next() in a try except StopIteration
    def intentionSelector(self):
        for item in self.desires:
            self.plan += len(item[0])
            yield item

    #The "plan" is how many lootboxes the consumer expects to need to buy before achieving their end goal
    #Planner can be called to make a new plan, which would constitute choosing the next desire in order 
    #After selecting the next intention, we would need to check which already purchased items are in it.
    #Planner calls executor which returns True if it achieved its goal, and False if not.
    def planner(self):
        try:
            self.intention = next(self.intentionSelector())
        except StopIteration:
            print("NO DESIRES!")
            return
        
        while self.executor() != True:
            self.confidence = self.confidenceReset
            temp = list(self.intention)
            temp.clear()
            self.intention = tuple(temp)        #TUPLES ARE IMMUTABLE! But lists are not! So in order to go to the next intention we must convert the current one into a list
            try:
                self.intention = next(self.intentionSelector())
            except StopIteration:
                print("RAN OUT OF DESIRES!")
                return
            
            for item in self.intention[0]:
                if item[0] in self.indexAcquired:
                    temp = list(self.intention[0])
                    temp.remove(item)
                    self.intention = (temp,sum(temp)) #tuples are weird
            if len(self.intention[0]) == 0: return 
                
        

    #We buy lootboxes, registering what we got
    def executor(self):
        
        while self.confidence >= CONFIDENCE_THRESHOLD or self.instinct < self.instinctThreshold: #INSTINCT TAKEOVER! Pessoa compra até conseguir completar uma intenção
            # if len(self.intention[0]) == 0: #Bodge
            #     return False
            self.numBought += 1
            # random.seed()
            if MERCY and self.mercyCounter == 0:
                purchased = random.choice(self.intention[0])            #purchased é uma tupla de índice e valor
                self.mercyCounter = 10
            else:
                purchased = random.choice(list(enumerate(self.evals)))
                if MERCY: self.mercyCounter-=1    
            
            
            #self.evals[purchased[0]] = 0                        #Agora que ganhei o item, ele não tem mais valor pra mim
            
            if purchased[0] not in self.indexAcquired:          #registra o item ganho
                self.indexAcquired.append(purchased[0])

            if purchased in self.intention[0]:                     #Plano está dando certo!
                self.confidence += CONFMOD
                self.intention[0].remove(purchased)     
            elif self.numBought > self.plan:                        #Plano NÃO está dando certo...
                self.confidence -= CONFMOD 

            if len(self.intention[0]) == 0:                    #Conseguimos!
                    return True 

        self.instinct -= INSTMOD                                #Perdemos confiança no plano...
        
        if self.instinct < INSTINCT_THRESHOLD and PERSON_TYPE == NON_GAMBLER:
             return True

        return False

    def getPlan(self):
        return self.plan

    def getUniqueAcquired(self):
        return self.indexAcquired

    def getInstinct(self):
        return self.instinct < INSTINCT_THRESHOLD

    def getNumBought(self):
        return self.numBought

    def getDesires(self):
        return self.desires

    def getEvals(self):
        return self.evals

    def getConfindence(self):
        return self.confidence
    
    def getConfidenceReset(self):
        return self.confidenceReset

    def getInstinctThreshold(self):
        return self.instinctThreshold

    def getPlanSize(self):
        return self.planSize

    def setPlanSize(self,new):
        self.planSize = new

    def setInstinctThreshold(self,new):
        self.instinctThreshold = new

    def setConfidenceReset(self,new):
        self.confidenceReset = new

    def setEvals(self,new):
        self.evals.clear()
        self.evals = [item for item in new]
    
    def setInstinct(self,new):
        self.instinct = new

    def setConfidence(self,new):
        self.confidence = new
