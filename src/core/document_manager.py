from langchain_core.documents import Document
import json

class DocumentManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_documents(self):
        documents = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:   
                chunk = json.loads(line)

                document = Document(
                    page_content=chunk['content'],
                    metadata = {
                        'chunk_id': chunk['chunk_id'],
                        **chunk['metadata']
                    }
                )
                documents.append(document)
        print(f' Loaded {len(documents)} documents successfully')

        return documents