import json
import asyncio
import aiohttp
import datetime
import time
import traceback

class Magicwallet():
    def __init__(self,config): 
        header = {
            'User-Agent': 'curl/7.35.0',
            'Accept': '*/*',
            'apikey':config}
        self.session = aiohttp.ClientSession(headers=header)

    @asyncio.coroutine
    def get_changerate(self):
        try:
            url = "https://redemption.icowallet.net/api_v2/RechargeAndWithdrawTables/GetListForRechargeAndWithdrawtable"
            response = yield from asyncio.wait_for(self.session.post(url), 120)
            response = yield from response.read()
            result = json.loads(response.decode("utf-8-sig"))
            price_element = self.get_most_recent_data(result)
            depositBitCNY = float(price_element['depositBitCNY'])
            withdrawBitCNY = float(price_element['withdrawBitCNY'])
            depositFiatCNY = float(price_element['depositFiatCNY'])
            withdrawFiatCNY = float(price_element['withdrawFiatCNY'])
            price_rate = float((depositFiatCNY+withdrawFiatCNY)/(depositBitCNY+withdrawBitCNY))
            print('magic price rate:'+str(price_rate))
            return price_rate
        except Exception as e:
            print("Error fetching book from magicwallet!")
            print(e)
            return 1

    def is_valid_element(self, element):
        depositFiatCNY = float(element['depositFiatCNY'])
        withdrawFiatCNY = float(element['withdrawFiatCNY'])
        return (depositFiatCNY+withdrawFiatCNY)!=0

    def get_most_recent_data(self, price_list):
        #datetypes = (1, 5, 15, 30, 60, 120, 240, 360, 720, 1440)
        for price_element in price_list:
            datelength=price_element['datelength']
            if (datelength >= 60) and self.is_valid_element(price_element):
                print('datalength:'+str(datelength))
                return price_element
        return None




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    magicwallet = Magicwallet() 
    loop.run_until_complete(magicwallet.get_changerate())
    loop.run_forever()
