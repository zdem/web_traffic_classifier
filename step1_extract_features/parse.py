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
		# This is a POST or a PUT request: get the arguments from the line following 'Content-Length'
                typ = 'POST or PUT'
                arguments = re.sub('\n|\r','',HTTP_request[r.end(1)+1:])
		argument_len = len(arguments)

                if argument_len != int(r.group(1)):
                    print HTTP_request
                    print arguments
                    print "error in parsing POST or PUT arguments"
                    exit()

		# Generate the path as in GET request
		path = path + '?' + arguments
	else:
		# This is a GET request: get the arguments directly from the path
                typ = 'GET '
		arguments = re.search('\?(.*)',path)
		if (arguments):
			arguments = arguments.group(1)
		else:
			arguments = ''

	arguments = re.sub('\n|\r','', arguments)

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
                print "\n" + typ
		print "Path:", path
		print "Arguments:", arguments
		print features

	return features

with open('input_data/normalTrafficAll.txt', 'r') as input_file: data_normal = input_file.read()
with open('input_data/anomalousTrafficTest.txt', 'r') as input_file: data_anomalous = input_file.read()

# Split the raw data into individual HTTP requests using 'GET ' and 'POST ' as delimiters

normal_HTTP_requests = re.split('GET |POST |PUT ', data_normal)
normal_HTTP_requests.pop(0)

anomalous_HTTP_requests = re.split('GET |POST |PUT ', data_anomalous)
anomalous_HTTP_requests.pop(0)

print "Found ",len(normal_HTTP_requests)," normal HTTP requests"
print "Found ",len(anomalous_HTTP_requests)," anomalous HTTP requests\n"

# Generate the training data set (X,y) with two y labels: normal = 0, anomalous = 1

X = []
y = []
for HTTP_request in normal_HTTP_requests:
        X.append(extract_features(HTTP_request))
        y.append(0)

for HTTP_request in anomalous_HTTP_requests:
        X.append(extract_features(HTTP_request))
        y.append(1)

print "Number of samples = ", len(y)
np.savez('training_data.npz', X, y)
