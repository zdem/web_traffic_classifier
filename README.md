# web_traffic_classifier

Scripts for determining the logistic regression model for classification of HTTP requests into normal and anomalous.
The data set used in the fitting is the [CSIC 2010 dataset](http://www.isi.csic.es/dataset/).

The script `main.py` performs first parsing of the input data set using the methods and functions implemented in the `http_requests.py` module and then proceeds to 
construct four different logistic regression models using the `scikit-learn` library.

The final decision function `http_requests.normal_or_anomalous` implements the parameters of the (linear) Model 1 as defined in `main.py`.
