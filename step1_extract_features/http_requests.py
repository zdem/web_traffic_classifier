import re
import numpy as np
from urlparse import urlparse, parse_qs

# Extract the five features from a single HTTP_request as described in Althubiti et al paper.
# These are formed from the URI only: the rest of the HTTP request is not useful.
def extract_features(HTTP_request, debug = False):
	features = np.zeros(5)

	# Extract the method and the URI
	first_line = re.match('(.*) (http.*) HTTP',HTTP_request)
	method = first_line.group(1)
	uri_string = first_line.group(2)

	# Remove the redundant information from the request body
	stripped_request = re.sub('User-Agent:.*Connection: close|[\n\r]','',HTTP_request)

	if (method != 'GET'):
		post_query = re.search('Content-Length:\s*\d+(.*)',stripped_request)
                arguments = re.sub('\n|\r','',post_query.group(1))
		uri_string = uri_string + '?' + arguments

	stripped_request = uri_string

	# Parse the URI into path and arguments
	uri = urlparse(uri_string)

	path = uri.path
	arguments = parse_qs(uri.query)

	#1. Length of the request
	features[0] = len(stripped_request)

	#2. Length of the arguments
	features[1] = 0
	for parameter, value in arguments.iteritems():
		features[1] += len(parameter+(''.join(value)))

	#3. Number of arguments
	features[2] = len(arguments)

	#4. Length of the path
	features[3] = len(path)

	#5. Number of special chars in the path
	features[4] = len(re.findall('\W',path))

	if (debug):
                print "\n" + method
		print path
		print arguments
		print features

	return features

# Predicts whether a given HTTP request string is normal (=0) or anomalous (=1)
def normal_or_anomalous(HTTP_request):

	features = extract_features(HTTP_request)
	theta = [0.16163343, -0.16745845, -0.23716181, -0.18078638, -0.02442735]

	p = 1.0/(1+np.exp(-(np.dot(theta,features)-4.19002258)))
	if p >= 0.5:
		p = 1
	else:
		p = 0

	return p

class dataset:

	# Read-in the dataset and parse it into individual HTTP requests.
	def __init__(self, path_to_file):

		self.HTTP_requests = []
		self.n_requests = 0
		self.path_to_file = path_to_file

		with open(path_to_file, 'r') as input_file: data = input_file.read()

		# Split the raw data into individual methods (GET, POST, PUT) request strings
		methods_requests = re.split('(GET |POST |PUT )', data)
		methods_requests.pop(0)

		only_methods = methods_requests[::2]
		only_requests = methods_requests[1:][::2]

		self.HTTP_requests =  [method + request for method,request in zip(only_methods,only_requests)]

		self.n_requests = len(self.HTTP_requests)
		print "\nFound ", self.n_requests, " HTTP requests in file: ", path_to_file

	# Generate two sets of data (training, testing) splitting the whole data set according to the fraction of training data required and
	# assign a label to the data too.
	def extract_labelled_HTTP_features(self,label):

		X = []
		y = []

		for HTTP_request in self.HTTP_requests:
			X.append(extract_features(HTTP_request))
			y.append(label)

		print "\nData from",self.path_to_file,"have been exported"
                print "Label assigned:", label

		return X, y
