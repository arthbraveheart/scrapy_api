from itemloaders.processors import TakeFirst, MapCompose, Compose, Identity
from scrapy.loader import ItemLoader
import re



class BalaProductLoader(ItemLoader):
    
    default_output_processor = Identity()
            
    def extract_ean(self, dumped_json):

         pattern_ean   = re.compile(r'"ean":"(\d+)"')
         match         = re.findall(pattern_ean, dumped_json)
         if match:
             return match
         return None
    
    def extract_url(self, dumped_json):

         pattern_link  = re.compile(r'"link":"(.*?)"')
         match         = re.findall(pattern_link, dumped_json)
         if match:
             return match
         return None
    
    def extract_price(self, dumped_json):

         pattern_price = re.compile(r'"Price":(\d+\.\d+)')
         match         = re.findall(pattern_price, dumped_json)
         if match:
             return match
         return None
    
    
    eans   = MapCompose(lambda x :  BalaProductLoader().extract_ean(x) )
    url    = MapCompose(lambda x : BalaProductLoader().extract_url(x) )
    price  = MapCompose(lambda x: BalaProductLoader().extract_price(x))


