import pandas as pd
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

