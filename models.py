from dataclasses import dataclass
from datetime import date
import torch
@dataclass(slots=True)
class ImageFile:
    filename:str
    path:str
    content:bytes
    mime_type:str

@dataclass(slots=True)
class ImageEmbeddingResult:
    name:str
    embedding:torch.Tensor
    path:str
    date_modified:date=None

@dataclass(slots=True)
class TextEmbeddingResult:
    text:str
    embedding:torch.Tensor


