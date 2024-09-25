from typing import List
from fastapi import FastAPI, HTTPException
from PIL import Image
import requests
import io
import torch
from transformers import AutoModel
from pydantic import BaseModel, Field

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

def encode_text(sentences: List[str]) -> List[List[float]]:
    return get_model().encode_text(sentences).tolist()

def encode_image(image_urls: List[str]) -> List[List[float]]:
    embeddings = []
    for url in image_urls:
        try:
            if url.startswith('http'):
                response = requests.get(url)
                img = Image.open(io.BytesIO(response.content))
            else:
                img = Image.open(url)
            embeddings.append(get_model().encode_image(img).tolist())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing image {url}: {str(e)}")
    return embeddings

class EmbedRequest(BaseModel):
    text: List[str] = Field(None, description="List of text sentences")
    image: List[str] = Field(None, description="List of image URLs")

@app.post("/embed")
async def embed(request: EmbedRequest):
    if not request.text and not request.image:
        raise HTTPException(status_code=400, detail="Both text and image lists are empty")

    response = {}

    if request.text:
        response["text_embeddings"] = encode_text(request.text)

    if request.image:
        response["image_embeddings"] = encode_image(request.image)

    return response

if __name__ == "__main__":
    import uvicorn
    get_model()
    uvicorn.run(app, host="0.0.0.0", port=7144)