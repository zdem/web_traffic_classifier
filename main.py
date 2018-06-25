import http_requests
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

normal_requests = http_requests.dataset('input_data/normalTrafficAll.txt')
X_normal, y_normal = normal_requests.extract_labelled_HTTP_features(0)

anomalous_requests = http_requests.dataset('input_data/anomalousTrafficTest.txt')
X_anomalous, y_anomalous = anomalous_requests.extract_labelled_HTTP_features(1)

X = np.concatenate((X_normal,X_anomalous),axis=0)
y = np.concatenate((y_normal,y_anomalous),axis=0)

print X
print y

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=0)

print "Number of samples = ",len(y)
print "Number of features = ",len(X[0,:])
#
# Model 1: linear features
#
model = LogisticRegression(C=0.01) #regularization using C does not affect the results too much
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

print model.coef_
print model.intercept_

# 
# Model 2: linear + quadratic features
#

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

#
# Remove repetitive entries from the training data and repeat the fit
#

Xy = np.column_stack((X_train,y_train))
Xy = np.asarray(np.unique(Xy, axis=0))

n_samples = len(Xy)
n_features = len(Xy[0])-1

print "Number of unique samples = ", n_samples
print "Number of features = ", n_features

y = Xy[:,n_features]
X_train = np.delete(Xy,n_features,1)

# 
# Model 3: linear features, unique set of training points
#

model = LogisticRegression(C=0.01) #regularization using C does not affect the results too much
model.fit(X_train, y)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

print model.coef_
print model.intercept_

#
# Model 4: linear + quadratic features, unique set of training points
#

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
