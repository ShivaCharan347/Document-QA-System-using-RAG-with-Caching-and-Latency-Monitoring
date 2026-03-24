import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ingestion.ingest import IngestionPipeline

if __name__ == "__main__":
    IngestionPipeline().run()
