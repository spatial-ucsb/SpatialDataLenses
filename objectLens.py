import pandas as pd
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


##############################################################################
# Gather data

df = pd.read_csv("vacantBuildings.csv")
df.head()
coordinates = df.as_matrix(columns=['Lon', 'Lat'])
valueLookup = df.as_matrix(columns=['Lon', 'neighborhood'])

# make dictionary of neighborhoods
neighborhoods = {}

for neighborhood in df['neighborhood']:
    if neighborhood not in neighborhoods:
        neighborhoods[neighborhood] = 0

print len(neighborhoods)
# for i in len(df):
#     print(df[i].councilDistrict)

##############################################################################
# Compute DBSCAN
db = DBSCAN(eps=.0005, min_samples=5).fit(coordinates)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated total number of clusters: %d' % n_clusters_)
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#       % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#       % metrics.adjusted_mutual_info_score(labels_true, labels))
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, labels))

##############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1.5, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = coordinates[class_member_mask & core_samples_mask]
    clusters = plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=8)

    xy = coordinates[class_member_mask & ~core_samples_mask]
    singles = plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=3)

plt.grid(b=True, which='both', color='k', linestyle='-', linewidth=0.3)
plt.title('Vacancy Clusters in Baltimore City')
plt.suptitle('Estimated number of clusters: %d' % n_clusters_)
plt.xlabel("Decimal Degrees [longitude]")
plt.ylabel("Decimal Degrees [latitude]")

plt.show()
