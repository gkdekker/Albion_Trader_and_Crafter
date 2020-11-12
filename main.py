import requests
from item_list import item_list_full
import json
from multiprocessing import Pool
from multiprocessing.dummy import Pool
import pandas as pd
import re
import time

def handler(lista):
    PRICE_LIST = []
    X = []
    Y = []
    Z = []
    item_list1 = item_list_full[:2200]
    item_list2 = item_list_full[2201:4400]
    item_list3 = item_list_full[4401:]
    Pool_cmd = Pool(3)
    [X,Y,Z] = Pool_cmd.map(get_item_info,[item_list1,item_list2,item_list3])
    PRICE_LIST = X + Y + Z
    my_df = pd.DataFrame(data=PRICE_LIST)[['item_id','buy_price_max','city','sell_price_min','sell_price_max']]
    my_df.to_csv(r'Albion_Prices.csv')
    return

def get_item_info(lista):
    starttime = time.time()
    PLIST = []
    chunk_list = chunk_item(lista,200)
    for item in chunk_list:
        try:
            DADOS = city_get(item)
            PLIST.extend(DADOS)
        except:
            print(DADOS)
        print(chunk_list.index(item),"--- %s seconds ---" % (time.time() - starttime))
    return PLIST

def chunk_item(lista,size):
    chunk_item = []
    while len(lista) > 0:
        chunkname = ''
        chunk = lista[0:size-1]
        for itens in chunk:
            chunkname = chunkname + itens + ','
        chunk_item.append(chunkname) 
        lista = lista[size:]
    return chunk_item   

def city_get(ITEM):
    URL = 'https://www.albion-online-data.com/api/v2/stats/prices/' + ITEM + '?locations=Caerleon,lymhurst,bridgewatch,martlock,fortsterling,thetford&qualities=1'
    R = requests.get(URL).content
    RESPONSE = json.loads(R.decode('utf-8'))
    return RESPONSE

handler(item_list_full)