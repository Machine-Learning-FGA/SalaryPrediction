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
    # 'FullDescription': 200,
    # 'LocationRaw': 10,
    # 'LocationNormalized':10
}

new_file = open("Vectorized.csv","w")
array = []

with zipfile.ZipFile('Train_rev1.zip') as myzip:
    with myzip.open('Train_rev1.csv') as myfile:
        df = pd.read_csv(myfile, nrows=1000)

writer = csv.writer(new_file, delimiter=',')


for key in columns_to_vectorize:
    count_vectorizer = CountVectorizer(max_features=columns_to_vectorize['Title'], stop_words='english')
    transformed = count_vectorizer.fit_transform(df['Title'].head(1000)).toarray()
    for value in transformed:
        print(count_vectorizer.vocabulary_)
        print(value)
        writer.writerow(value)
        # new_file.write(str(value) + ',')
    # array.append(transformed)
    # print(array)
    # new_file.write(transformed)

new_file.close()

# df['ContractType'] = df['ContractType'].replace(['part_time'], 0)
# df['ContractType'] = df['ContractType'].replace(['full_time'], 1)
# df['ContractTime'] = df['ContractTime'].replace(['permanent'], 0)
# df['ContractTime'] = df['ContractTime'].replace(['contract'], 1)
#
#
# X = df.drop('SalaryNormalized', axis=1)
# y = df['SalaryNormalized']
#
# print(X)
#
# X = X[:, 10]
# X = X.reshape(-1, 1)
# y = y.reshape(-1, 1)
#
# print(X)
