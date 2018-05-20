import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import linear_model
import seaborn as sns
import operator
import sys
import zipfile
import scipy.sparse as sp
import csv

columns_to_vectorize = {
    'Title': 6,
    'FullDescription': 200,
    'LocationRaw': 10,
    'LocationNormalized':10
}

NUMBER_OF_ROWS = 100

new_file = open("Vectorized.csv","w")
writer = csv.writer(new_file, delimiter=',')

with zipfile.ZipFile('Train_rev1.zip') as myzip:
    with myzip.open('Train_rev1.csv') as myfile:
        df = pd.read_csv(myfile, nrows=NUMBER_OF_ROWS)

definite_row = []

for i in range(0, NUMBER_OF_ROWS + 1):
    definite_row.append([])

for i in range(0, 226):
    definite_row[0].append(i)

definite_row[0].append('Salary')
writer.writerow(definite_row[0])

for key in columns_to_vectorize:
    count_vectorizer = CountVectorizer(max_features=columns_to_vectorize[key], stop_words='english')
    transformed = count_vectorizer.fit_transform(df[key].values.astype('U')).toarray()
    for index, value in enumerate(transformed):
        value = value.tolist()
        definite_row[index].extend(value)

for i in range(0, NUMBER_OF_ROWS-1):
    definite_row[i + 1].extend([str(df['SalaryNormalized'][i])])
    writer.writerow(definite_row[i + 1])

new_file.close()
