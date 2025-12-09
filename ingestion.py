import lancedb 
from backend.constans import DATA_PATH, VECTOR_PATH
from backend.data_models import Transcripts
import time

def setup_vector_db(path):
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("youtube", schema=Transcripts, exist_ok=True)
    return vector_db

def ingest_docs_to_vector_db(table):
     for file in DATA_PATH.glob("*.md"):
        with open(file, "r") as f:
            content = f.read()

        doc_id = file.stem
        table.delete(f"doc_id = '{doc_id}'")

        table.add([
             {
                  "doc_id": doc_id,
                  "filepath": str(file),
                  "filename": file.stem,
                  "content": content
             }
        ])

        print(table.to_pandas()["filename"])
        time.sleep(15)

if __name__ == "__main__":
     vector_db = setup_vector_db(VECTOR_PATH)
     ingest_docs_to_vector_db(vector_db["youtube"])
          

