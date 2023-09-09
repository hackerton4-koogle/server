from config.settings.base import get_secret

import requests

def translate(sentence, target_language='영어'):
    # NCP의 Papago API를 사용해 주어진 한국어 텍스트를 원하는 언어로 번역합니다. 
    # sentence: 번역하고 싶은 한국어 문장
    # target_language: 번역 결과 언어 코드

    supported_language = {
        "영어": "en", 
        "일본어": "ja", 
        "중국어 간체": "zh-CN", 
        "중국어 번체": "zh-TW", 
        "베트남어": "vi",
        "태국어": "th", 
        "인도네시아어": "id", 
        "프랑스어": "fr", 
        "스페인어": "es", 
        "러시아어": "ru",
        "독일어": "de", 
        "이탈리아어": "it"
    }

    if not sentence: 
        return ''
    
    if target_language not in supported_language:
        return sentence
    
    lang_code = supported_language[target_language]
    
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": get_secret('NCP_PAPAGO_CLIENT_ID'),
        "X-NCP-APIGW-API-KEY":  get_secret('NCP_PAPAGO_CLIENT_SECRET'),
        "Content-Type": "application/json"
    }
    data = {
        "source": "ko",
        "target": lang_code,
        "text": sentence,
    }

    response = requests.post(url, headers=headers, json=data)
    response_status_code = response.status_code

    if response_status_code == 200:
        translated_text = response.json()['message']['result']['translatedText']
        return translated_text

    else:
        print(f"Error: HTTP status code {response_status_code}")
        print(response.text)

    

if __name__ == '__main__':
    result = translate('파파고는 최고의 번역기입니다.')
    print(result)