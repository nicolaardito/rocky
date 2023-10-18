import sqlite3
import requests

#parametri

token = 'ROCKY'

#Conta numero di offerte in cui si offre ROCKY

response = requests.get("https://api.dexie.space/v1/offers?offered_type=cat&requested_type=cat&compact=true&page_size=100&page=1&offered=ROCKY");
conteggio1 = response.json()['count']
print('Numero di offerte trovate:' + str(conteggio1))

#Conta numero di offerte in cui si chiede ROCKY

response = requests.get("https://api.dexie.space/v1/offers?offered_type=cat&requested_type=cat&compact=true&page_size=100&page=1&requested=ROCKY");
conteggio2 = response.json()['count']
print('Numero di offerte trovate:' + str(conteggio2))

#Svuota il DB

con = sqlite3.connect("DB.db")
cur = con.cursor();
cur.execute('DELETE FROM offerteAttiveA')
cur.execute('DELETE FROM offerteAttiveB')
con.commit();
con.close();
print('Database Resettato')

#Inserisce nel DB le richieste derivanti dal chiedere ROCKY

i = 1;
while i <= round(conteggio1/100,0)+1:
    response = requests.get("https://api.dexie.space/v1/offers?offered_type=cat&offered=ROCKY&requested_type=cat&compact=true&page_size=100&page=" + str(i));
    y = 0;
    while y <= 99:
        try:
            if len(response.json()['offers'][y]['offered'][0]) == 4 and len(
                    response.json()['offers'][y]['requested'][0]) == 4:
                con = sqlite3.connect("DB.db");
                cur = con.cursor();
                stringa_query = "INSERT INTO offerteAttiveA VALUES('" + str(
                    response.json()['offers'][y]['offered'][0]['code']) + "'," + str(
                    response.json()['offers'][y]['offered'][0]['amount']) + ",'" + str(
                    response.json()['offers'][y]['requested'][0]['code']) + "'," + str(
                    response.json()['offers'][y]['requested'][0]['amount']) + ",0)";

                cur.execute(stringa_query);
                con.commit();
                con.close();

                print('Numero:' + str(i * 100 + y) + '/' + str(conteggio1) + '->  REGISTRATA', end="\r");

            else:
                print('Numero:' + str(i * 100 + y) + '/' + str(conteggio1) + '->  NFT       ', end="\r");
        except:
            print('Numero: ' + str(i * 100 + y) + '/' + str(conteggio1) + '->  STRANGE   ', end="\r");

        y += 1;
    i += 1;


#Inserisce nel DB le richieste derivanti dal cedere ROCKY

i = 1;
while i <= round(conteggio2/100,0)+1:
    response = requests.get("https://api.dexie.space/v1/offers?offered_type=cat&requested=ROCKY&requested_type=cat&compact=true&page_size=100&page=" + str(i));
    y = 0;
    while y <= 99:
        try:
            if len(response.json()['offers'][y]['offered'][0]) == 4 and len(
                    response.json()['offers'][y]['requested'][0]) == 4:
                con = sqlite3.connect("DB.db");
                cur = con.cursor();
                stringa_query = "INSERT INTO offerteAttiveB VALUES('" + str(
                    response.json()['offers'][y]['offered'][0]['code']) + "'," + str(
                    response.json()['offers'][y]['offered'][0]['amount']) + ",'" + str(
                    response.json()['offers'][y]['requested'][0]['code']) + "'," + str(
                    response.json()['offers'][y]['requested'][0]['amount']) + ",0)";

                cur.execute(stringa_query);
                con.commit();
                con.close();

                print('Numero:' + str(i * 100 + y) + '/' + str(conteggio1) + '->  REGISTRATA', end="\r");

            else:
                print('Numero:' + str(i * 100 + y) + '/' + str(conteggio1) + '->  NFT       ', end="\r");
        except:
            print('Numero: ' + str(i * 100 + y) + '/' + str(conteggio1) + '->  STRANGE   ', end="\r");

        y += 1;
    i += 1;

# Cancella dal DB le richieste non mie

con = sqlite3.connect("DB.db")
cur = con.cursor();
cur.execute('DELETE FROM offerteAttiveA where offered_amount <> 1 ')
cur.execute('DELETE FROM offerteAttiveA where requested_amount not in("0.0001")')
cur.execute('DELETE FROM offerteAttiveB where offered_amount not in("0.0001")')
cur.execute('DELETE FROM offerteAttiveB where requested_amount <> 1')
con.commit();
con.close();
print('Cancellate Richieste non di Ardito')

# Conta offerte attive del primo tipo

con = sqlite3.connect("DB.db");
cur = con.cursor();
query = 'select * from offerteAttiveA';
cur.execute(query);
records = cur.fetchall();
num_record_tipo1 = len(records);
print('Numero di richieste di tipo 1 ==> '+str(num_record_tipo1));
con.commit();
con.close();

# Conta offerte attive del secondo tipo

con = sqlite3.connect("DB.db");
cur = con.cursor();
query = 'select * from offerteAttiveA';
cur.execute(query);
records = cur.fetchall();
num_record_tipo2 = len(records);
print('Numero di richieste di tipo 2 ==> '+str(num_record_tipo2));
con.commit();
con.close();

