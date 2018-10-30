import json
import requests
import time

def getData(api):
	return requests.get(url=api).json()

print("Start parsing")
print("Parsing: Cryptopia")
dataCryptopia = getData("https://www.cryptopia.co.nz/api/GetMarket/KRB_BTC")
dataCryptopia = { "sell_btc": float(dataCryptopia["Data"]["AskPrice"]) }
print("Parsing: Tradeogre")
dataTradeogre = getData("https://tradeogre.com/api/v1/ticker/BTC-KRB")
dataTradeogre = { "sell_btc": float(dataTradeogre["ask"]) }
print("Parsing: Kuna")
dataKuna = getData("https://kuna.io/api/v2/tickers/krbuah")
dataKuna = { "sell_uah": float(dataKuna["ticker"]["sell"]) }
print("Parsing: BTC-Trade")
dataBtcTrade = getData("https://btc-trade.com.ua/api/ticker/krb_uah")
dataBtcTrade = { "sell_uah": float(dataBtcTrade["krb_uah"]["sell"]), "sell_usd": float(dataBtcTrade["krb_uah"]["sell_usd"]), "usd_uah": float(dataBtcTrade["krb_uah"]["usd_rate"]) }
print("Parsing: Richamster (UAH)")
dataRichamsterUAH = getData("https://richamster.com/public/v1/exchange/ticker/?pair=KRB/UAH")
dataRichamsterUAH = { "sell_uah": float(dataRichamsterUAH[0]["last"]) }
print("Parsing: Richamster (BTC)")
dataRichamsterBTC = getData("https://richamster.com/public/v1/exchange/ticker/?pair=KRB/BTC")
dataRichamsterBTC = { "sell_btc": float(dataRichamsterBTC[0]["last"]) }

print("Processing...")
btc2usd = float(getData("http://preev.com/pulse/units:btc+usd/sources:bitstamp")["btc"]["usd"]["bitstamp"]["last"])
usd2uah = dataBtcTrade["usd_uah"]
prices = { "uah": [], "usd": [], "btc": [] }

prices["uah"].append(dataBtcTrade["sell_uah"])
prices["uah"].append((btc2usd * dataCryptopia["sell_btc"]) * usd2uah)
prices["uah"].append((btc2usd * dataTradeogre["sell_btc"]) * usd2uah)
prices["uah"].append(dataKuna["sell_uah"])
prices["uah"].append(dataRichamsterUAH["sell_uah"])
prices["uah"].append((btc2usd * dataRichamsterBTC["sell_btc"]) * usd2uah)

prices["usd"].append(dataBtcTrade["sell_usd"])
prices["usd"].append(btc2usd * dataCryptopia["sell_btc"])
prices["usd"].append(btc2usd * dataTradeogre["sell_btc"])
prices["usd"].append(dataKuna["sell_uah"] / usd2uah)
prices["usd"].append(dataRichamsterUAH["sell_uah"] / usd2uah)
prices["usd"].append(btc2usd * dataRichamsterBTC["sell_btc"])

prices["btc"].append(dataBtcTrade["sell_usd"] / btc2usd)
prices["btc"].append(dataCryptopia["sell_btc"])
prices["btc"].append(dataTradeogre["sell_btc"])
prices["btc"].append((dataKuna["sell_uah"] / usd2uah) / btc2usd)
prices["btc"].append((dataRichamsterUAH["sell_uah"] / usd2uah) / btc2usd)
prices["btc"].append(dataRichamsterBTC["sell_btc"])

result = {
	"uah": format(sum(prices["uah"]) / float(len(prices["uah"])), ".8f"),
	"usd": format(sum(prices["usd"]) / float(len(prices["usd"])), ".8f"),
	"btc": format(sum(prices["btc"]) / float(len(prices["btc"])), ".8f"),
	"updated": int(time.time())
}

print("Writing price.json")
with open('price.json', 'w') as outfile:
	json.dump(result, outfile)

print("Done :)")
