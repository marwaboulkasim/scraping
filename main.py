# main.py

import argparse
from pipelines.pipeline_scraping import run_scraping_pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de scraping de livres")
    parser.add_argument("--pages", type=int, default=1, help="Nombre de pages à scraper")
    args = parser.parse_args()
    run_scraping_pipeline(pages=50)  
