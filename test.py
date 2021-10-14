from decimal import localcontext
import random
import os
from functools import reduce
from supFunc import avg, normalize
import consumidorBDI
from defs import *
import plotly.express as px
from statistics import median
import pandas as pd
import numpy as np
import scipy.stats

VERBOSE = True

evaluations = []

def probGenerator(mode,n):
    
    for i in range(n):
        if mode == UNIFORM: evaluations.append(round(random.uniform(0,2),4))
        elif mode == LOG: evaluations.append(round(random.lognormvariate(0,1),4)) #Ver se estes parâmetros estão certos
        elif mode == EXPO: evaluations.append(round(random.expovariate(1),4))


def simulator(items):
    

    lootboxes_purchased = []
    instincts_triggered = []
    unique_items_acquired = []
    final_plans = []


    

    # if not os.path.exists(f"{OVERWRITE}"): os.mkdir(f"RESET")

    for i in range(SIM_N):
        probGenerator(GEN,items)
        cons = consumidorBDI.ConsumidorBDI(evaluations)
        cons.run()
        if VERBOSE: print(f"progress = {(i/SIM_N) * 100} %")
        lootboxes_purchased.append(cons.getNumBought())
        instincts_triggered.append(cons.getInstinct())
        unique_items_acquired.append(len(cons.getUniqueAcquired()))
        final_plans.append(cons.getPlan())
        evaluations.clear()
        del(cons)
    
    return lootboxes_purchased, unique_items_acquired, instincts_triggered

    


#     temp = getItemsInsts(lootboxes_purchased,instincts_triggered,True)
#     temp2 = list(range(1,len(temp)+1))
#     df = pd.DataFrame(list(zip(temp,temp2)),columns=['Number of lootboxes purchased','iteration'])
#     fig = px.scatter(df,
#         x='iteration',
#         y='Number of lootboxes purchased',
#         title=f"Lootboxes Purchased | Instincts used",
#     )
#     makeFig(fig, temp,"lootboxes_purchased_true",OVERWRITE)

#  #--------------------------------------------------
#     temp.clear()
#     temp = getItemsInsts(lootboxes_purchased,instincts_triggered,False)
#     temp2 = list(range(1,len(temp)+1))
#     df = pd.DataFrame(list(zip(temp,temp2)),columns=['Number of lootboxes purchased','iteration'])
#     fig = px.scatter(df,
#         x='iteration',
#         y='Number of lootboxes purchased',
#         title=f"Lootboxes Purchased | Instincts not used"
#     )
#     makeFig(fig, temp,"lootboxes_purchased_false",OVERWRITE)

#  #--------------------------------------------------------------------------------------------
#     temp.clear()
#     temp = getItemsInsts(unique_items_acquired,instincts_triggered,True)
#     temp2 = list(range(1,len(temp)+1))
#     df = pd.DataFrame(list(zip(temp,temp2)),columns=['Unique items acquired','iteration'])
#     fig = px.scatter(df,
#         x = 'iteration',
#         y='Unique items acquired',
#         title=f"Unique items acquired | Instincts used"
#     )
#     makeFig(fig, temp,"unique_items_true",OVERWRITE)

#  #---------------------------------------
#     temp.clear()
#     temp = getItemsInsts(unique_items_acquired,instincts_triggered,False)
#     temp2 = list(range(1,len(temp)+1))
#     df = pd.DataFrame(list(zip(temp,temp2)),columns=['Unique items acquired','iteration'])
#     fig = px.scatter(df,
#         x = 'iteration',
#         y='Unique items acquired',
#         title=f"Unique items acquired | Instincts not used"
#     )
#     makeFig(fig, temp,"unique_items_false",OVERWRITE)

#  #---------------------------------------------------------------------------------------------
#     temp.clear()
#     temp = ['True','False']
#     temp2 = [instincts_triggered.count(True),instincts_triggered.count(False)]
#     df = pd.DataFrame(list(zip(temp,temp2)), columns=['key','value'])
#     fig = px.pie(df,
#         values='value',
#         names='key',
#         title=f"Instincts triggered"
#     )
#     # fig.show()
#     fig.write_image(f"{OVERWRITE}/instincts_triggered.png")





