import numpy as np
import pandas as pd
from sklearn import preprocessing, tree
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

# Create classifier
regr_1 = tree.DecisionTreeRegressor(max_depth=5)
regr_2 = tree.DecisionTreeRegressor(max_depth=10)

# Fit model
regr_1.fit(X_train, y_train)
regr_2.fit(X_train, y_train)

# Predict
y_pred_1 = regr_1.predict(X_test)
y_pred_2 = regr_2.predict(X_test)

# Calculate score
score1 = explained_variance_score(y_test, y_pred_1)
score2 = explained_variance_score(y_test, y_pred_2)

print(score1)
print(score2)
