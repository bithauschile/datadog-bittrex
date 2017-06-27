from checks import AgentCheck
import urllib2
import ssl
import json

class BittrexTickerCheck(AgentCheck):

    #baseUrl = 'https://bittrex.com/api/v1.1/public/getticker?market='
    baseUrl = 'https://bittrex.com/api/v1.1/public/getmarketsummaries';
    markets = []
    minBaseVolume = None;
    ctx = None

    def check(self, instance):

        content = urllib2.urlopen(self.baseUrl, context=self.ctx);
        self.log.info(content);

        content = json.load(content);

        for res in content.get("result"):

            market = res.get("MarketName");

            if not self.checkMarket(market):
                continue;


            data = {}
            data['low'] = res.get("Low");
            data['high'] = res.get("High");
            data['volume'] = res.get("Volume");
            data['last'] = res.get("Last");
            data['baseVolume'] = res.get("BaseVolume");
            #data['bid'] = res.get("Bid") * 100000;
            #data['ask'] = res.get("Ask") * 100000;
            data['openBuyOrders'] = res.get("OpenBuyOrders");
            data['openSellOrders'] = res.get("OpenSellOrders");


            if data["baseVolume"] < self.minBaseVolume:
                self.log.info("Market " + market + " < %s BTC, not publishing." % self.minBaseVolume);
                continue;

            self.log.info("Publishing marketdata for " + market);

            for key in data:
                self.gauge("crypto.ticker." + key, data.get(key), ["market:" + market, "exchange:bittrex"], None, None)


    def checkMarket(self, market):

        if market in self.markets:
            return 1;

        for m in self.markets:
            if m.endswith("*"):
                newMarket = m[:len(m)-1]
                #self.log.info("newMarket " + newMarket);
                if market.startswith(newMarket):
                    return 1;

        return 0;


    def __init__(self, *args, **kwargs):
        AgentCheck.__init__(self, *args, **kwargs)


        self.markets = self.init_config.get('markets')
        self.log.info('markets: %s' % ','.join(self.markets))

        self.minBaseVolume = self.init_config.get("minBaseVolume");
        self.log.info("minBaseVolume: %s" % self.minBaseVolume);

        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE



class MarketDataEntry():
    low = None;
    high = None;
    volume = None;
    last = None;
    baseVolume = None;
    bid = None;
    ask = None;
    openBuyOrders = None;
    openSellOrder = None;
