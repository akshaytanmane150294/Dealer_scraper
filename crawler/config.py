import json

CRAWL_CONFIG = {
"AUTOTRADER_HEADERS" : [
    "-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'",
    "-H 'Connection: keep-alive'",
    "-H 'Accept-Encoding: gzip, deflate, br'",
    "-H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8'",
    "-H 'Upgrade-Insecure-Requests: 1'",
    #    "-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'",
    "--compressed"
]}
