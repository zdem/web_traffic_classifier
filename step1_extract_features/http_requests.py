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

class dataset:

	# Read-in the dataset and parse it into individual HTTP requests.
	def __init__(self, path_to_file):

		self.HTTP_requests = []
		self.n_requests = 0
		self.path_to_file = path_to_file

		with open(path_to_file, 'r') as input_file: data = input_file.read()

		# Split the raw data into individual HTTP requests using 'GET ', 'POST ' and 'PUT ' as delimiters
		self.HTTP_requests = re.split('GET |POST |PUT ', data)
		self.HTTP_requests.pop(0)

		self.n_requests = len(self.HTTP_requests)
		print "Found ", self.n_requests, " HTTP requests in file: ", path_to_file

	# Generate two sets of data (training, testing) splitting the whole data set according to the fraction of training data required.
	def extract_labelled_HTTP_features(self,fraction_training,label):

		X_training = []
		y_training = []

		X_testing = []
		y_testing = []

		if fraction_training < 0 or fraction_training > 1:
			print "Error on input: fraction_training not in range [0,1]"
			exit()

		fraction_test = 1 - fraction_training

		last_training_request = int(self.n_requests * fraction_training)

		for i,HTTP_request in enumerate(self.HTTP_requests):

			HTTP_features = extract_features(HTTP_request)

			if i+1 <= last_training_request:
				X_training.append(HTTP_features)
				y_training.append(label)
			else:
				X_testing.append(HTTP_features)
				y_testing.append(label)

		print "Data from",self.path_to_file,"have been split into a fraction of",fraction_training, "for training and a fraction of ",fraction_test,"for testing"
                print "Label assigned:", label
		print "Total number of training requests obtained:",last_training_request

		return X_training, y_training, X_testing, y_testing
