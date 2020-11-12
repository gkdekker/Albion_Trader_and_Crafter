from item_list import CRAFTABLE_LIST
import requests
import json
import pandas as pd
from multiprocessing import Pool
from multiprocessing.dummy import Pool

def get_item_info(ITEM):
    URL = 'https://gameinfo.albiononline.com/api/gameinfo/items/' + ITEM + '/data'
    RESPONSE = requests.get(URL).content
    ITEM_FULL_INFOS = json.loads(RESPONSE.decode('utf-8'))
    try:
        QTY_ENCHANTMENTS = len(ITEM_FULL_INFOS['enchantments']['enchantments'])
        QTY_INGREDIENTS_OF_ENCHANTMENTS = len(ITEM_FULL_INFOS['enchantments']['enchantments'][QTY_ENCHANTMENTS-1]['craftingRequirements']['craftResourceList'])
    except:
        QTY_ENCHANTMENTS = 0
        QTY_INGREDIENTS_OF_ENCHANTMENTS = 0
    try:
        QTY_INGREDIENTS = len(ITEM_FULL_INFOS['craftingRequirements']['craftResourceList'])
    except:
        QTY_INGREDIENTS = len(ITEM_FULL_INFOS['enchantments']['enchantments'][QTY_ENCHANTMENTS-1]['craftingRequirements']['craftResourceList'])
    return [ITEM_FULL_INFOS, QTY_INGREDIENTS, QTY_ENCHANTMENTS,QTY_INGREDIENTS_OF_ENCHANTMENTS]

def item_IDs(ITEM,QTY_ENCHANTMENT):
    ID_LAYOUT = {
        0: [ITEM['uniqueName']],
        1: [ITEM['uniqueName'],ITEM['uniqueName']+'@1'],
        2: [ITEM['uniqueName'],ITEM['uniqueName']+'@1',ITEM['uniqueName']+'@2'],
        3: [ITEM['uniqueName'],ITEM['uniqueName']+'@1',ITEM['uniqueName']+'@2',ITEM['uniqueName']+'@3']
    }
    ITENS = ID_LAYOUT[QTY_ENCHANTMENT]
    return ITENS

def item_craft_data(ITEM_ID,ITEM,QTY_INGREDIENTS,QTY_INGREDIENTS_OF_ENCHANTMENTS):
    ITEM_RELEVANT_INFO = [{
        'ID': ITEM_ID[0],
        'Name': ITEM['localizedNames']['EN-US'],
        'Focus_Points' : ITEM['craftingRequirements']['craftingFocus']
    }]
    x = 1
    while x <= QTY_INGREDIENTS:
        ITEM_RELEVANT_INFO[0]['Ingredient'+str(x)] = ITEM['craftingRequirements']['craftResourceList'][x-1]['uniqueName']
        ITEM_RELEVANT_INFO[0]['qty'+str(x)] = ITEM['craftingRequirements']['craftResourceList'][x-1]['count']
        x +=1
    while len(ITEM_ID)>len(ITEM_RELEVANT_INFO):
        ITEM_ENCHANTMENT_INFO = [{
        'ID': ITEM_ID[len(ITEM_RELEVANT_INFO)],
        'Name': ITEM['localizedNames']['EN-US'],
        'Focus_Points' : ITEM['enchantments']['enchantments'][len(ITEM_RELEVANT_INFO)-1]['craftingRequirements']['craftingFocus']
        }]
        y=1
        while y <= QTY_INGREDIENTS_OF_ENCHANTMENTS:
            ITEM_ENCHANTMENT_INFO[0]['Ingredient'+str(y)] = ITEM['enchantments']['enchantments'][len(ITEM_RELEVANT_INFO)-1]['craftingRequirements']['craftResourceList'][y-1]['uniqueName']
            ITEM_ENCHANTMENT_INFO[0]['qty'+str(y)] = ITEM['enchantments']['enchantments'][len(ITEM_RELEVANT_INFO)-1]['craftingRequirements']['craftResourceList'][y-1]['count']
            y +=1
        ITEM_RELEVANT_INFO.extend(ITEM_ENCHANTMENT_INFO)
    return ITEM_RELEVANT_INFO

def handler(ITEM_LIST):
    ITEM_RECIPE = []
    conterro = 0
    for item in ITEM_LIST:
        try:
            info = get_item_info(item)
            ids = item_IDs(info[0],info[2])
            data = item_craft_data(ids,info[0],info[1],info[3])
            ITEM_RECIPE.extend(data)
        except:
            conterro +=1
            print(conterro)
        if ITEM_LIST.index(item) % 50 == 0:
            print(ITEM_LIST.index(item),len(ITEM_RECIPE))
    my_df = pd.DataFrame(ITEM_RECIPE)
    my_df.to_csv(r'Receitas Boladonas do Dekker.csv')
    return

handler(CRAFTABLE_LIST)