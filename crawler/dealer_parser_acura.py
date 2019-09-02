import datetime
import logging
import os.path
import pdb
import sys
import json
import csv
from itertools import cycle
import requests
# from lib.commons.config import CRAWL_CONFIG
from lib.commons.zip_5o_miles import _zip

PATH = os.path.realpath(os.path.abspath(__file__))  # it tell u corrent file
print(PATH)
_logger = logging.getLogger(__name__)


def setup_logging():
    """Setup basic logging
    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    _logger = logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                                  format=logformat, datefmt="%Y-%m-%d %H:%M:%S")
def main(argv):
    make = argv
    setup_logging()
    print("The Dir name is {}".format(make))
    date_object = datetime.date.today()
    # pdb.set_trace()
    file_dir = os.environ['HOME'] + "/all_dealers_csv/" + str(date_object)
    _logger.info('Run with file_dir: {}, and make {}'.format(file_dir, make))
    path = os.getcwd()
    print(path)
    try:
        os.makedirs(file_dir + "/" + str(make))
        _logger.info('Created with file_dir make :{}'.format(make))
        count = 0
        proxies = {'173.208.103.45:8800', '148.251.29.97:60000'}
        proxy_pool = cycle(proxies)
        make_zip = _zip()
        for zip in make_zip:
            proxy = next(proxy_pool)
            print("Request #%s" % (zip))
            try:
                logging.info('Getting proxy:{}-'.format(proxy))
                url = "https://www.acura.com/platform/api/v1/dealer?productDivisionCode=B&zip=" + str(
                    zip) + "&maxResults=100"
                logging.info('Getting url:{}-'.format(url))
                response = requests.get(url, proxy)
                jsonObject = json.loads(response.text)
                logging.info(response)
                if response.status_code == 200:
                    logging.info("Creating Csv file :{}-".format(make))
                    with open('acura.csv', 'a') as fd:
                        for dealer in jsonObject['Dealers']:
                            dealer_id = dealer['DealerNumber']
                            dealer_name = dealer['Name']
                            dealer_add = dealer['Address']
                            dealer_city = dealer['City']
                            dealer_State = dealer['State']
                            dealer_zipcode = dealer['ZipCode']
                        myCsvRow = [dealer_id, dealer_name, dealer_add, dealer_city, dealer_State, dealer_zipcode]
                        logging.info("These are dealer info:{}".format(myCsvRow))
                        newFileWriter = csv.writer(fd)
                        newFileWriter.writerow(myCsvRow)
                        count += 1
                        logging.info("Total Scraped dealer's :{}".format(count))
                else:
                    print("Getting Error : 404")
                pass
            except:
                # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
                # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
                print("Skipping. Connnection error")
        pass
    except:
        print("Already exist:{}".format(make))
    # proxyDict = {
    #     "http": http_proxy,
    #     "https": https_proxy,
    #     "ftp": ftp_proxy
    # }
def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1])
    _logger.info("Given argument {}:".format("acura"))
if __name__ == "__main__":
    run()
