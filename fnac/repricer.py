from fnapy.fnapy_manager import FnapyManager
from fnapy.connection import FnapyConnection
import datetime


class FnacRepricer:

    def __init__(self, ean, fnac_id, floor_price):
        self.credentials = {'partner_id': ,
                            'shop_id': ,
                            'key': ,
                            'sandbox': False}
        self.sandbox_credentials = {
            'partner_id': ,
            'shop_id': ,
            'key': ,
            'sandbox': True
        }
        self.ean = [ean]
        self.fnac_id = fnac_id
        self.floor_price = floor_price
        self.connection = FnapyConnection(self.credentials)
        self.manager = FnapyManager(self.connection)
        self.token = self.manager.authenticate()


    def repricing(self, my_price, best_price, floor_price, my_quantity, my_sku):
        if my_price > best_price and best_price >= floor_price and my_quantity > 0:
            self.manager.update_offers(['offer_reference', my_sku])


    def run(self):

        # connection
        print(self.token)
        print('Connected to shop id : %s' % self.credentials['shop_id'])

        # query best price
        print('Time : %s' % datetime.datetime.now())
        dp = self.manager.query_pricing(self.ean).dict
        price = dp['pricing_query_response']['pricing_product']['pricing'][0]['price']
        shipping_price = dp['pricing_query_response']['pricing_product']['pricing'][0]['shipping_price']
        best_price = price + shipping_price
        print('Best price for EAN %s is at %s is : %s'
              % (self.ean, datetime.datetime.now(), best_price))

        # query my_price
        do = self.manager.query_offers(offer_seller_id=self.fnac_id).dict
        my_price = do['offers_query_response']['offer']['price']
        my_sku = do['offers_query_response']['offer']['offer_fnac_id']
        my_quantity = do['offers_query_response']['offer']['quantity']

        # repricing
        if my_price > best_price and

'''SKU : offer_seller_id

[dict]
offer_data = [{'offer_reference': 'offer_seller_id', 'price': 3}]
'''

repricer = FnacRepricer(3700785420822, 28208518, 3)
repricer.run()


