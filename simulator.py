import sqlite3

import requests

response = requests.get("https://api.dexie.space/v1/offers?offered_type=cat&requested_type=cat&compact=true&page_size=100&page=1");
# print(response.json());
conteggio = response.json()['count']

print('Numero di offerte trovate:' + str(conteggio))

con = sqlite3.connect("DB.db")
cur = con.cursor();
cur.execute('DELETE FROM offerteAttive')
con.commit();
con.close();

i = 1;
while i <= round(conteggio/100,0)+1:
    response = requests.get("https://api.dexie.space/v1/offers?offered_type=cat&requested_type=cat&compact=true&page_size=100&page=" + str(i));
    # print("https://api.dexie.space/v1/offers?compact=true&page_size=100&page="+str(i));
    # print(response.json());
    y = 0;
    while y <= 99:
        try:
            if len(response.json()['offers'][y]['offered'][0]) == 4 and len(
                    response.json()['offers'][y]['requested'][0]) == 4:
                con = sqlite3.connect("DB.db");
                cur = con.cursor();
                ##print(response.json()['offers'][y]['id']);
                stringa_query = "INSERT INTO offerteAttive VALUES('" + str(
                    response.json()['offers'][y]['offered'][0]['code']) + "'," + str(
                    response.json()['offers'][y]['offered'][0]['amount']) + ",'" + str(
                    response.json()['offers'][y]['requested'][0]['code']) + "'," + str(
                    response.json()['offers'][y]['requested'][0]['amount']) + ",0)";

                cur.execute(stringa_query);
                con.commit();
                con.close();

                print('Numero:' + str(i * 100 + y) + '/' + str(conteggio) + '->  REGISTRATA', end="\r");

            else:
                ##print(response.json()['offers'][y]['id']);
                print('Numero:' + str(i * 100 + y) + '/' + str(conteggio) + '->  NFT       ', end="\r");
        except:
            print('Numero: ' + str(i * 100 + y) + '/' + str(conteggio) + '->  STRANGE   ', end="\r");

        y += 1;
    ##time.sleep(5);
    ##print('Rimangono:'+ str(conteggio-i*100+y),end="\r");
    ##time.sleep(30);
    i += 1;

