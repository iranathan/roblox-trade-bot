import httpx, json, settings
http = httpx.AsyncClient()

cookies = {
    '.ROBLOSECURITY': settings.settings['cookie']
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json; charset=utf-8',
    'X-CSRF-TOKEN': 'TWSGXzUxT212',
    'Connection': 'keep-alive',
    'Referer': 'https://www.roblox.com/my/money.aspx',
    'Cache-Control': 'max-age=0',
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-CSRF-TOKEN': '5HpedRy6Tri+',
    'Connection': 'keep-alive',
    'Referer': 'https://www.roblox.com/my/money.aspx',
}

async def get_trades():
    data = json.dumps({
        'startindex': 0,
        'statustype': 'inbound'
    })
    r = await http.post('https://www.roblox.com/my/money.aspx/getmyitemtrades', data=data, headers=headers, cookies=cookies)
    if r.status_code == 403 and r.headers.get('X-CSRF-TOKEN'):
        headers['X-CSRF-TOKEN'] = r.headers.get('X-CSRF-TOKEN')
        r = await http.post('https://www.roblox.com/my/money.aspx/getmyitemtrades', data=data, headers=headers, cookies=cookies)
    return r

async def execute_trade(id, tradetype):
    data = {
        'TradeID': id,
        'cmd': tradetype
    }
    r = await http.post('https://www.roblox.com/trade/tradehandler.ashx', headers=headers2, cookies=cookies, data=data)
    if r.status_code == 403 and r.headers.get('X-CSRF-TOKEN'):
        headers2['X-CSRF-TOKEN'] = r.headers.get('X-CSRF-TOKEN')
        r = await http.post('https://www.roblox.com/trade/tradehandler.ashx', headers=headers2, cookies=cookies, data=data)
    return r

async def resellers(id):
    r = await http.get(f'https://economy.roblox.com/v1/assets/{id}/resellers?limit=10', headers=headers, cookies=cookies)
    return r