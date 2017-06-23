from checks import AgentCheck
import urllib2
import ssl
import json

class BittrexTickerCheck(AgentCheck):

    baseUrl = 'https://bittrex.com/api/v1.1/public/getticker?market='
    markets = []
    ctx = None

    def check(self, instance):


        for market in self.markets:
            url = self.baseUrl + market;
            self.log.info(url);

            content = urllib2.urlopen(url, context=self.ctx);
            self.log.info(content);

            content = json.load(content);

            self.log.info(content.get("result"));

            bid = content.get("result").get('Bid')
            ask = content.get("result").get('Ask')
            last = content.get("result").get('Last')

            self.log.info("Bid=%s" % bid)
            self.log.info("Ask=%s" % ask)
            self.log.info("Last=%s" % last)



            self.gauge("crypto.ticker.bid", bid, ["market:" + market, "exchange:bittrex"], None, None)
            self.gauge("crypto.ticker.ask", ask, ["market:" + market, "exchange:bittrex"], None, None)
            self.gauge("crypto.ticker.last", last, ["market:" + market, "exchange:bittrex"], None, None)



    def __init__(self, *args, **kwargs):
        AgentCheck.__init__(self, *args, **kwargs)

        self.log.info('markets: %s' % ','.join(self.init_config.get('markets')))
    
        self.markets = self.init_config.get('markets')

        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE



  
