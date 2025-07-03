import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
import hdbscan
import joblib
import os

class BehaviorFingerprinter:
    def __init__(self, method='DBSCAN'):
        self.method = method
        self.scaler = StandardScaler()
        self.model = None
        self.vectors = []

    def fit(self, X):
        """Fit clustering model on initial known good behavior"""
        X_scaled = self.scaler.fit_transform(X)

        if self.method == 'DBSCAN':
            self.model = DBSCAN(eps=0.5, min_samples=5).fit(X_scaled)
        elif self.method == 'HDBSCAN':
            self.model = hdbscan.HDBSCAN(min_cluster_size=5).fit(X_scaled)
        else:
            raise ValueError("Invalid method")

        self.vectors = X_scaled

    def predict(self, x):
        """Predict if incoming vector is in-cluster or anomalous"""
        x_scaled = self.scaler.transform([x])

        if self.method == 'DBSCAN':
            cluster = self.model.fit_predict(np.vstack([self.vectors, x_scaled]))
            label = cluster[-1]
            return label == -1 
        elif self.method == 'HDBSCAN':
            label, _ = self.model.approximate_predict(x_scaled)
            return label[0] == -1
        else:
            return True 

    def save(self, path='models/cluster_model.pkl'):
        joblib.dump((self.model, self.scaler, self.vectors), path)

    def load(self, path='models/cluster_model.pkl'):
        if os.path.exists(path):
            self.model, self.scaler, self.vectors = joblib.load(path)
