import json
cj=['ZYW6PN','P1BM42','QGVXNI','397LAI','DZMM2H','EXAU5Y','SSYQKO','9LSL26','VJ9LQU','JO1DNH','BB1CP6','Y6ZSYT','WZ1K5G','H6248Z','PLC4IQ','M5H3LA','Q6ZJF5','6S4G03','QJ1MQU','4I7FDS','LOBTL7','KJYMGI','GOUJ35','UN2B1Z','U05E9G','ET9R4I','CAKQ41','J41YRG','29YV0A','WQ7HEA','MEC4C9','A0LDVP','4YYCYY','HT1BLP','TGEHDX','C6RZCJ','E2N70Z','F93TP1','2GGI6P','YICYKU']
d={
'codes':{
'ADMIN2024':{'duree':36500,'nom':'Administrateur','actif':True,'admin':True},
'5BW6MGSX':{'duree':365,'nom':'TETUANUI HEINI','actif':True,'email':'tetuanuiheini@gmail.com'},
'CPFRD66H':{'duree':365,'nom':'TETUANUI HEINI','actif':True,'email':'tetuanuiheini@gmail.com'}
},
'sessions':{},
'ventes':[
{'id':'0750a175','jeu':'1 DOLLAR','code_org':'CPFRD66H','paiement_statut':'valide','pack':100,'serie':'1','total':800,'pdf_url':'/api/pdf/2d18aba6193fa7890f74d558f62de9c4','token_doc':'593e4ad2ebb8b10987850aaa64358483','date':'2026-06-11T23:24:25'},
{'id':'05947ccc','jeu':'500 FRANCS','code_org':'CPFRD66H','paiement_statut':'valide','pack':100,'serie':'1','total':800,'pdf_url':'/api/pdf/bbdf9ab590e8aa1c8575dd742ba72f46','token_doc':'4631a276b63f94d72182597ee7a187d6','date':'2026-06-11T23:23:24'},
{'id':'77644521','jeu':'4 COINS','code_org':'CPFRD66H','paiement_statut':'valide','pack':100,'serie':'1','total':800,'pdf_url':'/api/pdf/6a80ecbd07be8597c833680678e6d7f6','token_doc':'5769cffac19c49e7a62c983b0dad7f14','date':'2026-06-11T23:21:27'},
{'id':'566ea553','code_org':'5BW6MGSX','jeu':'40 BOULES','pack':100,'serie':'1','paiement_statut':'valide','pdf_url':'/api/pdf/566ea55354935671','date':'2026-06-11T05:53','total':670},
{'id':'6de5174c','code_org':'5BW6MGSX','jeu':'40 BOULES','pack':100,'serie':'101','paiement_statut':'valide','pdf_url':'/api/pdf/6de5174c5b17a3cf','date':'2026-06-11T06:11','total':670}
],
'tickets':[{'id':c,'code_acheteur':c,'acheteur':'Joueur','jeu':'','serie':'','pdf_url':None,'page_debut':None,'page_fin':None,'code_org':'CPFRD66H','prix':0,'actif':True} for c in cj],
'commandes_tickets':[],
'commandes_pions':[],
'commandes_pions_joueurs':[],
'pions_org':{},
'pions_joueurs':{},
'micro_audio':{},
'tirage':[],
'coches':{},
'alertes_bingo':[]
}
json.dump(d,open('/data/ticketbingo_data.json','w'),ensure_ascii=False)
print('TOUT RESTAURE! Codes:'+str(len(d['codes']))+' Ventes:'+str(len(d['ventes']))+' Joueurs:'+str(len(d['tickets'])))
