import json
import requests
import time

def getData(api):
	return requests.get(url=api).json()

dataCryptopia = getData("https://www.cryptopia.co.nz/api/GetMarket/KRB_BTC")
dataCryptopia = { "sell_btc": float(dataCryptopia["Data"]["AskPrice"]) }
dataTradeogre = getData("https://tradeogre.com/api/v1/ticker/BTC-KRB")
dataTradeogre = { "sell_btc": float(dataTradeogre["ask"]) }
dataKuna = getData("https://kuna.io/api/v2/tickers/krbuah")
dataKuna = { "sell_uah": float(dataKuna["ticker"]["sell"]) }
dataBtcTrade = getData("https://btc-trade.com.ua/api/ticker/krb_uah")
dataBtcTrade = { "sell_uah": float(dataBtcTrade["krb_uah"]["sell"]), "sell_usd": float(dataBtcTrade["krb_uah"]["sell_usd"]), "usd_uah": float(dataBtcTrade["krb_uah"]["usd_rate"]) }

btc2usd = float(getData("http://preev.com/pulse/units:btc+usd/sources:bitstamp")["btc"]["usd"]["bitstamp"]["last"])
usd2uah = dataBtcTrade["usd_uah"]
prices = { "uah": [], "usd": [], "btc": [] }

prices["uah"].append(dataBtcTrade["sell_uah"])
prices["uah"].append((btc2usd * dataCryptopia["sell_btc"]) * usd2uah)
prices["uah"].append((btc2usd * dataTradeogre["sell_btc"]) * usd2uah)
prices["uah"].append(dataKuna["sell_uah"])

prices["usd"].append(dataBtcTrade["sell_usd"])
prices["usd"].append(btc2usd * dataCryptopia["sell_btc"])
prices["usd"].append(btc2usd * dataTradeogre["sell_btc"])
prices["usd"].append(dataKuna["sell_uah"] / usd2uah)

prices["btc"].append(dataBtcTrade["sell_usd"] / btc2usd)
prices["btc"].append(dataCryptopia["sell_btc"])
prices["btc"].append(dataTradeogre["sell_btc"])
prices["btc"].append((dataKuna["sell_uah"] / usd2uah) / btc2usd)

result = {
	"uah": format(sum(prices["uah"]) / float(len(prices["uah"])), ".8f"),
	"usd": format(sum(prices["usd"]) / float(len(prices["usd"])), ".8f"),
	"btc": format(sum(prices["btc"]) / float(len(prices["btc"])), ".8f"),
	"updated": int(time.time())
}

with open('price.json', 'w') as outfile:
    json.dump(result, outfile)