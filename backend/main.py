from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pandas as pd
from starlette.responses import StreamingResponse
from io import BytesIO
#from utils import  print_covers
import matplotlib.pyplot as plt
import requests
from PIL import Image


def print_covers(df):
    fig, axs = plt.subplots(1 , 5,figsize=(18,5))
    fig.suptitle('Recomendations', size = 22,color="white")
    fig.patch.set_facecolor('#1b1a1a')
    for i in range(len(df)):
        prov = df.iloc[i]
        url = prov["Image-URL-L"]
        im = Image.open(requests.get(url, stream=True).raw)
        im = im.resize((500,450),)
        axs[i].imshow(im,)
        axs[i].axis("off")
        axs[i].set_title(f"{prov['Book-Title'][:18]}",
                    y=-0.18,    
                    color="white",
                    fontsize=18)
    return fig


class Book(BaseModel):
    name:str
    n: int

app = FastAPI()
model = pd.read_pickle('models/cosine_similarity_model.pickle')
books = pd.read_csv("data/BX-Books.csv",sep=';', encoding='cp1252',  on_bad_lines='skip',low_memory=False)[["Book-Title","Image-URL-L","Year-Of-Publication"]]


@app.get('/')
def index():
    return {'message': 'Hello, World'}

@app.post('/recomend_item')
def get_predictions(data:Book):
    data = data.dict()
    n = 5
    name = str(data["name"])
    df = model[name].sort_values(ascending=False)
    df = pd.DataFrame({"Book-Title":(df.head(n+1).index)[1:]})
    df = df.merge(books)
    df["Year-Of-Publication"] = df["Year-Of-Publication"].astype(int)
    df = df.sort_values(by="Year-Of-Publication" ,ascending=False).drop_duplicates(["Book-Title"])
    fig = print_covers(df)
    filename = f"/storage/{name}.png"
    fig.savefig(filename)
    #buf = BytesIO()
    #fig.savefig(buf, format="png")
    #buf.seek(0)
    #return StreamingResponse(buf, media_type="image/png")
    return {"filename":filename}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080)