# py-ebay
This is some sample code of a wrapper to talk to Ebay.  It uses the ebay-sdk and there are some IPython notebooks sample code.

## Note
You have to create a ebay.yaml file in the root directory.  I have been bad and just used the production for my testing as I am listing 
my own products.  So my file looks like this:

### ebay.yaml
name: ebay_api_config

#### Trading API - https://www.x.com/developers/ebay/products/trading-api
api.ebay.com:
    compatability: 719
	siteid: 3
    appid: Xxxxxxxx-Xxxxxxxx-PRD-000000000-00000000
    certid: PRD-000000000000-0000-0000-0000-0000
    devid: 00000000-0000-0000-0000-0000000000000
    token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
           

#### Finding API - https://www.x.com/developers/ebay/products/finding-api
svcs.ebay.com:
    appid: Xxxxxxxx-Xxxxxxxx-PRD-000000000-00000000
    version: 1.0.0

#### Shopping API - https://www.x.com/developers/ebay/products/shopping-api
open.api.ebay.com:
    appid: Xxxxxxxx-Xxxxxxxx-PRD-000000000-00000000
 