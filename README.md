# datadog-bittrex
This is an integration (Custom agent) to extract cryptocurrencies values from Bittrex and publish them to Datadog in "real-time". It queries the Bittrex ticker API every 30 seconds and sends the bid, ask and last value of the currencies configured.

## Instalation (for Linux)

- Place bittrex.py in /opt/datadog-agent/agent/checks.d/
- Place bittrex.yaml in /etc/dd-agent/conf.d/
- Edit /etc/dd-agent/conf.d/bittrex.yamp to add you favorites cryptocurrencies.

## Configuration
- No Datadog API key configuration needed, as it uses the one from the local agent.
- Just add the currencies.

<pre>
init_config:
    min_collection_interval: 30
    markets:
    - BTC-LTC
    - BTC-XRP
    - BTC-WAVES
instances:
    [{}]
<pre>

