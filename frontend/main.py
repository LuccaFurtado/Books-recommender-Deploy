import streamlit as st
import pandas as pd
import json
import requests
from PIL import Image
st.title('Books Recommender System')


a= list(pd.read_csv("data/filtered.csv")["Book-Title"].unique())

option = st.selectbox(
    'Book to recommend',
    (a)
)


if st.button('Get Recomendations'):
    if option is not None:
        st.write('Recomendations:')
        option = json.dumps({"name": option ,
                             "n":5})
#        st.write(option)
        res = requests.post(f"http://backend:8080/recomend_item", data= option)
#        img_path = res.content
#        st.write(img_path)
#        image = Image.open(img_path)
#        st.image(image, width=500)

        img_path = res.json()
        image = Image.open(img_path.get("filename"))
        st.image(image)
