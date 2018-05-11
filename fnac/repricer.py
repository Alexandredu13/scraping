from fnapy.fnapy_manager import FnapyManager
from fnapy.connection import FnapyConnection
import datetime


class FnacRepricer:

    def __init__(self):
        self.credentials = {'partner_id': 'BDF301E4-9E9F-E153-6A51-0C37D6A32C9F',
                            'shop_id': '345FF055-4B8B-0C07-38C8-36CC3B3D16B9',
                            'key': 'F4FB8AC7-F7B5-8BDC-F5FC-5594BBFBE5F8',
                            'sandbox': True}
        self.eans = [5030917077418]

    def run(self):
        # connection
        connection = FnapyConnection(self.credentials)
        manager = FnapyManager(connection)
        token = manager.authenticate()
        print(token)
        print('Connected to shop id : %s' % self.credentials['shop_id'])

        # update offers
        offer_data1 = {'product_reference': '5030917077418',
                       'offer_reference': 'B067-F0D-75E',
                       'price': 20,
                       'product_state': 11,
                       'quantity': 16,
                       'description': 'New product - 2-3 days shipping, from France'}
        manager.update_offers([offer_data1])
        a = manager.query_batch()
        print('Offer updated EANs %s' % offer_data1['product_reference'])
        print('Time : %s' % datetime.datetime.now())
        print(manager.query_offers().xml)

        price = manager.query_pricing(eans=self.eans).xml
        print(price)


repricer = FnacRepricer()
repricer.run()


