import logging
import os
 
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
 
logger = logging.getLogger(__name__)
 
DEFAULT_CLUSTER_NAMES = {
    0: "Tech-Accessories & Everyday Electronics",
    1: "Entertainment Tablets & Media Devices",
    2: "Smart Home & Audio Systems",
    3: "Non-Electronics (Office & Pets)",
    4: "E-Readers & E-Books",
}
 
 
class ProductClusterer:
 
    def __init__(
        self,
        n_clusters=5,
        model_path="models/all-MiniLM-L6-v2",
        embeddings_cache_path="cache/product_embeddings.npy",
        cluster_name_mapping=None,
        random_state=42,
    ):
        self.n_clusters = n_clusters
        self.model_path = model_path
        self.embeddings_cache_path = embeddings_cache_path
        self.cluster_name_mapping = cluster_name_mapping or DEFAULT_CLUSTER_NAMES
        self.random_state = random_state
 
        self.model = None
        self.df_clean = None
        self.unique_products = None
        self.embeddings = None
 
    def load_data(self, csv_path):
        logger.info("Load raw data from %s", csv_path)
        df = pd.read_csv(csv_path)
        self.df_clean = df.dropna(subset=["name"]).copy()
        return self.df_clean
 
    def build_product_profiles(self):
        self.df_clean["product_profile"] = (
            self.df_clean["name"].fillna("") + " | " + self.df_clean["categories"].fillna("")
        )
        self.unique_products = (
            self.df_clean[["name", "brand", "categories", "product_profile"]]
            .drop_duplicates(subset=["name"])
            .reset_index(drop=True)
        )
        logger.info("Unique products: %d", len(self.unique_products))
        return self.unique_products
 
    def load_embedding_model(self):
        if os.path.exists(self.model_path):
            logger.info("Load embedding model from disk: %s", self.model_path)
            self.model = SentenceTransformer(self.model_path)
        else:
            logger.info("Load embedding model: all-MiniLM-L6-v2")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            self.model.save(self.model_path)
        return self.model
 
    def compute_embeddings(self):
        if os.path.exists(self.embeddings_cache_path):
            logger.info("Load cached embeddings: %s", self.embeddings_cache_path)
            self.embeddings = np.load(self.embeddings_cache_path)
        else:
            logger.info("Calculate embeddings")
            self.embeddings = self.model.encode(
                self.unique_products["product_profile"].tolist(),
                show_progress_bar=True,
            )
            os.makedirs(os.path.dirname(self.embeddings_cache_path), exist_ok=True)
            np.save(self.embeddings_cache_path, self.embeddings)
 
        logger.info("Embedding matrix (products x dimensions): %s", self.embeddings.shape)
        return self.embeddings
 
    def cluster_products(self):
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state, n_init=10)
        self.unique_products["cluster"] = kmeans.fit_predict(self.embeddings)
        logger.info("Finished clustering k=%d", self.n_clusters)
        return self.unique_products
 
    def map_meta_categories(self):
        self.unique_products["meta_category"] = self.unique_products["cluster"].map(
            self.cluster_name_mapping
        )
        return self.unique_products
 
    def merge_meta_categories(self):
        df_final = self.df_clean.merge(
            self.unique_products[["name", "meta_category"]], on="name", how="left"
        )
        return df_final
 
    def export(self, df_final, output_path):
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        df_final.to_csv(output_path, index=False)
        logger.info("Saved result: %s", output_path)
 
    def run(self, input_csv_path, output_csv_path):
        self.load_data(input_csv_path)
        self.build_product_profiles()
        self.load_embedding_model()
        self.compute_embeddings()
        self.cluster_products()
        self.map_meta_categories()
        df_final = self.merge_meta_categories()
        self.export(df_final, output_csv_path)
        return df_final

