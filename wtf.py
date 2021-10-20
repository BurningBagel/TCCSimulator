import numpy as np
import scipy.stats
import pandas as pd
import plotly.express as px

from test import makeFig

SIM_N = 5



def makeFigInst(insts):
    margin = mean_confidence_interval(insts)
    temp = list(range(1,len(insts)+1))
    temp2 = list(map(lambda n: n/SIM_N * 100,insts))
    df = pd.DataFrame(list(zip(temp2,temp)),columns=["Percentage of Instincts used","Set"])
    #df["e"] = margin
    # df["e"] = 2
    fig = px.bar(df,
        x = "Set",
        y = "Percentage of Instincts used",
        title = "Percentage of Instincts used by set",
        error_y=dict(type='data',array=[margin]*len(temp2),arrayminus=marginCorrector(temp2,margin),symmetric=False)
    )

    fig.show()

def marginCorrector(input,margin):
    result = []
    for item in input:
        if item < margin:
            result.append(item)
        else:
            result.append(margin)

def mean_confidence_interval(data,confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    se = scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1+confidence)/2.,n-1)
    return h




makeFigInst([1,2,3,4,5,6])