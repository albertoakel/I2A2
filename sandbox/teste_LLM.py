import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
# import itertools as itera
import seaborn as sns
# import plotly.express as px
# import warnings
# from matplotlib.ticker import MultipleLocator
# import time
# import matplotlib.ticker as ticker
#inicio = time.time()

plt.rcParams["figure.dpi"] = 180
sns.set_style("whitegrid")
pd.set_option('display.width',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth',None)

#warnings.filterwarnings("ignore", category=FutureWarning)

data_dir='/home/akel/PycharmProjects/I2A2/data/'
df = pd.read_csv(data_dir+'base_merge_interp.csv')

df['data'] = pd.to_datetime(df['data'])

print(df.dtypes)

