from email import header
from os import sep
from unittest import skip
from urllib import request
import pandas as pd
from pyparsing import col
from matplotlib import pyplot as pyp
import seaborn as sns
import plotly as pl
from sklearn.model_selection import learning_curve
import sklearn
import http

### Starting ###
dframe= pd.read_csv('data/owid-covid-data.csv')
ldata = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')
# ldata = pd.save('https://github.com/owid/covid-19-data/blob/master/public/data/latest/owid-covid-latest.csv',on_bad_lines='skip')
print(ldata)
