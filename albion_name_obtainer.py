from item_list import item_list_full
import requests
import json
import pandas as pd
from multiprocessing import Pool
from multiprocessing.dummy import Pool

def get_item_info(ITEM):
    URL = 'https://gameinfo.albiononline.com/api/gameinfo/items/' + ITEM + '/data'
    RESPONSE = requests.get(URL).content
    ITEM_FULL_INFOS = json.loads(RESPONSE.decode('utf-8'))
    return ITEM_FULL_INFOS

def handler(item_list):
    NAMES_LIST = []
    for item in item_list:
        try:
            ITEM_FULL_INFOS = get_item_info(item)
            if ITEM_FULL_INFOS['enchantments'] is not None:
                try:
                    CRAFT_REQUIREMENTS = ITEM_FULL_INFOS['craftingRequirements']
                    cont = 0
                except:
                    print('tchau')
                    ITEM_NAME = item
                    NAMES_LIST.append(ITEM_NAME)
        except:
            cont = 0
        if item_list.index(item) % 50 == 0:
            print(item_list.index(item),len(NAMES_LIST))
    return NAMES_LIST

item_list1 = item_list_full[0:550]
item_list2 = item_list_full[551:1120]
item_list3 = item_list_full[1121:1650]
item_list4 = item_list_full[1651:2241]
item_list5 = item_list_full[2242:2700]
item_list6 = item_list_full[2701:3362]
item_list7 = item_list_full[3363:3900]
item_list8 = item_list_full[3901:4483]
item_list9 = item_list_full[4484:5000]
item_list10 = item_list_full[5001:5550]
item_list11 = item_list_full[5551:6100]
item_list12 = item_list_full[6101:]

threads = 12
CRAFT_LIST = []
global X
global Y
global Z
global A
global B
global C
global D
global E
global F
global G
global H
global I
Pool_cmd = Pool(threads)
[X,Y,Z,A,B,C,D,E,F,G,H,I] = Pool_cmd.map(handler,[item_list1,item_list2,item_list3,item_list4,item_list5,item_list6,item_list7,item_list8,item_list9,item_list10,item_list11,item_list12])
CRAFT_LIST = X + Y + Z + A + B + C + D + E + F + G + H + I
print(CRAFT_LIST)
with open("COOKABLE.txt", "w") as output:
    output.write(str(CRAFT_LIST))


#def get_names(get_item_info(ITEM)):
#    CRAFTABLE = ITEM_FULL_INFOS['craftingRequirements']
#    POSSIBLE_ENCHANTMENTS = len(ITEM_FULL_INFOS['enchantments']['enchantments'])

#ITEM_LIST = ['T4_2H_BOW_HELL', 'T8_2H_LONGBOW_UNDEAD','T4_POTION_HEAL']
#ITEM_FULL_INFOS = []
#for item in ITEM_LIST:
#    INFO = get_item_info(item)
#    try:
#        ITEM_RELEVANT_INFO ={
#        'Name': INFO['localizedNames']['EN-US'],
#        'Focus_Points' : INFO['craftingRequirements']['craftingFocus'],
#        'Ingredient1': INFO['craftingRequirements']['craftResourceList'][0]['uniqueName'],
#        'Ingredient1_qty': INFO['craftingRequirements']['craftResourceList'][0]['count'],
#        'Ingredient2': INFO['craftingRequirements']['craftResourceList'][1]['uniqueName'],
#        'Ingredient2_qty': INFO['craftingRequirements']['craftResourceList'][1]['count'],
#        'Ingredient3': INFO['craftingRequirements']['craftResourceList'][2]['uniqueName'],
#        'Ingredient3_qty': INFO['craftingRequirements']['craftResourceList'][2]['count'],
#        'Ingredient4': INFO['craftingRequirements']['craftResourceList'][3]['uniqueName'],
#        'Ingredient4_qty': INFO['craftingRequirements']['craftResourceList'][3]['count'],
#        'Ingredient5': INFO['craftingRequirements']['craftResourceList'][4]['uniqueName'],
#        'Ingredient5_qty': INFO['craftingRequirements']['craftResourceList'][4]['count'],
#        'Ingredient6': INFO['craftingRequirements']['craftResourceList'][5]['uniqueName'],
#        'Ingredient6_qty': INFO['craftingRequirements']['craftResourceList'][5]['count']
#    }
#    except:
#        print('ops')
#    print(ITEM_RELEVANT_INFO)
#    ITEM_FULL_INFOS.append(INFO)


#my_df = pd.DataFrame(ITEM_FULL_INFOS)
#my_df.to_csv(r'Craft_albion')
