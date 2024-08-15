# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:58:50 2024

@author: ArthurRodrigues
"""

import scrapy
from balarotiscraper.itemloaders import BalaProductLoader
from balarotiscraper.items import BalaProduct 
from pandas import read_pickle 
import re
import json
import urllib
import base64

class BalaSpider(scrapy.Spider):
   """
   Aqui encontra-se o core da nossa busca. 
   A URL principal, start_url, foi encontrada a partir da investigação da aba Network no frame DevTools do navegador. 
   Lá encontramos o comportamento da página, mostrando as fontes e respostas dessas consultas. 
     
   """

   name       = 'balarotispider'
   refs       = read_pickle('C:/Users/Usuario/Arthur/Códigos/crawler_API-main/APIs/CrawlAPI/Variables/BalaMap.pkl')
   start_urls = ['https://www.balaroti.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=3d10c899-3307-422f-9440-1b8075245ef3&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%228e3fd5f65d7d83516bfea23051b11e7aa469d85f26906f27e18afbee52c56ce4%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJGSVJTVF9BVkFJTEFCTEUiLCJzaW11bGF0aW9uQmVoYXZpb3IiOiJkZWZhdWx0IiwiaW5zdGFsbG1lbnRDcml0ZXJpYSI6Ik1BWF9XSVRIT1VUX0lOVEVSRVNUIiwicHJvZHVjdE9yaWdpblZ0ZXgiOmZhbHNlLCJtYXAiOiJjIiwicXVlcnkiOiJtYXRlcmlhbC1kZS1jb25zdHJ1Y2FvIiwib3JkZXJCeSI6Ik9yZGVyQnlTY29yZURFU0MiLCJmcm9tIjowLCJ0byI6MTEsInNlbGVjdGVkRmFjZXRzIjpbeyJrZXkiOiJjIiwidmFsdWUiOiJtYXRlcmlhbC1kZS1jb25zdHJ1Y2FvIn1dLCJmYWNldHNCZWhhdmlvciI6IlN0YXRpYyIsImNhdGVnb3J5VHJlZUJlaGF2aW9yIjoiZGVmYXVsdCIsIndpdGhGYWNldHMiOmZhbHNlLCJhZHZlcnRpc2VtZW50T3B0aW9ucyI6eyJzaG93U3BvbnNvcmVkIjp0cnVlLCJzcG9uc29yZWRDb3VudCI6MywiYWR2ZXJ0aXNlbWVudFBsYWNlbWVudCI6InRvcF9zZWFyY2giLCJyZXBlYXRTcG9uc29yZWRQcm9kdWN0cyI6dHJ1ZX19%22%7D']
   
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_generator = getALL(self.start_urls[0], 2759, self.refs)
        self.next_url = next(self.url_generator, None)

   def parse(self, response):
        """
        Aqui extraímos a informação que precisamos em formato de texto para depois, 
        nas etapas de Item e ItemLoaders, extrairmos exatamente o que precisamos. 

        """
       
        
        product = BalaProductLoader(item=BalaProduct(), selector=response)
        product.add_value('eans', response.text)
        product.add_value('price', response.text)
        product.add_value('url', response.text)
        yield product.load_item()

        if self.next_url:
            next_page_url = self.next_url
            self.next_url = next(self.url_generator, None)
            yield response.follow(next_page_url, callback=self.parse)  


def getProducts(url : str , rng : tuple, ref : str) -> str:
    
    """
    Essa também é uma função muito importante no processo, pois é ela que decodifica
    os comandos GraphQL. 
    Após decodificado, transformamos num dicionário. Assim podemos editar e
    executarmos os comandos que quisermos.
    
    """
    
    # Extract the query parameters from the URL
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Extract the 'extensions' parameter
    extensions_encoded = query_params['extensions'][0]

    # URL decode the 'extensions' parameter
    extensions_decoded = urllib.parse.unquote(extensions_encoded)

    # Parse the decoded JSON string
    extensions_obj = json.loads(extensions_decoded)#[:-1] + '"}') #extension string fixed

    # Extract the 'variables' parameter
    variables_encoded = extensions_obj['variables']

    # Base64 decode the 'variables' parameter
    variables_decoded = base64.b64decode(variables_encoded).decode('utf-8')

    # Parse the JSON string to get the original JSON object
    variables_obj = json.loads(variables_decoded)

    # Modify the variables object
    variables_obj['from'] = rng[0]
    variables_obj['to']   = rng[1]
    variables_obj['query']= ref#'material-de-construcao'
    variables_obj['selectedFacets'][0]['value'] = variables_obj['query']
    # Convert the modified object to a JSON string
    modified_variables_json = json.dumps(variables_obj)
    # Base64 encode the JSON string
    modified_variables_encoded = base64.b64encode(modified_variables_json.encode('utf-8')).decode('utf-8')
    # Update the extensions object with the new encoded variables
    extensions_obj['variables'] = modified_variables_encoded
    # Convert the updated extensions object to a JSON string
    updated_extensions_json = json.dumps(extensions_obj)
    # URL encode the JSON string
    updated_extensions_encoded = urllib.parse.quote(updated_extensions_json)

    # Construct the new URL with the updated 'extensions' parameter
    new_query_params = query_params
    new_query_params['extensions'] = updated_extensions_encoded
    # Construct the new URL
    #new_url = urllib.parse.urlunparse(parsed_url._replace(query=urllib.parse.urlencode(new_query_params, doseq=True)))

    url_base = 'https://www.balaroti.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=3d10c899-3307-422f-9440-1b8075245ef3&operationName=productSearchV3&variables=%7B%7D&extensions='

    new_urlll = url_base + updated_extensions_encoded

    return new_urlll




def getALL(url : str, n : int, refs : list):
    """
    Simplesmente cria um loop para executar comandos GET comum range de 100 produtos. 

    Parameters
    ----------
    url : str
        comando GraphQL.
    n : int
        quantos GET serão executados.
    refs : list
        lista contendo o mapa do site em url relativa, por exemplo: ['material-de-construção', 'banheiro','ferramentas'].

    Yields
    ------
    new_url : str
        comando GraphQL atualizado com o novo range.

    """
     
    i=0
    chunk = 99
    #querys = (ref in refs)
    for ref in refs: 
        while True:
             if i<ref[1]:
                 tup     = (i,i+chunk)
                 new_url = getProducts(url,tup,ref[0])
                 i = i+chunk
                 yield new_url
             else:
                 tup = (i-chunk,ref[1])
                 new_url = getProducts(url,tup,ref[0])
                 yield new_url
                 break

  
