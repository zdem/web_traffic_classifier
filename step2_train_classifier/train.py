import numpy as np
from sklearn.linear_model import LogisticRegression

training_data = np.load('../step1_extract_features/training_data.npz')
#training_data = np.load('../training_data.npz')
X = training_data['arr_0']
y = training_data['arr_1']

print "Data set read from disk:"
print "Number of samples = ",len(y)
print "Number of features = ",len(X[0,:])

model = LogisticRegression(C=0.01) #regularization using C does not affect the results too much
model.fit(X, y)

preds = model.predict(X)
print (preds == y).mean()

# Add all unique quadratic terms

Xquad = X
col = np.zeros(len(y))
for col_i in range(0,len(X[0,:])):
	for col_j in range(0,col_i+1):
		col = X[:,col_i] * X[:,col_j]
		Xquad = np.column_stack((Xquad,col))

model = LogisticRegression(C=1) #regularization using C does not affect the results too much
model.fit(Xquad, y)

preds = model.predict(Xquad)
print (preds == y).mean()
print model.score(Xquad,y)


# Remove repetitive entries from the training data and repeat the fit

Xy = np.column_stack((X,y))
Xy = np.asarray(np.unique(Xy, axis=0))

n_samples = len(Xy)
n_features = len(Xy[0])-1

print "Number of unique samples = ", n_samples
print "Number of features = ", n_features

y = Xy[:,n_features]
X = np.delete(Xy,n_features,1)

model.fit(X, y)

preds = model.predict(X)
print (preds == y).mean()

# Add all unique quadratic terms

Xquad = X
col = np.zeros(len(y))
for col_i in range(0,len(X[0,:])):
	for col_j in range(0,col_i+1):
		col = X[:,col_i] * X[:,col_j]
		Xquad = np.column_stack((Xquad,col))

model = LogisticRegression(C=1) #regularization using C does not affect the results too much
model.fit(Xquad, y)

preds = model.predict(Xquad)
print (preds == y).mean()
