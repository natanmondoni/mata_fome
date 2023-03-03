# Libraries import pandas as pd
import numpy as np
import locale
import inflection
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go



from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
## 1.  Funções Auxiliares

st.set_page_config(
    page_title='Visão Culinária 🍽 ',
    page_icon='🍽',
    layout='wide')





def plotly_price_two_people(df1):
    
            
        
    df_aux = (df1[['cuisines','country','restaurant_name','currency','average_cost_for_two']]
              .groupby(['cuisines','restaurant_name','country','currency'])
              .mean()
              .sort_values('average_cost_for_two',ascending=False)
              .reset_index())
    return df_aux



def plotly_restaurantes_italianos(df1,top_restaurant):
        
    cols = ['aggregate_rating','restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines','currency', 'average_cost_for_two', 'votes']


    df_aux = (df1.loc[df1['cuisines'] == 'Italian'][cols]
             .groupby(['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'currency','average_cost_for_two', 'votes'])
             .mean()
             .sort_values(['aggregate_rating','votes'], ascending=[False,True])
             .reset_index()
             .head(top_restaurant))
    
    
    fig = px.bar(df_aux.head(top_restaurant),
                 x='restaurant_name',
                 y='aggregate_rating',
                 text_auto='.2f',
                 labels={ "restaurant_name": "Nome do Restaurante","aggregate_rating": "Nota Média Do Restaurante"})
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    return fig




def plotly_tabela(df1):
    df_aux = (df1[['restaurant_name','country','city','cuisines','currency','average_cost_for_two','votes','aggregate_rating']]
              .sort_values(['aggregate_rating', 'votes'],ascending = [False,False])
              .copy()
              .head(top_restaurant)
              .reset_index(drop=True))

    return df_aux



# Função coloca o nome dos países com base no código de cada país
COUNTRIES = {
   1: "India",
   14: "Australia",
   30: "Brazil",
   37: "Canada",
   94: "Indonesia",
   148: "New Zeland",
   162: "Philippines",
   166: "Qatar",
   184: "Singapure",
   189: "South Africa",
   191: "Sri Lanka",
   208: "Turkey",
   214: "United Arab Emirates",
   215: "England",
   216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]
#---------------------------------------------------------


# Função cria os nomes das cores com base nos códicos
COLORS = {
   "3F7E00": "darkgreen",
   "5BA829": "green",
   "9ACD32": "lightgreen",
   "CDD614": "orange",
   "FFBA00": "red",
   "CBCBC8": "darkred",
   "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]
#---------------------------------------------------------

#
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
#---------------------------------------------------------

def rename_columns(dataframe):
    df = dataframe.copy()

    title = lambda x: inflection.titleize(x)

    snakecase = lambda x: inflection.underscore(x)

    spaces = lambda x: x.replace(" ", "")

    cols_old = list(df.columns)

    cols_old = list(map(title, cols_old))

    cols_old = list(map(spaces, cols_old))

    cols_new = list(map(snakecase, cols_old))

    df.columns = cols_new

    return df



def data_process(df):
    
    
    df = df.dropna()
    
    df = rename_columns(df)
    
    df = df.drop_duplicates()
    
    df["country"] = df.loc[:, "country_code"].apply(lambda x: country_name(x))
    
    
    df["price_type"] = df.loc[:, "price_range"].apply(lambda x: create_price_type(x))

    df["color_name"] = df.loc[:, "rating_color"].apply(lambda x: color_name(x))
                                                    
    df["cuisines"] = df.loc[:,'cuisines'].apply(lambda x: x.split(",")[0])
    
    
    return df
              
#---------------------------------------------------------

def get_num(df):
    return df.select_dtypes(include=['int64', 'float64'])

#---------------------------------------------------------


# Import Dataset
data = pd.read_csv('datasets/zomato.csv')

df1 = data_process(data)


#=======================================
# BARRA LATERAL NO STREAMLIT
#=======================================


image_path = open('logomata.png','rb')

image = image_path.read()

st.sidebar.image(image)


st.sidebar.markdown("""___""")


st.sidebar.markdown(' ## Filtros')

country_options = st.sidebar.multiselect(label = 'Selecione os paises que deseja visualizar (E as cidades do país que selecionar serão exibidas )',
               options=df1.loc[:,'country'].unique().tolist(),
               default=["Brazil"])
st.sidebar.markdown("""___""")

#===============================================================================================

top_restaurant = st.sidebar.slider( "Selecione a quantidade de restaurantes que deseja visualizar ",0,1,20)
#===============================================================================================

cuisines_options = st.sidebar.multiselect(label = 'Selecione os tipos de culinárias que deseja visualizar ',
                       options = df1.loc[:,'cuisines'].unique().tolist(),
                       default=['Italian', 'Japanese'])
st.sidebar.markdown("""___""")

#===============================================================================================




# Ligando os filtros aos dados 

# Filtro do País
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]



# Filtro Tipos de Culinarias

linhas_selecionadas = df1['cuisines'].isin(cuisines_options)

df1 = df1.loc[linhas_selecionadas,:]

#--------------------------------------------------------------

#--------------------------------------------------------------


#=======================================
# LAYOUT LATERAL NO STREAMLIT
#=======================================

st.title(' Visão Culinária 🍽️')

st.markdown('## 📍 Mata Sua Procura De Comida Aqui')


with st.container():
    st.title(f'Top {top_restaurant} Restaurantes Com Base Nas Avaliações')

    df_aux = plotly_tabela(df1)
    
    st.dataframe(df_aux, use_container_width=True)
    

    
    

    


with st.container():
    st.title(f'Top {top_restaurant} Melhores Restaurantes Do tipo Italiano')
    
    fig = plotly_restaurantes_italianos(df1,top_restaurant)
    st.plotly_chart(fig,use_container_width=True)
    
    
    
                 

with st.container():
    
    col1,col2 = st.columns(2)
    

    with col1:
        col1.title(' Maior Valor De Prato Para Duas Pessoas')
        df_aux = plotly_price_two_people(df1)
        
        col1.dataframe(df_aux,use_container_width=True)
        
        
        
    with col2:
        col2.title('Restaurantes Que Aceitam Pedidos On e Fazem Entregas')
        
        df_aux = df1.loc[(df1['has_online_delivery'] ==1) | (df1['is_delivering_now'] == 1)]
        
        
        col2.dataframe(df_aux)
        
        
        
        
        
        