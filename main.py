import requests
import json

payload = {'USER_LOGIN': '*** PLACE YOUR LOGIN EMAIL HERE', 'USER_HASH': '*** PLACE YOUR API KEY HERE ***'}
base_url = 'https://*** URL ***.amocrm.ru'


def auth_(base_url, payload):
    auth_url = '/private/api/auth.php?type=json'
    try:
        s = requests.Session()
        response = s.post(url=base_url + auth_url, data=payload)
        print('[+] Server responded with code', response.status_code, ',connected to AmoCRM successfully')
        if 'false' in response.text:
            exit(1)
        print('[+] Auth success!')
        return s
    except:
        print('[-] CRITICAL: Auth failure, exiting...')
        amo_error_codes = {'110': 'Authentication error: bad credentials',
                           '111': 'Authentication error: Multiple auth attempts failed, authenticate using the '
                                  'webbrowser and enter CAPTCHA', '112': 'Authentication error: User disabled',
                           '113': 'Access denied: Account access policy disallows sessions from you\'r IP address.',
                           '101': 'Unauthorized: Requested a nonexistent subdomain', '401':
                               'Unauthorized: No data for this account on server.'}
        response_json = (response.json())
        print(amo_error_codes[response_json["response"]["error_code"]])
        return 1


def fetch_pipeline_names(base_url, s):          #       Query for avaliable pipeline names and ids
    fetch_pipeleines_url = '/api/v2/account?with=pipelines'
    response = s.get(url=base_url + fetch_pipeleines_url)
    response_json = json.loads(response.text)
    for id in (response_json['_embedded']["pipelines"]):
        print(response_json['_embedded']["pipelines"][id]["name"])
        print('Pipeline id:', response_json['_embedded']["pipelines"][id]['id'])
    return


session = auth_(base_url, payload)
fetch_pipeline_names(base_url, session)

