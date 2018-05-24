import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from numpy import isnan
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, median_absolute_error
from sklearn.metrics import explained_variance_score

df = pd.read_csv('FinalTrainFixdColumns.csv')

df['salarynormalized'] = np.log(df['salarynormalized'])
for column in df:
    df[column].fillna(0, inplace=True)

X = df.drop('salarynormalized', axis=1).values
y = df['salarynormalized'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

reg = RandomForestRegressor(max_depth=2, random_state=42)

reg.fit(X_train, y_train)

result = reg.predict(X_test)

# print('Coefficients: \n', reg.coef_)
print("median_absolute_error: %.2f" % median_absolute_error(y_test, result))
print('Variance score: %.2f' % r2_score(y_test, result))
print(explained_variance_score(y_test, result))
