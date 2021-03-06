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

        cons.setPlanSize(override)
        
        cons.run()
        if VERBOSE: print(f"{j} - progress = {(i/SIM_N) * 100} %")
        lootboxes_purchased.append(cons.getNumBought())
        instincts_triggered.append(cons.getInstinct())
        unique_items_acquired.append(len(cons.getUniqueAcquired()))
        final_plans.append(cons.getPlan())
        evaluations.clear()
        del(cons)
    
    return lootboxes_purchased, unique_items_acquired, instincts_triggered

    







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
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    
    os.chdir(PATH)

    averagesLootboxesTrue = []
    averagesUniquesTrue = []
    averagesLootboxesFalse = []
    averagesUniquesFalse = []
    totalInstsTrue = []

    temp1 = []
    temp2 = []
    temp3 = []
    
    for i in range(1,16):
        temp1, temp2, temp3 = simulator(j = i,override=i)
        averagesLootboxesTrue.append(avg(getItemsInsts(temp1,temp3,True)))
        averagesLootboxesFalse.append(avg(getItemsInsts(temp1,temp3,False)))
        averagesUniquesTrue.append(avg(getItemsInsts(temp2,temp3,True)))
        averagesUniquesFalse.append(avg(getItemsInsts(temp2,temp3,False)))
        totalInstsTrue.append(temp3.count(True))


        

    if VERBOSE: 
        print("Done! Making plots...")

    
    
    
    makeTwoFigs(averagesLootboxesTrue,averagesLootboxesFalse,"purchased_lootoboxes_mixed",0,75)
    # makeFig(averagesLootboxesTrue,"Lootboxes purchased","Lootboxes purchased | Instincts used","purchased_lootboxes_true",0,75)
    # makeFig(averagesLootboxesFalse,"Lootboxes purchased","Lootboxes purchased | Instincts not used","purchased_lootboxes_false",0,75)
    makeFig(averagesUniquesTrue,"Unique items acquired","Unique items acquired | Instincts used","uniques_acquired_true",0,18)
    makeFig(averagesUniquesFalse,"Unique items acquired","Unique items acquired | Instincts not used","uniques_acquired_false",0,18)
    makeFigInst(totalInstsTrue)
    # fig.show()
    
def makeFig(data,yID,title,filename,low,high):
    margin = mean_confidence_interval(data)
    temp2 = list(range(1,len(data)+1))
    dfLoot = pd.DataFrame(list(zip(data,temp2)),columns=[yID,"Plan size"])
    dfLoot["e"] = margin
    # dfLoot["e"] = 2
    fig = px.scatter(dfLoot,
        x = "Plan size",
        y = yID,
        title = title,
        error_y="e"
    )
    # fig.add_hline(y=median(temp),line_width=2,line_dash='dash',line_color="red",name="Median",annotation_text="Median",annotation_position="bottom right")
    fig.add_hline(y=avg(data),line_width=2,line_dash='dash',line_color="blue",name="Average",annotation_text="Average",annotation_position="bottom left")
    fig.update_layout(yaxis_range=[low,high])

    fig.write_image(f"{filename}.png")

def makeTwoFigs(data1,data2,filename,low,high):
    margin1 = mean_confidence_interval(data1)
    margin2 = mean_confidence_interval(data2)
    tempRange1 = list(range(1,len(data1)+1))
    tempRange2 = list(range(1,len(data2)+1))

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name = "Entraram em modo de instinto",
        x= tempRange1, y = data1,
        error_y=dict(type='data',symmetric=False,array=[margin1]*len(data1),arrayminus=marginCorrector(data1,margin1))
    ))

    fig.add_trace(go.Bar(
        name = "Não entraram em modo de instinto",
        x= tempRange2, y = data2,
        error_y=dict(type='data',symmetric=False,array=[margin2]*len(data2),arrayminus=marginCorrector(data2,margin2))
    ))

    fig.update_layout(
        title = "Número de lootboxes compradas por <br>tamanho de plano",
        xaxis_title="Tamanho de plano",
        yaxis_title="Número de lootboxes compradas",
        yaxis_range=[low,high],
        legend_orientation="h",
        legend_y=-0.25
    )

    fig.write_image(f"{filename}.png")

def makeFigInst(insts):
    temp = list(range(1,len(insts)+1))
    temp2 = list(map(lambda n: n/SIM_N * 100,insts))
    temp3 = list(map(lambda n: 100 - n,temp2))
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
    fig = go.Figure(
        data=[
            go.Bar(name='Consumidores que entraram em modo de instinto', x = temp, y=temp2),
            go.Bar(name='Consumidores que não entraram em modo de instinto', x = temp, y = temp3)
        ]
    )
    # fig.add_trace(go.Bar(
    #     name = "Percentage of Instincts used by Plan size",
    #     x = temp, y = temp2,
    #     error_y=dict(type='data',symmetric=False,array=[margin]*len(insts),arrayminus=marginCorrector(temp2,margin))
    # ))

    fig.update_layout(
        title = "Porcentagem de consumidores que entraram em modo de instinto por <br>tamanho de plano",
        xaxis_title="Tamanho de plano",
        yaxis_title="População total",
        yaxis_range=[0,100],
        barmode='stack',
        legend_orientation="h",
        legend_y=-0.25
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