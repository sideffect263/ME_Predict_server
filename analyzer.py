import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import time
from tqdm import tqdm



# Load and preprocess your dataset as previously shown
print("starting analyzer.py")

print("loading mousedata.tsv")

# Load the TSV datasets
mousedata = pd.read_csv('mousedata.tsv', sep='\t', parse_dates=['Time'])
mouse_mov_speeds = pd.read_csv('mouse_mov_speeds.tsv', sep='\t', parse_dates=['Time'])


print("checking and removing unnecessary columns")
# Check and remove any unnecessary columns
mousedata = mousedata[['Time', 'Event_Type', 'X', 'Y', 'Daylight']]
mouse_mov_speeds = mouse_mov_speeds[['Time', 'Speed(ms)', 'Daylight']]


print("merging datasets on timestamp")
# Merge datasets on timestamp
merged_data = pd.merge_asof(mousedata.sort_values('Time'), mouse_mov_speeds.sort_values('Time'), on='Time', direction='nearest')
merged_data.dropna(inplace=True)

print(merged_data.head())
print("converting categorical data to numerical data")

data = merged_data[['Time', 'Event_Type', 'X', 'Y', 'Speed(ms)']]

# Rename columns for consistency
data.columns = ['timestamp', 'event_type', 'x', 'y', 'speed'] 
data = data.dropna()

# Feature engineering
data['distance'] = np.sqrt((data['x'].diff()**2) + (data['y'].diff()**2))
data['time_diff'] = data['timestamp'].diff()
data['time_diff_seconds'] = data['time_diff'].dt.total_seconds()
data['speed'] = data['distance'] / data['time_diff_seconds']
data['acceleration'] = data['speed'].diff() / data['time_diff_seconds']
data['distance_from_last'] = data['distance']
data['idle_time'] = data['time_diff_seconds']
data.loc[data['distance'] > 0, 'idle_time'] = 0

# Drop NA values created by diff
data = data.dropna()

# Replace infinities and very large values
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data = data.dropna()

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(data[['x', 'y', 'speed', 'acceleration', 'distance_from_last', 'idle_time']])

# Apply DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=2)

print(scaled_features[100:])
dbscan.fit(scaled_features[10:])

# Assign cluster labels to data
data['cluster'] = dbscan.labels_

# Plotting the clusters (example: 3D plot with x, y, and speed)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(data['x'], data['y'], data['speed'], c=data['cluster'], cmap='viridis')
legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
ax.add_artist(legend1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Speed')
plt.title('3D Scatter Plot of DBSCAN Clusters')
plt.show()

# Analyze the clusters
cluster_summary = data.groupby('cluster').agg(['mean', 'std'])
print("Cluster Summary:\n", cluster_summary)
