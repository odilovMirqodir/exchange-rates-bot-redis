import aiohttp
import xml.etree.ElementTree as ET
import asyncio
import redis
from config.config import CBR_URL, HOST, PORT

r = redis.Redis(host=HOST, port=PORT, decode_responses=True)
CURRENCY_URL = CBR_URL


async def fetch_exchange_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get(CURRENCY_URL) as response:
            if response.status == 200:
                data = await response.text()
                return data
            else:
                return None


def parse_exchange_rates(xml_data):
    root = ET.fromstring(xml_data)
    rates = {}
    for valute in root.findall('Valute'):
        char_code = valute.find('CharCode').text
        value = float(valute.find('Value').text.replace(',', '.'))
        rates[char_code] = value
    return rates


def update_redis(rates):
    with r.pipeline() as pipe:
        for currency, rate in rates.items():
            pipe.set(currency, rate)
        pipe.execute()


async def main():
    xml_data = await fetch_exchange_rates()
    if xml_data:
        rates = parse_exchange_rates(xml_data)
        update_redis(rates)


if __name__ == '__main__':
    asyncio.run(main())
