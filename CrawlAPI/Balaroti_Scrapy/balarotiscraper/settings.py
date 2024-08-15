# Scrapy settings for chocolatescraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'balarotiscraper'

SPIDER_MODULES = ['balarotiscraper.spiders']
NEWSPIDER_MODULE = 'balarotiscraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chocolatescraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# OUTPUT PATH
import time
out_path = 'C:/Users/Usuario/Arthur/Códigos/crawler_API-main/APIs/CrawlAPI/Variables/Outputs/'
today    = time.strftime("%d-%m-%Y")


# To Storing in AWS S3 Bucket
AWS_ACCESS_KEY_ID = 'myaccesskeyhere'
AWS_SECRET_ACCESS_KEY = 'mysecretkeyhere'



# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   
     'balarotiscraper.pipelines.SavingBalaCSV': 500,


}


