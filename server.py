from typing import List, Literal, Union
from fastapi import FastAPI, HTTPException
from PIL import Image
import requests
import io
import torch
from transformers import AutoModel
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return AutoModel.from_pretrained('jinaai/jina-clip-v1', trust_remote_code=True).to(device)

model = None

def get_model():
    global model
    if model is None:
        model = load_model()
    return model

def encode_text(sentences: str) -> List[float]:
    return get_model().encode_text(sentences).tolist()

def encode_image(url: str) -> List[float]:
    try:
        if url.startswith('http'):
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
        else:
            img = Image.open(url)
        return get_model().encode_image(img).tolist()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image {url}: {str(e)}")

class EmbedItem(BaseModel):
    type: Literal["text", "image"]
    data: Union[str, HttpUrl]

class EmbedRequest(BaseModel):
    inputs: List[EmbedItem] = Field(..., min_items=1)

@app.post("/embed")
async def embed(request: EmbedRequest):
    embeddings = []

    for item in request.inputs:
        if item.type == 'text':
            embeddings.append(encode_text(item.data))
        elif item.type == 'image':
            embeddings.append(encode_image(item.data))
        else:
            raise HTTPException(status_code=400, detail=f"Invalid type {item.type}")

    return {"embeddings": embeddings}

if __name__ == "__main__":
    import uvicorn
    get_model()
    uvicorn.run(app, host="0.0.0.0", port=7144)