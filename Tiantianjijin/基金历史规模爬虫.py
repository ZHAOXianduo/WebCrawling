import requests
import json
import pandas as pd
import time
from urllib.parse import urlencode
import pyquery as pq
import numpy as np

### 设置请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Cookie': 'qgqp_b_id=d4c7d95b9a3fea432b6afb4394d1e7cb; em_hq_fls=js; cowCookie=true; st_si=11660912221455; cowminicookie=true; st_asi=delete; HAList=a-sz-301179-N%u6CFD%u5B87%2Cf-0-000012-%u56FD%u503A%u6307%u6570; intellpositionL=1215.35px; intellpositionT=955px; st_pvi=54890317298070; st_sp=2021-02-13%2023%3A08%3A33; st_inirUrl=https%3A%2F%2Fwww.sogou.com%2Flink; st_sn=12; st_psi=2021120911112711-113300300815-1187412359'
}

### 设置抓取链接
funds = pd.read_csv("H:\基金数据\公募基金\公募基金名单.csv",converters={'基金代码':str})
for i in funds['基金代码']:
    try:
        URL_p = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=gmbd&mode=0&code=' + i
        r = requests.get(URL_p, headers=HEADERS, timeout=3.0)
        doc = pq.PyQuery(r.text)
        table = doc.text().split('content')[1].split("\"")[1].split("\n")[1:-1]
        table = np.array(table).reshape(int(len(table)/6),6)
        timetable = pd.DataFrame(table[1:],columns = table[0])
        timetable.to_csv(r'H:/基金数据/公募基金/amount/'+i+'_amount.csv')
    except:
        print(i,'fail')


