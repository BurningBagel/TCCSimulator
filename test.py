import random
import os
from functools import reduce
from supFunc import avg
import consumidorBDI
from defs import *
import plotly.express as px
import plotly.graph_objects as go
#from statistics import median
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


def simulator(j,override = 0):
    

    lootboxes_purchased = []
    instincts_triggered = []
    unique_items_acquired = []
    final_plans = []


    

    # if not os.path.exists(f"{OVERWRITE}"): os.mkdir(f"RESET")

    for i in range(SIM_N):
        probGenerator(GEN,N)
        cons = consumidorBDI.ConsumidorBDI(evaluations)

        # cons.setPlanSize(override)
        
        cons.run()
        if VERBOSE: print(f"{j} - progress = {(i/SIM_N) * 100} %")
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
    se = scipy.stats.sem(a)
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
    #random.seed(29092021)
    random.seed()
    os.chdir("C:/Users/Admin/Desktop/LivrosUnB/TCC/SimPy/FINAL30/MERCY")

    averagesLootboxesTrue = []
    averagesUniquesTrue = []
    averagesLootboxesFalse = []
    averagesUniquesFalse = []
    totalInstsTrue = []

    temp1 = []
    temp2 = []
    temp3 = []
    
    for i in range(30):
        temp1, temp2, temp3 = simulator(j = i)
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

    if VERBOSE: 
        print("Done! Making plots...")

    
    
    
    
    makeFig(averagesLootboxesTrue,"Lootboxes purchased","Lootboxes purchased | Instincts used","purchased_lootboxes_true",0,75)
    makeFig(averagesLootboxesFalse,"Lootboxes purchased","Lootboxes purchased | Instincts not used","purchased_lootboxes_false",0,75)
    makeFig(averagesUniquesTrue,"Unique items acquired","Unique items acquired | Instincts used","uniques_acquired_true",0,18)
    makeFig(averagesUniquesFalse,"Unique items acquired","Unique items acquired | Instincts not used","uniques_acquired_false",0,18)
    makeFigInst(totalInstsTrue)
    # fig.show()
    
def makeFig(data,yID,title,filename,low,high):
    margin = mean_confidence_interval(data)
    temp2 = list(range(1,len(data)+1))
    dfLoot = pd.DataFrame(list(zip(data,temp2)),columns=[yID,"Set"])
    dfLoot["e"] = margin
    # dfLoot["e"] = 2
    fig = px.scatter(dfLoot,
        x = "Set",
        y = yID,
        title = title,
        error_y="e"
    )
    # fig.add_hline(y=median(temp),line_width=2,line_dash='dash',line_color="red",name="Median",annotation_text="Median",annotation_position="bottom right")
    fig.add_hline(y=avg(data),line_width=2,line_dash='dash',line_color="blue",name="Average",annotation_text="Average",annotation_position="bottom left")
    fig.update_layout(yaxis_range=[low,high])

    fig.write_image(f"{filename}.png")

def makeFigInst(insts):
    temp = list(range(1,len(insts)+1))
    temp2 = list(map(lambda n: n/SIM_N * 100,insts))
    margin = mean_confidence_interval(temp2)
    # df = pd.DataFrame(list(zip(temp2,temp)),columns=["Percentage of Instincts used","Set"])
    #df["e"] = margin
    # df["e"] = 2
    # fig = px.bar(df,
    #     x = "Set",
    #     y = "Percentage of Instincts used",
    #     title = "Percentage of Instincts used by plan size",
    #     error_y=dict(type='data',array=[margin]*len(insts),arrayminus=marginCorrector(temp2,margin),symmetric=False)
    # )
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name = "Percentage of Instincts used by Set",
        x = temp, y = temp2,
        error_y=dict(type='data',symmetric=False,array=[margin]*len(insts),arrayminus=marginCorrector(temp2,margin))
    ))

    fig.update_layout(
        title = "Percentage of Instincts used by Set",
        xaxis_title="Set",
        yaxis_title="Percentage of instincts used"
    )

    fig.write_image("percentInsts.png")

def marginCorrector(input,margin):
    result = []
    for item in input:
        if item < margin:
            result.append(item)
        else:
            result.append(margin)
    return result


if __name__ == "__main__":
    main()