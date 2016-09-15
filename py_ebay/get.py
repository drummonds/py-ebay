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

class Ebay():
    """Interface to SAGE line 50 account system.
    Really an example of bundling up py_ebay-sdk
    """
    def  __init__(self):
        self.api = Trading()


    def user(self):
        try:
            response = self.api.execute('GetUser', {})
            result = response.dict()['User']['UserID']
        except ConnectionError as e:
            # print(e)
            result = e.response.dict()
        return result

