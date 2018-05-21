import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score
from sklearn import linear_model
import seaborn as sns
import operator
import sys
import zipfile

## y = a1x1 + a2x2 + a3x3 +... +anxn + b (n é o número de features)


with zipfile.ZipFile('Train_rev1.zip') as myzip:
    with myzip.open('Train_rev1.csv') as myfile:
        df = pd.read_csv(myfile)



#drop na coluna salary raw
# df = df.drop('SalaryRaw', 1)
# df = df.drop('Id', 1)
number = LabelEncoder()

# transforma dataframe em int
for column in df:
    if not df[column].dtype == np.int64:
        df[column] = number.fit_transform(df[column].astype(str))


#matriz de correlação
correlation = df.corr()
plt.figure(figsize=(10,10))
g = sns.heatmap(correlation, vmax=1, square=True,annot=True,cmap='RdYlGn',xticklabels=True,yticklabels=True, annot_kws={"size":7})
g.set_yticklabels(g.get_yticklabels(), rotation =0)
g.set_xticklabels(g.get_yticklabels(), size=7, rotation =90)
plt.title('Correlation between different features')
sns.plt.show()


X = df.drop('SalaryNormalized', axis=1).values
y = df['SalaryNormalized'].values
# primeiro método
X_salary = X[:, 10]

y = y.reshape(-1, 1)
X_salary = X_salary.reshape(-1, 1)

# scatter plot
plt.scatter(X_salary, y)
plt.ylabel('Salary')
plt.xlabel('Number of salarys')
plt.show()

#hist plot salário
# df['SalaryNormalized_log'] = np.log(df['SalaryNormalized'])
# plt.hist(df['SalaryNormalized_log'], bins=20)
# plt.ylabel('Frequencia')
# plt.xlabel('Salarios')
# plt.title('Histograma de salarios(log)')
# plt.show()

# reg = linear_model.LinearRegression()
# reg.fit(X_salary, y)
# prediction_space = np.linspace(min(X_salary), max(X_salary)).reshape(-1, 1)
# plt.scatter(X_salary, y, color='blue')
# plt.plot(prediction_space, reg.predict(prediction_space),color='black',linewidth=3)
# plt.show()

#segundo método
# X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=42)
# reg_all = linear_model.LinearRegression()
#
# reg_all.fit(X_treino, y_treino)
# y_pred = reg_all.predict(X_teste)
# print('score')
# print('\n',reg_all.score(X_teste, y_teste))
# print('\nexplained_variance_score')
# print('\n',explained_variance_score(y_teste, y_pred))
# print('\nmean_absolute_error')
# print('\n',mean_absolute_error(y_teste, y_pred))
# print('\nmean_absolute_error')
# print('\n',mean_squared_error(y_teste, y_pred))
# print('\nr^2 score')
# print('\n',r2_score(y_teste, y_pred))
