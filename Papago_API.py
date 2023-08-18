import json
import os
import sys
import urllib.request

from config.settings.base import get_secret

NCP_CLIENT_ID = "kdcgbbawp7"
NCP_CLIENT_SECRET = "ncyq8gM4gtRRjgWy8aKm2Qi3vxzTeEdDFN9eRO1c"

def translate_and_extract(sentence, target_language='en'):
    if not sentence: 
        return ''
    
    encText = urllib.parse.quote(str(sentence))
    data = "source=ko&target=en&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",NCP_CLIENT_ID)
    request.add_header("X-NCP-APIGW-API-KEY",NCP_CLIENT_SECRET)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_json = json.loads(str(response_body.decode('utf-8')))
        return response_json['message']['result']['translatedText']
    else:
        print('Error on translation: ' + rescode)
        return sentence
    

if __name__ == '__main__':
    result = translate_and_extract('파파고는 최고의 번역기입니다.')
    print(result)
