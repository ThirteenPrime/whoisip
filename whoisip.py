import sys,json

'''
#!/bin/bash
ip=$1
webapi="http://ip-api.com/json/"
curl -s $webapi$ip | python3 /home/hamob003/bin/whoisip.py
'''
input = sys.stdin
#print(f'input:{input})')
outputdict = json.load(input)
#outputdict = sys.argv[0]
#print(outputdict)
#outputdict = {"status":"success","country":"United States","countryCode":"US","region":"VA","regionName":"Virginia","city":"Ashburn","zip":"20149","lat":39.03,"lon":-77.5,"timezone":"America/New_York","isp":"Google LLC","org":"Google Public DNS","as":"AS15169 Google LLC","query":"8.8.8.8"}


for k,v in outputdict.items():
    print(f'{k}:{v}')
