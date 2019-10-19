import roblox, asyncio, json, re

print('----Roblox trade bot----')
print('   Made By: iranathan\n\n')


async def best_price(e):
    price = 0
    for item in e:
        id = int(''.join(re.findall(r'\b\d+\b', item['ItemLink'])))
        resellers = await roblox.resellers(id)
        if resellers.status_code == 200:
            resellers_json = resellers.json()
            price += resellers_json['data'][0]['price']
    return price


def parse_items(e):
    str = ''
    for item in e:
        str += item['Name'] + ', '
    return str


async def run():
    trades = await roblox.get_trades()
    if trades.status_code != 200:
        print('Your cookie has expired...')
        exit()
    data = json.loads(json.loads(trades.text)['d'])['Data']
    print(f'Found {len(data)} trades...\n')
    for i in range(len(data)):
        print(f'checking trade #{i+1}')
        trade = data[i]
        trade_identify = json.loads(trade)
        trade_object = await roblox.execute_trade(int(trade_identify['TradeSessionID']), 'pull')
        if trade_object.status_code != 200:
            print(f'Got status code {trade_object.status_code} when trying to fetch trade...')
            continue
        trade_json = json.loads(trade_object.json()['data'])['AgentOfferList']
        print(f'trade #{i+1} offer value is {trade_json[0]["OfferValue"]}')
        print(f'trade #{i+1} request value is {trade_json[1]["OfferValue"]}')
        prices = [await best_price(trade_json[0]['OfferList']), await best_price(trade_json[1]['OfferList'])]
        if prices[0] < prices[1]:
            print(f':pensive: trade #{i+1} is bad you will lose {prices[0] - prices[1]} robux')
            continue
        else:
            msg = input(f'\nTrade #{i+1}:\nYou will win {prices[0]-prices[1]} robux\nYou will give: {parse_items(trade_json[1]["OfferList"])}\nYou will get: {parse_items(trade_json[0]["OfferList"])}\nAccept Trade? (y/n) :')
            if msg.lower().startswith('y'):
                await roblox.execute_trade(int(trade_identify['TradeSessionID']), 'accept')
            else:
                await roblox.execute_trade(int(trade_identify['TradeSessionID']), 'decline')

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()
