import argparse
import logging
 
from clustering_pipeline import DEFAULT_CLUSTER_NAMES, ProductClusterer
 
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
 
 
def parse_args():
    parser = argparse.ArgumentParser(
        description="Clusters Amazon products for meta categories"
    )
    parser.add_argument("--input-csv", default="cleaned_reviews.csv")
    parser.add_argument("--output-csv", default="outputs/reviews_with_meta_categories.csv")
    parser.add_argument("--model-path", default="models/all-MiniLM-L6-v2")
    parser.add_argument("--embeddings-cache", default="cache/product_embeddings.npy")
    parser.add_argument("--n-clusters", type=int, default=5)
    return parser.parse_args()
 
 
def main():
    args = parse_args()
 
    pipeline = ProductClusterer(
        n_clusters=args.n_clusters,
        model_path=args.model_path,
        embeddings_cache_path=args.embeddings_cache,
        cluster_name_mapping=DEFAULT_CLUSTER_NAMES,
    )
 
    df_final = pipeline.run(args.input_csv, args.output_csv)
 
 
if __name__ == "__main__":
    main()