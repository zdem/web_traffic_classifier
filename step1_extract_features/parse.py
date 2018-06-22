import re
import numpy as np

# Extract five features from a single HTTP_request as described in Althubiti et al paper.
def extract_features(HTTP_request, debug = False):
	features = np.zeros(5)

	# Extract the full path
	path = re.match('(http.*) ',HTTP_request).group(1)

	# Extract the arguments
	r = re.search('Content-Length:\s*(\d+)',HTTP_request)
	if (r):
		if (debug):
			print "POST\n"
		# This is a POST request: get the arguments from the end of the request
		argument_len = int(r.group(1))
		arguments = HTTP_request[len(HTTP_request)-argument_len-4:len(HTTP_request)-4]

		# Generate the path as in GET request
		path = path + '?' + arguments
	else:
		if (debug):
			print "GET\n"
		# This is a GET request: get the arguments from the path
		arguments = re.search('\?(.*)',path)
		if (arguments):
			arguments = arguments.group(1)
		else:
			arguments = ''

	arguments = re.sub('\n','', arguments)
	arguments = re.sub('\r','', arguments)

	#1. Length of the request
	features[0] = len(HTTP_request)

	#2. Length of the arguments
	features[1] = len(arguments) - len(re.findall('&', arguments))

	#3. Number of arguments
	features[2] = len(re.split('&', arguments))

	#4. Length of the path
	features[3] = len(path)

	#5. Number of special chars in the path
	features[4] = len(re.findall('\W', path))
	
	if (debug):
		print "Path: ",path
		print "Arguments: ", arguments
		print features

	return features

with open('input_data/normalTrafficAll.txt', 'r') as input_file: data_normal = input_file.read()
with open('input_data/anomalousTrafficTest.txt', 'r') as input_file: data_anomalous = input_file.read()

# Split the raw data into individual HTTP requests using 'GET ' and 'POST ' as delimiters

normal_HTTP_requests = re.split('GET |POST ', data_normal)
normal_HTTP_requests.pop(0); #The first string is always empty
num_normal_HTTP_requests = len(normal_HTTP_requests)

anomalous_HTTP_requests = re.split('GET |POST ', data_anomalous)
anomalous_HTTP_requests.pop(0); #The first string is always empty
num_anomalous_HTTP_requests = len(anomalous_HTTP_requests)

print "Found ",num_normal_HTTP_requests," normal HTTP requests"
print "Found ",num_anomalous_HTTP_requests," anomalous HTTP requests\n\n"

# Generate the training data set with two labels: normal = 0, anomalous = 1

n_samples = num_normal_HTTP_requests + num_anomalous_HTTP_requests
n_features = 5

X = np.zeros([n_samples,n_features])
y = np.zeros(n_samples)

i = -1
for HTTP_request in normal_HTTP_requests:
        i = i + 1
        X[i,:] = extract_features(HTTP_request)
        y[i] = 0

for HTTP_request in anomalous_HTTP_requests:
        i = i + 1
        X[i,:] = extract_features(HTTP_request)
        y[i] = 1

# TODO clean up the features removing the redundant POST/GET equivalent vectors using a moveable window: the equivalent entries follow each other.

np.savez('training_data.npz', X, y)
