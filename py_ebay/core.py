# Code to get an Pandas Dataframe of your listings.
# Asssumes py_ebay.yaml in root directory and installed.
# Using Ebay SDK
# Having got and py_ebay.yaml setup in same directory
# Just get your user ID

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

import datetime as dt
import pandas as pd
import numpy as np

def is_nan(value):
    try:
        result = np.isnan(value)
    except TypeError:
        result = False
    return result

class Ebay:
    """Interface to Ebay Trading API.
    Really an example of bundling up py_ebay-sdk
    """
    def  __init__(self):
        self.api = Trading()
        self.num_api_calls = 0
        self.added_items = False
        # These are the fields for the dataframe.  At the moment this is smaller subset of data
        # Note that to get some of this data you may need to do multiple calls eg EAN
        self.ebay_fields = ['ItemID', 'Title', 'Quantity', 'HitCount', 'BuyItNowPrice',
                            'Description', 'SKU', 'MPN', 'EAN', 'ReturnPolicy', 'ListingStatus']

    def trading(self, call, data={}):
        response = self.api.execute(call, data)
        self.num_api_calls += 1
        return response

    @property
    def user(self):
        try:
            response = self.trading('GetUser')
            result = response.dict()['User']['UserID']
        except ConnectionError as e:
            # print(e)
            result = e.response.dict()
        return result

    @property
    def count(self):
        try:
            result = self._count
        except AttributeError:  # Hasn't yet been called
            result = 0  # default
            try:
                now = dt.datetime.now()
                listData = {
                    # 'DetailLevel': 'ReturnAll',
                    'StartTimeFrom': now - dt.timedelta(days=60),
                    'StartTimeTo': now,
                    'Pagination': {
                        'EntriesPerPage': '2',
                        'PageNumber': '1'
                    }
                }
                response = self.trading('GetSellerList', listData)
                result = int(response.dict()['PaginationResult']['TotalNumberOfEntries'])
                self._count = result
            except ConnectionError as e:
                print(listData)
                print(e)
                print(e.response.dict())
        return result

    def active(self, item_dictionary):
        """ Given an Item dictionary """
        try:
            result = item_dictionary['SellingStatus']['ListingStatus'] == 'Active'
        except:
            result = False
        return result

    def fill_page(self, page_number=1, entries_per_page=5, print_first=False):
        """This is only go to fill active items"""
        try:
            now = dt.datetime.now()
            listData = {
                'DetailLevel': 'ReturnAll',
                'StartTimeFrom': now - dt.timedelta(days=60),
                'StartTimeTo': now,
                'Pagination': {
                    'EntriesPerPage': '{}'.format(entries_per_page),
                    'PageNumber': '{}'.format(page_number)
                }
            }
            response = self.trading('GetSellerList', listData)
            # print('Number of items for sale = {}'.format(response.dict()['PaginationResult']['TotalNumberOfEntries']))
            index = (page_number - 1) * entries_per_page
            for d in response.dict()['ItemArray']['Item']:
                if print_first:
                    print('Page number {}'.format(page_number))
                    print('{}'.format(response.dict()))
                    print_first = False
                if self.active(d):
                    for f in self.ebay_fields:
                        try:
                            if f == 'EAN':
                                self.df.loc[self.high_index][f] = d['ReturnPolicy'][f]
                            elif f == 'ListingStatus':
                                self.df.loc[self.high_index][f] = d['SellingStatus'][f]
                            else:
                                self.df.loc[self.high_index][f] = d[f]
                        except KeyError:  # some fields may be absent eg if no hitcounter is setup then there will be no
                            # hitcount
                            pass
                        except TypeError:  # Probably due to SKU but not sure exact problem
                            pass
                    self.high_index += 1
        except ConnectionError as e:
            print(listData)
            print(e)
            print(e.response.dict())
            print('\n')

    def fill_pages(self):
        num_pages = (self.count + 4) / 5
        self.high_index = 0
        for page_number in range(num_pages):
            if page_number == 1:
                self.fill_page(page_number + 1) #  , print_first=True)
            else:
                self.fill_page(page_number + 1)

    @ property
    def allitems_dataframe(self):
        index = range(self.count)
        self.df = pd.DataFrame(index=index, columns=self.ebay_fields)
        self.fill_pages()
        # Not all the listings may be active so get rid of the ones that are not.
        self.df = self.df.iloc[:self.high_index]
        print('Add EAN')
        self.add_EAN()
        return self.df

    def add_EAN(self, get_even_if_sku = True):
        """This addes EAN data to each item.  Note with a large catalogue this may produce
        a single API call for every item.  So the maxiumum number of API calls could be
        exceeded. By setting get_even_if_sku False and using the SKU data as in an index you
        can reduce the number of calls."""
        for i, row_tuple in enumerate(self.df.iterrows()):
            row = row_tuple[1]
            if is_nan(row['SKU']) or get_even_if_sku:  # See if we can find an EAN/MPN to enrich the data
                if is_nan(row['EAN']):
                    EAN, MPN = self.get_EAN(row['ItemID'])
                    if EAN != '':
                        row['EAN'] = EAN
                    if MPN != '':
                        row['MPN'] = MPN

    def get_EAN(self, item_id):
        class NonLocal:
            EAN = ''
            MPN = ''
        def parse_item_specifics(name_value_dict):
            if name_value_dict['Name'] == 'EAN':
                NonLocal.EAN = name_value_dict['Value']
            elif name_value_dict['Name'] == 'MPN':
                NonLocal.MPN = name_value_dict['Value']
        try:
            assert item_id != 'nan', TypeError
            listData = {
                'ItemID': '{}'.format(item_id),
                'IncludeItemSpecifics': True,
            }
            response = self.trading('GetItem', listData)
            try:
                result = response.dict()['Item']['ItemSpecifics']['NameValueList']
                # result may be a single dict or a list of dicts
                if isinstance(result, list):
                    for d in result:
                        parse_item_specifics(d)
                else:  # Return only a single value as a dictionary
                    parse_item_specifics(result)
            except TypeError:
                print('Cannot parse this reponse.  In full is:\n{}\n\n'.format(response.dict()))
        except (ConnectionError, TypeError) as e:
            print(listData)
            print(e)
            try:
                print(e.response.dict())
            except AttributeError:
                print('No response dict')
        return NonLocal.EAN, NonLocal.MPN

    def set_sku(self, item, sku):
        try:
            listData = {
                'Item' : {
                    'ItemID' : '{}'.format(item),
                    'SKU' : '{}'.format(sku)
                }
            }
            response = self.trading('ReviseItem', listData)
        except ConnectionError as e:
            print(listData)
            print(e)
            try:
                print(e.response.dict())
            except AttributeError:
                print('No response dict')

    def set_MPN(self, item, MPN, brand = 'The Bedding Specialist'):
        try:
            listData = {
                'Item' : {
                    'ItemID' : '{}'.format(item),
                    'ItemSpecifics': {
                        'NameValueList': [
                            {'name': 'Brand', 'value': '{}'.format(brand)},
                            {'name': 'MPN',   'value': '{}'.format(MPN)}
                        ]
                    }
                }
            }
            response = self.trading('ReviseFixedPriceItem', listData)
        except ConnectionError as e:
            print(listData)
            print(e)
            try:
                print(e.response.dict())
            except AttributeError:
                print('No response dict')


    @property
    def version(self):
        return '0.20'


    def set_description(self, item, description):
        try:
            listData = {
                'Item' : {
                    'ItemID': '{}'.format(item),
                    'Description': '<![CDATA[{}]]>'.format(description.encode('utf8'))
                }
            }
            response = self.trading('ReviseItem', listData)
        except ConnectionError as e:
            print(listData)
            print(e)
            try:
                print(e.response.dict())
            except AttributeError:
                print('No response dict')

