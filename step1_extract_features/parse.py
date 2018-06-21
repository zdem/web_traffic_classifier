import re

# Extract five features from a single HTTP_request as described in Althubiti et al paper.
def extract_features(HTTP_request, debug = False):
	features = [0,0,0,0,0]

	# Extract the full path
	path = re.match("(http.*) ",HTTP_request).group()
	path = re.sub(' ','',path)

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

# TODO??? make the file a command-line argument, 2nd cmd argument should be the label: 0 or 1
with open('input_data/normalTrafficAll.txt', 'r') as input_file: data = input_file.read()

# Parse the raw data obtaining a two strings per request: the first string contains GET or POST and the 2nd one the body of the request
normal_HTTP_requests = re.split('GET |POST ', data)
normal_HTTP_requests.pop(0); #Remove the first string which is always empty

num_normal_HTTP_requests = len(normal_HTTP_requests)
print "Found ",num_normal_HTTP_requests," HTTP requests\n\n"

normal_HTTP_features = []
for HTTP_request in normal_HTTP_requests:
	normal_HTTP_features.append(extract_features(HTTP_request))

# TODO clean up the features removing the redundant POST/GET equivalent vectors using a moveable window: the equivalent entries follow each other.
