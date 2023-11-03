import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import seaborn as sns
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# Phân tích chọn điểm lân cận cho DBSCAN
def epsilon_analize(arr):
    # Xây dựng mô hình k-Means với k=10
    neighbors = 20
    nbrs = NearestNeighbors(n_neighbors=neighbors ).fit(arr)

    # Ma trận khoảng cách distances: (N, k)
    distances, indices = nbrs.kneighbors(arr)

    # Lấy ra khoảng cách xa nhất từ phạm vi láng giềng của mỗi điểm và sắp xếp theo thứ tự giảm dần.
    distance_desc = sorted(distances[:, neighbors-1], reverse=True)

    # Vẽ biểu đồ khoảng cách xa nhất ở trên theo thứ tự giảm dần
    plt.figure(figsize=(12, 8))
    plt.plot(list(range(1,len(distance_desc )+1)), distance_desc)
    plt.axhline(y=0.4)
    plt.text(2, 0.4, 'y = 0.4', fontsize=12)
    plt.axhline(y=0.45)
    plt.text(2, 0.45, 'y = 0.45', fontsize=12)
    plt.ylabel('distance')
    plt.xlabel('indice')
    plt.title('Sorting Maximum Distance in k Nearest Neighbor of kNN')


### Lưu ý ###
# arr là tập dữ liệu chuyển từ các term được vector hóa
# term là danh sách các thuật ngữ

def cluster_DBSCAN(arr, terms):
    for thres in np.linspace(0.3, 0.4, 20):

        # setup config cho DBSCAN
        dbscan = DBSCAN(eps=thres, min_samples=5, metric='euclidean')
        # Cluster các điểm dữ liệu
        labels = dbscan.fit_predict(arr)
        unique_list = sorted(list(set(labels)))

        print(f'Epsilon: {thres}')
        for unique in unique_list:
            print(f' Cluster: {unique}')
            for index, value in enumerate(labels):
                if (value == unique):
                    print(f'  {terms[index]}')
        
        print('='*200, '\n')

def cluster_HClust(arr, terms):
    for n_cluster in range(5, 15):
        HClust_model = AgglomerativeClustering(distance_threshold=None, n_clusters=n_cluster, metric='euclidean')
        
        labels = HClust_model.fit_predict(arr)
        unique_list = sorted(list(set(labels)))

        print(f'Number of Cluster: {n_cluster}')
        for unique in unique_list:
            print(f' Cluster: {unique}')
            for index, value in enumerate(labels):
                if (value == unique):
                    print(f'  {terms[index]}')
        
        print('='*200, '\n')


def cluster_Kmean(arr, terms):
    vocab = {term: idx for idx, term in enumerate(terms)}
    vectorizer = TfidfVectorizer(vocabulary = terms, ngram_range=(2, 5))

    true_k = 100
    Kmeans_model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    Kmeans_model.fit(arr)

    print("Top terms per cluster:")
    order_centroids = Kmeans_model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for i in range(true_k):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :]:
            print(' %s' % terms[ind]),
        print()