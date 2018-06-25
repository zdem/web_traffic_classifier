import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

training_data = np.load('training_data.npz')
X = training_data['arr_0']
y = training_data['arr_1']

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=0)

print "Data set read from disk:"
print "Number of samples = ",len(y)
print "Number of features = ",len(X[0,:])

model = LogisticRegression(C=0.01) #regularization using C does not affect the results too much
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

print model.coef_
print model.intercept_

# Add all unique quadratic terms

Xquad = X_train
col = np.zeros(len(y))
for col_i in range(0,len(X_train[0,:])):
	for col_j in range(0,col_i+1):
		col = X_train[:,col_i] * X_train[:,col_j]
		Xquad = np.column_stack((Xquad,col))

model = LogisticRegression(C=1) #regularization using C does not affect the results too much
model.fit(Xquad, y_train)

y_pred = model.predict(Xquad)
print(classification_report(y_train, y_pred))

print model.coef_
print model.intercept_

# Remove repetitive entries from the training data and repeat the fit

Xy = np.column_stack((X_train,y_train))
Xy = np.asarray(np.unique(Xy, axis=0))

n_samples = len(Xy)
n_features = len(Xy[0])-1

print "Number of unique samples = ", n_samples
print "Number of features = ", n_features

y = Xy[:,n_features]
X_train = np.delete(Xy,n_features,1)

model = LogisticRegression(C=0.01) #regularization using C does not affect the results too much
model.fit(X_train, y)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

print model.coef_
print model.intercept_

# Add all unique quadratic terms

Xquad = X_train
col = np.zeros(len(y))
for col_i in range(0,len(X[0,:])):
	for col_j in range(0,col_i+1):
		col = X_train[:,col_i] * X_train[:,col_j]
		Xquad = np.column_stack((Xquad,col))

model = LogisticRegression(C=0.01) #regularization using C does not affect the results too much
model.fit(Xquad, y)

y_pred = model.predict(Xquad)
print(classification_report(y, y_pred))

print model.coef_
print model.intercept_
