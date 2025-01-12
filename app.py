from shipment.logger import logging
from shipment.exception import shippingException
import sys

logging.info("Testing logging setup")

try:
    a = 2 + '3'
    print(a)
except Exception as e:
    raise shippingException(e, sys) from e