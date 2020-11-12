import requests
from item_list import COST_LIST
from multiprocessing import Pool
from multiprocessing.dummy import Pool
import pandas as pd
import re
import time

def handler(lista):
    PLIST = []
    for item in lista:
        DADOS = city_get(item)
        try:
            ITEM_PROPERTIES = get_name_and_price_properties_json(DADOS)
            PLIST.append(ITEM_PROPERTIES)
        except:
            print(DADOS)
        if lista.index(item) % 60 == 0:
            print(lista.index(item),len(PLIST),"--- %s seconds ---" % (time.time() - starttime))
    return PLIST

def city_get(ITEM):
    URL = 'https://www.albion-online-data.com/api/v2/stats/view/' + ITEM + '?locations=lymhurst&qualities=0'
    R = requests.get(URL).text
    return R

def get_name_and_price_properties_json(DADOS):
    TD_LENGHT = 4
    FIELD_POS_IN = [m.start() for m in re.finditer('<td>', DADOS)]
    FIELD_POS_OUT = [m.start() for m in re.finditer('</td>', DADOS)]
    NAME = DADOS[FIELD_POS_IN[0] + TD_LENGHT:FIELD_POS_OUT[0]]
    try:
        BUY_PRICE = int(DADOS[FIELD_POS_IN[3] + TD_LENGHT:FIELD_POS_OUT[3]])
    except:
        BUY_PRICE = 0
    try:
        SELL_PRICE = int(DADOS[FIELD_POS_IN[9] + TD_LENGHT:FIELD_POS_OUT[9]])
    except:
        SELL_PRICE = 0

    ITEM_PROPERTIES = {
    'NAME' : NAME,
    'BUY_PRICE' : BUY_PRICE,
    'SELL_PRICE' : SELL_PRICE
    }
    return ITEM_PROPERTIES

item_list1 = COST_LIST[0:2370]
item_list2 = COST_LIST[2371:4745]

#PRICE_LIST = []
#X = []
#Y = []
#Z = []
starttime = time.time()
#Pool_cmd = Pool(2)
#[X,Y] = Pool_cmd.map(handler,[item_list1,item_list2])
#PRICE_LIST = X + Y
PRICE_LIST = handler(COST_LIST)
my_df = pd.DataFrame(PRICE_LIST)
my_df.to_csv(r'Craft Prices.csv')
print('deu baooo')