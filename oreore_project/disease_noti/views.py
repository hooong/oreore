from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json, os
from oreore_project.settings import BASE_DIR

def predict_month(request):
    filename = os.path.join(BASE_DIR,'data/disease_month_data/j00_1601_1812.csv')
    j00_data = pd.read_csv(filename)

    data_month = []

    for i in range(1,13):
        list_mon = []
        for m in [16,17,18]:
            list_mon.append(str(m)+'_'+str(i))

        data_mon = pd.DataFrame()
        for j in list_mon:
            data_mon.loc[:,j] = j00_data[:22][j]
        
        data_mon = data_mon[1:].astype('int')
        data_month.append(data_mon.sum(axis=1)[1])


    data_month = np.array(data_month)
    data_mon_avg = (data_month // 3) // 10000   # 0~100까지의 값만 사용하기 위해 나눔
    data_mon_avg = zip(range(1,13),data_mon_avg)

    predict_mon = []
    for mon, data in data_mon_avg:
        if data >= 70:
            predict_mon.append([mon,data])

    context = {"months":predict_mon}

    return render(request,"noti.html",context)