import chromadb
import numpy

from models import ImageEmbeddingResult, TextEmbeddingResult, ImageFile
class DB:
    def __init__(self):
        self.vectordb = chromadb.Client()
        self.image_collection = self.vectordb.get_or_create_collection(name="images")

    def add(self, embeddings: list[ImageEmbeddingResult]):
        names = []
        embeds = []
        metas: chromadb.Metadatas = []
        for em in embeddings:
            names.append(em.name)
            embeds.append(em.embedding.numpy())
            metas.append({"path": em.path})
        
        self.image_collection.upsert(
            ids=names,
            embeddings=embeds,
            metadatas=metas
        )
    def checkExists(self, images: list[str]):
        result = self.image_collection.get(ids=images, include=['metadatas'])
        return result["ids"]
    def query(self, text_embeddings: list[TextEmbeddingResult], resultCount:int):
        return self.image_collection.query(
            query_embeddings=[t.embedding.numpy() for t in text_embeddings],
            n_results=resultCount,
            include=["embeddings", "metadatas", "distances"]
        )
    def deleteCollection(self, collectionName):
        self.vectordb.delete_collection(collectionName)
    def createCollection(self, collectionName):
        self.image_collection = self.vectordb.get_or_create_collection(name=collectionName)