import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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


print("converting categorical data to numerical data")
# Convert categorical data to numerical data
if 'Event_Type' in merged_data.columns:
    merged_data['Event_Type'] = merged_data['Event_Type'].astype('category').cat.codes
if 'Daylight_x' in merged_data.columns:
    merged_data['Daylight_x'] = merged_data['Daylight_x'].astype('category').cat.codes

print("feature engineering")
# Feature engineering
merged_data['Speed_Change'] = merged_data['Speed(ms)'].diff().fillna(0)
merged_data['Acceleration'] = merged_data['Speed_Change'].diff().fillna(0)
merged_data['Distance'] = np.sqrt(merged_data['X'].diff()**2 + merged_data['Y'].diff()**2).fillna(0)
merged_data['Click_Count'] = merged_data['Event_Type'].apply(lambda x: 1 if x == 0 else 0).cumsum()

# Select features for clustering
features = [ 'X', 'Y','Distance', 'Speed_Change','Acceleration']
X = merged_data[features]

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(X_scaled)
clusters = kmeans.predict(X_scaled)

# Add cluster labels to the data
merged_data['Cluster'] = clusters

# Print the first few rows of the data with cluster labels
print(merged_data.head())

# Create a 3D scatter plot using matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Assign colors to clusters
colors = ['r', 'g', 'b', 'y']

# Plot each cluster
for cluster in range(4):
    cluster_data = merged_data[merged_data['Cluster'] == cluster]
    ax.scatter(
        cluster_data['X'],
        cluster_data['Y'],
        cluster_data['Speed(ms)'],
        c=colors[cluster],
        label=f'Cluster {cluster}'
    )

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Speed(ms)')
plt.title('3D Scatter Plot of Clusters')
plt.legend()
plt.show()  

# Show plot
