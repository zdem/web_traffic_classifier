import http_requests
import numpy as np

normal_requests = http_requests.dataset('input_data/normalTrafficAll.txt')
X_normal, y_normal = normal_requests.extract_labelled_HTTP_features(0)

anomalous_requests = http_requests.dataset('input_data/anomalousTrafficTest.txt')
X_anomalous, y_anomalous = anomalous_requests.extract_labelled_HTTP_features(1)

X = np.concatenate((X_normal,X_anomalous),axis=0)
y = np.concatenate((y_normal,y_anomalous),axis=0)

print X
print y

np.savez('training_data.npz', X, y)
