import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from loguru import logger


s = requests.Session()

retries = Retry(total=5,
                backoff_factor=1,
                status_forcelist=[ 500, 502, 503, 504 ])

s.mount('https://', HTTPAdapter(max_retries=retries))
s.mount('http://', HTTPAdapter(max_retries=retries))


def get_raw(url):
    return s.get(url).content


def music_search(member: str):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'region': 'cn',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'EOEBeat/1 CFNetwork/1402.0.8 Darwin/22.2.0'
    }
    data = {
        "condition": [
            {
                "name": "userInput",
                "value": member
            },
            {
                "name": "order",
                "value": "0" # 时间倒序
            }
        ],
        "pageable": {"page": 0,"size": 1000} # 全量
    }
    res = s.post(url='https://api.eoebeat.com/eoebackend/music/search', headers=headers, json=data).json()
    return res['pageable'], res['items']

