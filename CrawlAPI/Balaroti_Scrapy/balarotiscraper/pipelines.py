# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:58:50 2024

@author: ArthurRodrigues

O objsetivo de criar pipelines é conseguir lidar com o que está sendo extraído
da internet de forma mais objetiva e deixar o código mais limpo e facilmente
editável.
Nesse caso, utilizo classes para armazenar as minhas buscas ou em um baco de 
dados em um servidor, ou num simples arquivo CSV. 

"""


from balarotiscraper.settings import out_path, today
import csv
## Storing to DB
#import mysql.connector ## MySQL
import psycopg2 ## Postgres


        
class SavingBalaDB(object):
    """
    Aqui salvamos as nossas buscas em um banco de dados Postgre Server. 
    Nesse casoé um servidor local, entretanto pode ser facilmente modificado
    para outro servidor na função 'create_connection'. 
    
    """

    def __init__(self):
        self.create_connection()
        

    def create_connection(self):
        conn = psycopg2.connect(
            host="localhost",
            database="scrapys",
            user="postgres",
            password="123456")
        return conn    


    def process_item(self, item, spider):
        self.store_in_db(item)
        #we need to return the item below as scrapy expects us to!
        return item


    def store_in_db(self, item):
        conn = self.create_connection()
        curr = conn.cursor()
        for e,p,u in zip(item["eans"],item["price"],item["url"]):
            curr.execute("""INSERT INTO public."Balaroti" ("ean", "price", "url") VALUES (%s,%s,%s);""", ( #, urlAPI, jsons) VALUES (%s, %s, %s);""", (
                e,#item["eans"],#[0],
                p,#item["price"],#[0],
                u,#item["url"],#[0]
            ))
            conn.commit()  
        
class SavingBalaCSV(object):
    """
    Aqui salvamos as nossas buscas em um arquivo CSV
    
    """

    
    def process_item(self, item, spider):
        self.store_in_csv(item)
        #we need to return the item below as scrapy expects us to!
        return item


    def store_in_csv(self, item):
        

        # Cria o arquivo CSV
        with open(out_path + f'Balarotti_{today}.csv', "w", newline="", encoding="utf-8") as f:
            # Especifica o separador como ponto e vírgula
            csv_writer = csv.writer(f, delimiter=';')
            titulo = ['EAN','Price','URL']
            csv_writer.writerow(titulo)
            
            
            for e,p,u in zip(item["eans"],item["price"],item["url"]):
                linha = [e,p,u]
                csv_writer.writerow(linha)
                
            #f.close()
                
            
                
                
         
        
