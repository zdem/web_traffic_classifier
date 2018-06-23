import http_requests
import numpy as np

normal_requests = http_requests.dataset('input_data/normalTrafficAll.txt')
X_normal, y_normal, X_normal_test, y_normal_test = normal_requests.extract_labelled_HTTP_features(0.6,0)

anomalous_requests = http_requests.dataset('input_data/anomalousTrafficTest.txt')
X_anomalous, y_anomalous, X_anomalous_test, y_anomalous_test = anomalous_requests.extract_labelled_HTTP_features(0.6,1)

X = np.concatenate((X_normal,X_anomalous),axis=0)
y = np.concatenate((y_normal,y_anomalous),axis=0)

np.savez('training_data.npz', X, y)

X = np.concatenate((X_normal_test,X_anomalous_test),axis=0)
y = np.concatenate((y_normal_test,y_anomalous_test),axis=0)

np.savez('test_data.npz', X, y)

