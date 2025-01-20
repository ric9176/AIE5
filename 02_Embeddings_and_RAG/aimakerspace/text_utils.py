import os
from typing import List

import pymupdf 

class DocumentLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path):
            if self.path.endswith((".pdf", ".txt")):
                self.load_file()
            else:
                raise ValueError("File must be either .pdf or .txt")
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a supported file."
            )

    def load_file(self):
        if self.path.endswith(".pdf"):
            doc = pymupdf.open(self.path)
            text = ""
            for page in doc:
                text += page.get_text()
            self.documents.append(text)
            doc.close()
        else:  # .txt file
            with open(self.path, "r", encoding=self.encoding) as f:
                self.documents.append(f.read())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith((".pdf", ".txt")):
                    file_path = os.path.join(root, file)
                    if file.endswith(".pdf"):
                        doc = pymupdf.open(file_path)
                        text = ""
                        for page in doc:
                            text += page.get_text()
                        self.documents.append(text)
                        doc.close()
                    else:  # .txt file
                        with open(file_path, "r", encoding=self.encoding) as f:
                            self.documents.append(f.read())

    def load_documents(self):
        self.load()
        return self.documents


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i:i + self.chunk_size]
            chunks.append(chunk)
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


if __name__ == "__main__":
    loader = DocumentLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])

