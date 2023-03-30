import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np
import urllib.request
import os
from PIL import Image
from fastapi import FastAPI, Body
from pydantic import BaseModel


app = FastAPI()


class Img(BaseModel):
    image_url: str


class Response(BaseModel):
    dog: float
    cat: float

img_examples = {
    "Example 1": {
        "value": {
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/29/Aesir_amstaffs_2016_blue_puppies.jpg"
        }
    },
    "Example 2": {
        "value": {
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/69/Rottweiler_-52773841920.jpg"
        }
    } ,
    "Example 3": {
        "value": {
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Kot-027.jpg/1280px-Kot-027.jpg"
        }
    }     
}


@app.on_event("startup")
async def startup_event():
    model = torch.load("./models/model.pth")
    model.cpu()
    model.eval()

    preprocessor = transforms.Compose([
        transforms.Resize(200),
        transforms.CenterCrop((200, 200)),
        transforms.ToTensor(),
    ])

    app.package = {
        "model": model,
        "preprocessor": preprocessor
    }


@app.post("/predict/", response_model=Response)
async def predict(image: Img = Body(..., examples=img_examples)):
    """
    Make a prediction on an image from given URL.
    """
    image_url = image.image_url
    image_path = '/tmp/tmp_image.jpg'
    urllib.request.urlretrieve(image_url, image_path)

    model = app.package['model']
    preprocessor = app.package['preprocessor']

    img = Image.open(image_path)
    img = preprocessor(img)
    img = img.cpu()
    
    with torch.no_grad():
        out = model.forward(img.unsqueeze(0))

    out = F.softmax(out, dim=1)
    out = out.data.cpu().numpy()

    return Response(dog=float(out[0, 0]),cat=float(out[0, 1]))
