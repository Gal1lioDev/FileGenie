import requests
from models import ImageFile
class APIClient:

    def __init__(self, base_url):

        self.base_url = base_url.rstrip("/")

    def _build_upload(self, header, images: list[ImageFile]):

        return [
            (header, (image.filename, image.content, image.mime_type)) for image in images
        ]
        
    
    
    def post(self, endpoint, **kwargs):

        response = requests.post(
            self.base_url + endpoint,
            **kwargs
        )

        response.raise_for_status()

        return response.json()

    def classify_images(self, upload_files, labels):

        return self.post(
            "/image",
            files=self._build_upload('pics', upload_files),
            data={"labels": labels}
        )

    def image_embeddings(self, imagesData:list[ImageFile]):
        if(len(imagesData)==0):
            return None
        return self.post(
            "/image_embedding",
            files=self._build_upload('pics', imagesData)
        )

    def text_embeddings(self, texts:list[str]):
        if(len(texts)==0):
            return None
        return self.post(
            "/text_embedding",
            data={"text": texts}
        )

    def similarity(self, text_embeddings, image_embeddings):

        return self.post(
            "/similarity",
            json={
                "text_embed": text_embeddings,
                "image_embed": image_embeddings
            }
        )