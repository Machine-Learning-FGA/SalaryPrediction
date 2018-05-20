import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, median_absolute_error


df = pd.read_csv('Vectorized.csv')


X = df.drop('Salary', axis=1).values
y = df['Salary'].values

print(X)
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)

result = reg.predict(X_test)

print('Coefficients: \n', reg.coef_)
print("median_absolute_error: %.2f" % median_absolute_error(y_test, result))
print('Variance score: %.2f' % r2_score(y_test, result))
