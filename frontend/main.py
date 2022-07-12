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
number = st.slider('How many recomendations do you want?', 0, 20, 5)


if st.button('Get Recomendations'):
    if option is not None:
        st.write('Recomendations:')
        option = json.dumps({"name": option ,
                             "n":number})
        res = requests.post(f"http://backend:8080/recomend_item", data= option)

        img_path = res.json()
        list = img_path.get("list")
        for i,element in enumerate(list):
            st.write(f"{i+1} : {element}")
        image = Image.open(img_path.get("filename"))
        st.image(image)

