class pluster:
    def __init__(self):
        import numpy as np
        import pandas as pd
     #   self.name = name
     #   self.age = age
    
    def clusterting_feature_importance (df, cluster_col):
        """
        get the dataframe with the cluster column, and check, per cluster the minimal STD per column range
        those are the best features

        """
        scores = pd.DataFrame()
        df0 = df.copy()
        df0 = df.select_dtypes(include=np.number)

        for i in df0[cluster_col].unique():
            df2 = df0[df0[cluster_col] == i]
            df2.drop(cluster_col,axis=1, inplace=True)
            #df2 = df.select_dtypes(include=np.number)
            scores[i] = df2.std() / (df2.max() - df2.min())
        scores['mean'] = scores.mean(axis = 1)

        scores = 1 - scores

        return scores
    
    def x_elbow(grpx,range0=range(2,10),init='k-means++',n_init=20, random_state=random_state,max_iter=400):
        distortions = []
        silhuettes = []

        for k in range0:
            x_cluster = KMeans(n_clusters=k,init=init, n_init=n_init, random_state=random_state,max_iter=max_iter)
            x_cluster.fit(grpx)
            distortions.append(x_cluster.inertia_)
            silhuettes.append(silhouette_score(grpx, x_cluster.labels_, metric='euclidean'))

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('k')
        ax1.set_ylabel('Distortion', color=color)
        ax1.plot(range0, distortions, 'bx-')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('silhuette score', color=color)  # we already handled the x-label with ax1
        ax2.plot(range0, silhuettes, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        return distortions, silhuettes
