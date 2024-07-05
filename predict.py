import sys
import joblib
import numpy as np
import json
import sys
import traceback



# Load the saved model and scaler
kmeans = joblib.load('kmeans_model.joblib')
scaler = joblib.load('scaler.joblib')


# Get input from command line arguments
x, y, speed  = map(float, sys.argv[1:])

# Prepare the input data
input_data = np.array([[ x, y, speed]])

# Scale the input data
scaled_data = scaler.transform(input_data)

# Predict the cluster
cluster = kmeans.predict(scaled_data)[0]

# Print the result as JSON
print(json.dumps({'cluster': int(cluster)}))