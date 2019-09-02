import csv
import datetime
import json
import logging
import os.path
import pdb
import sys
from itertools import cycle
#from urllib import response
import requests
#import setup
#from  ..commons.zip_5o_miles import _zip

PATH = os.path.realpath(os.path.abspath(__file__)) #it tell u corrent file
print(PATH)
logger  = logging.getLogger(__name__)
#logging.basicConfig(filename='logger.log' ,  level= logging.INFO, format= '%(asctime)s:%(name)s:%(message)s')
logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
_logger = logging.basicConfig(level = logging.INFO, stream = sys.stdout,format = logformat, datefmt = "%Y-%m-%d %H:%M:%S")
date_object = datetime.date.today()
make = sys.argv[1]
file_dir =  os.environ['HOME']+"/all_dealers_csv/"+str(date_object)
logger.info('Run with file_dir: {}, and make {}'.format(file_dir,make))
path = os.getcwd()
print(path)
try:
    os.makedirs(file_dir+"/"+str(make))
    logger.info('Created with file_dir make :{}'.format(make))
    pass
except :
    logger.info("Already exist:{}".format(make))

def make_zip():
    arr = ["17087", "95666", "53936", "83330", "17006", "42157", "57562", "28349", "85743", "38471", "81212",
           "82058", "84721", "62469", "97635", "87943", "58561", "95421", "24211", "47930", "64761", "56025",
           "49635", "28376", "69128", "84766", "30454", "59230", "32350", "12969", "31312", "12455", "65263",
           ]
    return arr
make_zip = make_zip()
print(make_zip)
proxies = {'173.208.103.45:8800','148.251.29.97:60000'}
proxy_pool = cycle(proxies)
# proxyDict = {
#               "http"  : http_proxy,
#               "https" : https_proxy,
#               "ftp"   : ftp_proxy
#             }
CRAWL_CONFIG = {
        "AUTOTRADER_HEADERS": [
            "-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'",
            "-H 'Connection: keep-alive'",
            "-H 'Accept-Encoding: gzip, deflate, br'",
            "-H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8'",
            "-H 'Upgrade-Insecure-Requests: 1'",
            #    "-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'",
            "--compressed"
        ]}
count = 0
for zip in make_zip:
        # Get a proxy from the pool
        proxy = next(proxy_pool)
        print("Request #%s"%(zip))
        try:
            logging.info('Getting proxy:{}-'.format(proxy))
            url = "https://www.acura.com/platform/api/v1/dealer?productDivisionCode=B&zip="+str(zip)+"&maxResults=100"
            logging.info('Getting url:{}-'.format(url))
            response = requests.get(url,proxy)
            jsonObject = json.loads(response.text)
            logging.info(response)
            if response.status_code == 200:
                logging.info("Creating Csv file :{}-".format(make))
                with open('acura.csv', 'a') as fd:
                    for dealer in jsonObject['Dealers']:
                          dealer_id  = dealer['DealerNumber']
                          dealer_name = dealer['Name']
                          dealer_add = dealer['Address']
                          dealer_city = dealer['City']
                          dealer_State = dealer['State']
                          dealer_zipcode = dealer['ZipCode']
                    myCsvRow = [dealer_id,dealer_name,dealer_add,dealer_city,dealer_State,dealer_zipcode]
                    logging.info("These are dealer info:{}".format(myCsvRow))
                    newFileWriter = csv.writer(fd)
                    newFileWriter.writerow(myCsvRow)
                    count +=1
                    logging.info("Total Scraped dealer's :{}".format(count))
            else:
             print("Getting Error : 404")
            pass
        except:
            # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            print("Skipping. Connnection error")


