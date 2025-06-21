import sys,os
from mlops.logger import logging
from mlops.exception import NetworkSecurityException
logging.info('welcome to custom log')
# try:
#     a=2/0
# except Exception as e:
#     raise NetworkSecurityException(e,sys)