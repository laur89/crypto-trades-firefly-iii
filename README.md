# crypto-trades-firefly-iii

This service lets you import your movements on supported crypto trading platforms to your Firefly III account. Keep an overview of your traded crypto assets.

## Supported crypto trading platform / exchanges for trades
- Binance (formerly known as [binance-firefly-iii](https://github.com/financelurker/binance-firefly-iii))
  - "notes identifier": "crypto-trades-firefly-iii:binance"

In the doing:
- Crypto.com
- Kraken
- coinbase
- ...

This module runs stateless next to your Firefly III instance (as Docker container or standalone) and periodically processes new data from your configured crypto trading platform. Just spin it up and watch your trades being imported right away.

## Imported Movements from Crypto Trading Platform to Firefly III

The following movements on your crypto trading platform account will be imported to your Firefly III instance:

### Executed trades
- creates transactions for each trade happened automatically
  - adds/lowers funds to/from your "security" account - the asset account of the coin you have bought or sold in that trade
  - lowers/adds funds to/from your "currency" account - the asset account of the coin you have sold or bought in that trade
  - transactions get a tag <crypto trading platform> assigned (e.g. "binance")
  - transactions get a note "crypto-trades-firefly-iii:<crypto exchange>:trade" (e.g. "crypto-trades-firefly-iii:binance:trade")
- Paid fees import as new transactions
  - For each trade on your crypto trading platform there is a paid commission. For this paid commission an additional transaction is created, linking the asset account holding the commission currency, and the crypto trading platform expense account.
  - transactions get a tag <crypto trading platform> assigned (e.g. "binance")
  - transactions get a note "crypto-trades-firefly-iii:<crypto exchange>:fee" (e.g. "crypto-trades-firefly-iii:binance:fee")
- _**Known limitations for Binance:**_
  - Only 500 transactions will be imported for each trading pair. (I'll fix that in the future with a more sophisticated import query with the Binance API)
  - Rate limiting: if you run this app in debug mode the Binance API will be polled every 10 seconds. You'll probably get blocked sometime from further API calls. Make sure that you're using Binance testnet when running this in debug-mode to not interfer with your IP rates at Binance (or you know what you're doing).

### ToDos per Crypto Trade Platform

  - Trades and trading fees
  - Deposits from / Withdrawals to your other crypto addresses
  - Received Interest vía lending or staking
  - On-/Off-ramping from or to SEPA asset account (via IBAN-matching)

# How to Use

## If you have used binance-firefly-iii before

Just configure this service as you configured binance-firefly-iii and run it. All "notes identifier" will be migrated for using crypto-trades-firefly-iii.
binance-firefly-iii will not find any accounts within Firefly-III afterwards.

_"notes identifier" are used so that crypto-trades-firefly-iii services can find and match your correct exchange accounts._

## Prepare your Firefly III instance

To import your movements from Binance your Firefly III installation has to be extended as follows:

- Currencies for crypto coins/tokens
  - Add custom currencies which you are trading on crypto exchanges (e.g. name "Bitcoin", symbol "₿", code "BTC", digits "8")
- Create accounts for each of your exchange connections
  - asset
    - add an asset account for each coin/token
  - expense
    - add one account for all expenses on that exchange
  - revenue
    - add a revenue account for each coin/token where you get lending interest or staking interest from
  - for all accounts you create
    - set a specific note in the notes field: "crypto-trades-firefly-iii:<exchange>"
- Asset Accounts for currency funds on crypto exchanges
  - Create exactly one account for each coin/token you trade for each crypto exchange (type = 'asset')
  - Make sure you select the currency for that account, so the code or symbol matches the trading symbol for that currency on the exchange.
  - Add the "notes identifies" to the notes of that account:
    - Binance: **"crypto-trades-firefly-iii:binance:fund"**
    - Crypto.com **"crypto-trades-firefly-iii:crypto.com:fund"**
- Revenue Accounts for lending/staking revenues
  - Create exactly one account for each coin/token you trade for each crypto exchange (type = 'revenue')
  - Make sure you select the currency for that account, so the code or symbol matches the trading symbol for that currency on the exchange.
  - Add the "notes identifies" to the notes of that account:
    - Binance: **"crypto-trades-firefly-iii:binance:revenue"**
    - Crypto.com **"crypto-trades-firefly-iii:crypto.com:revenue"**
- Expense Accounts for fees and commission
  - Create exactly one account for each exchange for paid fees and commission.
  - Add the "notes identifies" to the notes of that account:
    - Binance: **"crypto-trades-firefly-iii:binance:expenses"**
    - Crypto.com **"crypto-trades-firefly-iii:crypto.com:expenses"**

## Working environments

- Firefly III Version 5.4.6
- Binance API Change Log up to 2021-04-08

## Run as Docker container from Docker Hub

Pull the image and run the container passing the needed environmental variables.

```
docker pull financelurker/crypto-trades-firefly-iii:latest
docker run --env....
```

## Run as Docker container from repository

Check out the repository and build the docker image locally. Build the container and then run it by passing the needed environmental variables.

```
git clone https://github.com/financelurker/crypto-trades-firefly-iii.git
cd crypto-trades-firefly-iii
docker build .
docker run --env....
```

## Run it standalone

Check out the repository, make sure you set the environmental variables and start thy python script:

```
git clone https://github.com/financelurker/crypto-trades-firefly-iii.git
cd crypto-trades-firefly-iii
python -m pip install --upgrade setuptools pip wheel
python -m pip install --upgrade pyyaml
python -m pip install Firefly-III-API-Client
python -m pip install python-binance
python -m pip install cryptocom-exchange
python main.py
```

If you are having any troubles, make sure you're using **python 3.9** (the corresponding Docker image is **"python:3.9-slim-buster"** for version referencing).

## Configuration

This image is configured via **environmental variables**. As there are many ways to set them up for your runtime environment please consult that documentation.

Make sure you have them set as there is no exception handling for missing values from the environment.
- **FIREFLY_HOST**
  - Description: The url to your Firefly III instance you want to import trades. (e.g. "https://some-firefly-iii.instance:62443" and **make sure it's a test system for now!!**)
  - Type: string
- **FIREFLY_VALIDATE_SSL**
  - Description: Enables or disables the validation of ssl certificates, if you're using your own x509 CA.
    (there probably are better ways of doing this)
  - Type: boolean [ false | any ]
  - Optional
  - Default: true
- **FIREFLY_ACCESS_TOKEN**
  - Description: Your access token you have created within your Firefly III instance.
  - Type: string
- **BINANCE_API_KEY**
  - Description: The api key of your binance account. It is highly recommended creating a dedicated api key with only read permissions on your Binance account.
  - Type: string
- **BINANCE_API_SECRET**
  - Description: The api secret of that api key.
  - Type: string
- **CRYPTOCOM_API_KEY**
  - Description: **This config key has no impact for now.** The api key of your Crypto.com Exchange account. It is highly recommended creating a dedicated api key with only read permissions on your Crypto.com Exchange account.
  - Type: string
- **CRYPTOCOM_API_SECRET**
  - Description: **This config key has no impact for now.** The api secret of that api key.
  - Type: string
- **SYNC_BEGIN_TIMESTAMP**
  - Description: The date of the transactions must not be older than this timestamp to be imported. This helps you to import from back to 2017 initially and once you have imported them all you can set the date to a date near the container runtime start to reduce probable bandwidth-costs on exchange-side. (e.g. "2018-01-22") as these APIs often work with rate-limiting.
  - Type: date [ yyyy-MM-dd ]
- **SYNC_TRADES_INTERVAL**
  - Description: This defines on how often this module will check for new trades on all configured exchanges.
    Only trades up to the last full interval (hour or day) are synchronized.
    The debug mode fetches every 10 seconds.
  - Type: enum [ hourly | daily | debug ]
- **DEBUG**
  - Description: Adds to each written object an additional 'dev' tag. As long as this arg is present the debug mode will be turned on.
  - Type: boolean [ any ]
  - Optional
  - Default: false

# How to add exchanges

To add a new exchange as data source you need to implement two classes which super classes are [declared in here](./src/exchanges/exchange_interface.py):
- **CryptoExchangeModuleMetaClass** which is the meta class for your exchange module. It defines meta information and access to the client implementation
  - the name of the exchange
  - the environmental variables needed to run this exchange plugin
  - an instance of the appropriate CryptoExchangeInterface sub-class
- **CryptoExchangeInterface** is the specific implementation class for the exchange API which provides
  - a method to check connectivity
  - a method to get all trades of the account (for a given time period)
  - a method to get all received interest (for a given time period)
  - a method to get all previously detected trading pairs that were rejected by the exchange

When you have those classes implemented add your module (*.py file) to [this package](./src/exchanges/impls). Python modules in that package will be picked up automatically during initialization phase of the service.

If you want your exchange implementation added to this repository, just create a pull request with your exchange implementation. When you add the needed environmental variables declared by your exchange plugin the service will automatically connect to that exchange and import data.

Pull requests containing writing actions to the exchange will probably be rejected - as all exchange interactions have to be of read nature.

# Disclaimer
This app needs access tokens for your Firefly III instance, and access tokens/API-Keys for your crypto trading platform account. It is absolutely okay to only give read-permissions to that access tokens/API-Keys, as there will be no writing actions to crypto trading platform by this service.
