from api import APIClient
from file_manager import FolderManager
from config import DEFAULT_URL, ROOT_DIR
from models import ImageEmbeddingResult, TextEmbeddingResult
from vectorDB import DB
import torch
import time
class SmartFolder:
    def __init__(self):
        self.api = APIClient(DEFAULT_URL)
        self.folderManager = FolderManager()
        self.db = DB()

    def ImageEmbedding(self, scan:bool = False, rootdir:str=ROOT_DIR):
        
        upload_files, file_maps = self.folderManager.scan_directory(rootdir) if scan else self.folderManager.select_files()
        
        st = time.perf_counter()
        check = self.db.checkExists([f.filename for f in upload_files])
        imageToBeSent = []
        for im in upload_files:
            if im.filename not in check:
                imageToBeSent.append(im)
        
        response = self.api.image_embeddings(imageToBeSent)

        print(time.perf_counter()-st)
        if(not response):
            return None
        return [ImageEmbeddingResult(f, torch.tensor(response["Image_embedding"][f], dtype=torch.float32), file_maps[f]) for f in response["Image_embedding"].keys()]

    def TextEmbedding(self, text:list[str]):

        response = self.api.text_embeddings(text)
        
        if(not response):
            return None
        return [TextEmbeddingResult(t, torch.tensor(response["Text_embedding"][t], dtype=torch.float32)) for t in text]
    
    def saveImageEmbedding(self,  embeddings: list[ImageEmbeddingResult]):
        self.db.add(embeddings)


    def findImageFromText(self, text_embeddings: list[TextEmbeddingResult]=None):
        if text_embeddings:
            result = self.db.query(text_embeddings=text_embeddings, resultCount = 1)
        else:
            result = self.db.query(text_embeddings=self.TextEmbedding(["A group of men"]), resultCount=1)

        print(result["ids"])
        print(result["metadatas"])
        #self.folderManager.displayImage(result["metadatas"][0][0]['path'])
    
    """def _del(self):
        self.db.deleteCollection("images")
    def _create(self):
        self.db.createCollection("images")"""
    def main(self):
        image_embeddings = self.ImageEmbedding()
        if(image_embeddings):
            self.saveImageEmbedding(image_embeddings)
            self.findImageFromText()

        image_embeddings = self.ImageEmbedding(scan=True)
        if(image_embeddings):
            self.saveImageEmbedding(image_embeddings)
            self.findImageFromText()



Smart = SmartFolder()
Smart.main()