#Returns error margin
def mean_confidence_interval(data,confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1+confidence)/2.,n-1)
    return h




    


def getItemsInsts(list,insts,which):
    result = []
    for x,y in enumerate(list):
        if insts[x] == which:
            result.append(y)
    if len(result) == 0: return [0] * 100
    return result




def main():
    random.seed(29092021)
    os.chdir("C:/Users/Admin/Desktop/LivrosUnB/TCC/SimPy/FINAL")

    averagesLootboxesTrue = []
    averagesUniquesTrue = []
    averagesLootboxesFalse = []
    averagesUniquesFalse = []
    totalInstsTrue = []

    temp1 = []
    temp2 = []
    temp3 = []
    
    for i in range(1,16):
        temp1, temp2, temp3 = simulator(i)
        averagesLootboxesTrue.append(avg(getItemsInsts(temp1,temp3,True)))
        averagesLootboxesFalse.append(avg(getItemsInsts(temp1,temp3,False)))
        averagesUniquesTrue.append(avg(getItemsInsts(temp2,temp3,True)))
        averagesUniquesFalse.append(avg(getItemsInsts(temp2,temp3,False)))
        totalInstsTrue.append(temp3.count(True))


        #Find averages and confidence intervals of each vector
        #vline and hrect(y0=lower,y1=upper,opacity=0.2,fillcolor="blue")

        # Consolidar os gráficos do Plan size em 4 gráficos, dois para os lootbox purchased true e false. Eixo x com o tamanho do plan size. Eixo y com a média obtida e intervalo de confiança.
        # dois para unique itens true e false. Eixo x com o tamanho do plan size. Eixo y com a média obtida e intervalo de confiança.

        # Fazer o mesmo para instinct e confidence. ?????

    if VERBOSE: print("Done! Making plots...")

    
    
    
    
    makeFig(averagesLootboxesTrue,"Lootboxes purchased","Lootboxes purchased | Instincts used","purchased_lootboxes_true")
    makeFig(averagesLootboxesFalse,"Lootboxes purchased","Lootboxes purchased | Instincts not used","purchased_lootboxes_false")
    makeFig(averagesUniquesTrue,"Unique items acquired","Unique items acquired | Instincts used","uniques_acquired_true")
    makeFig(averagesUniquesFalse,"Unique items acquired","Unique items acquired | Instincts not used","uniques_acquired_false")
    makeFigInst(totalInstsTrue)
    # fig.show()
    
def makeFig(data,yID,title,filename):
    margin = mean_confidence_interval(data)
    temp2 = list(range(1,len(data)+1))
    dfLoot = pd.DataFrame(list(zip(data,temp2)),columns=[yID,"Plan size"])
    dfLoot["e"] = margin
    fig = px.scatter(dfLoot,
        x = "Plan size",
        y = yID,
        title = title,
        error_y="e"
    )
    # fig.add_hline(y=median(temp),line_width=2,line_dash='dash',line_color="red",name="Median",annotation_text="Median",annotation_position="bottom right")
    fig.add_hline(y=avg(data),line_width=2,line_dash='dash',line_color="blue",name="Average",annotation_text="Average",annotation_position="bottom left")
    fig.update_layout(yaxis_range=[8,35])

    fig.write_image(f"{filename}.png")

def makeFigInst(insts):
    margin = mean_confidence_interval(insts)
    temp = list(range(1,len(insts)+1))
    df = pd.DataFrame(list(zip(insts,temp)),columns=["Percentage of Instincts used","Plan size"])
    df["e"] = margin
    fig = px.bar(df,
        x = "Plan size",
        y = "Percentage of Instincts used",
        title = "Percentage of Instincts used by plan size",
        error_y="e"
    )

    fig.write_image("percentInsts.png")


if __name__ == "__main__":
    main()