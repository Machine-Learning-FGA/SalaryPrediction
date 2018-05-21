import numpy as np
import pandas as pd
from sklearn import preprocessing, tree, linear_model
from sklearn.metrics import explained_variance_score
from sklearn.model_selection import cross_val_score, train_test_split

# Load content of file in memory
df = pd.read_csv("Vectorized.csv", header=None)

# Separate features and targets
targets = df.iloc[:,-1:]
features = df.iloc[:,0:-1]

# Separate Test and Train data randomly
X_train, X_test, y_train, y_test = train_test_split(
    features, targets, test_size=0.4, random_state=42)

# Create classifiers
decis_tree_regr_1 = tree.DecisionTreeRegressor(max_depth=5)
decis_tree_regr_2 = tree.DecisionTreeRegressor(max_depth=10)
lasso_regr_1 = linear_model.Lasso(0.1)
lasso_regr_2 = linear_model.Lasso(1)

# Fit model
decis_tree_regr_1.fit(X_train, y_train)
decis_tree_regr_2.fit(X_train, y_train)
lasso_regr_1.fit(X_train, y_train)
lasso_regr_2.fit(X_train, y_train)

# Predict
y_decis_tree_1 = regr_1.predict(X_test)
y_decis_tree_2 = regr_2.predict(X_test)
y_lasso_regr_1 = lasso_regr.predict(X_test)
y_lasso_regr_2 = lasso_regr.predict(X_test)

# Calculate score
score_decis_tree_1 = explained_variance_score(y_test, y_decis_tree_1)
score_decis_tree_2 = explained_variance_score(y_test, y_decis_tree_2)
score_lasso_1 = explained_variance_score(y_test, y_lasso_regr_1)
score_lasso_2 = explained_variance_score(y_test, y_lasso_regr_2)

print(score_decis_tree_1)
print(score_decis_tree_1)
print(score_lasso_1)
print(score_lasso_2)
