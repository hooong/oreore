from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json, os
from oreore_project.settings import BASE_DIR
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def predict_month(request):
    if 'code' in request.POST:
        kcdcode = request.POST['code']
    filename = os.path.join(BASE_DIR,'data/disease_month_data/'+kcdcode+'_1601_1812.csv')
    data = pd.read_csv(filename)

    data_month = []

    for i in range(1,13):
        list_mon = []
        for m in [16,17,18]:
            list_mon.append(str(m)+'_'+str(i))

        data_mon = pd.DataFrame()
        for j in list_mon:
            data_mon.loc[:,j] = data[:22][j]
        
        data_mon = data_mon[1:].astype('int')
        data_month.append(data_mon.sum(axis=1)[1])


    # data 정규화 ( 0 ~ 100 )
    data_month = np.array(data_month)
    data_min = data_month.min()
    data_max = data_month.max()
    data_denom = data_max - data_min
    for i in range(len(data_month)):
        data_month[i] = (float(data_month[i] - data_min) / float(data_denom)) * 100
    data_mon_avg = zip(range(1,13),data_month)

    predict_mon = {}
    predict_mon['noti'] = {}
    for mon, data in data_mon_avg:
        if data >= 50:
            if kcdcode in predict_mon['noti']:
                predict_mon['noti'][kcdcode] = predict_mon['noti'][kcdcode] + ',' +str(mon) + '월'
            else:
                predict_mon['noti'][kcdcode] = str(mon) + '월'

    context = {"months":predict_mon}
    # month = json.dumps(predict_mon)

    return JsonResponse(predict_mon)
