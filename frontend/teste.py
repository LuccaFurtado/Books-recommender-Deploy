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
        img_path = res.content
#        new_image = img_path.resize((600, 400))
#        st.write(img_path)
        st.image(img_path, width=1000)


