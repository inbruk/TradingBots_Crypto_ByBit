import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from IPython.core.display import display
from update_candles import *
from update_equations import *
from update_orders import *
from select_best_cur import *

best_curs = select_best_currencies()
print()
