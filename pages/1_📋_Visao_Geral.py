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

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster



st.set_page_config(
    page_title='Visão Geral 📋',
    page_icon='🍽',
    layout='wide')
## 1.  Funções Auxiliares 


# Função da criação do mapa. 




def criando_map(df1):
    
    """
    Esta funcao tem a responsabilidade criar um mapa
    
        
    1. Chamo a funcao para criar o mapa.
    2. Guardos osvalores das variaveis em outras variavels
    3. Faço a criaçao do popup.
    4. Adiciono o mapa com o popup
    
    Input: DataFrame
    Output: Mapa 


    """
    
    
    
    
    mapa = folium.Map(max_bounds=True)

    marker_cluster = MarkerCluster().add_to(mapa)


    for index, location_info in df1.iterrows():
        name = location_info["restaurant_name"]
        city = location_info["city"]
        price_for_two = location_info["average_cost_for_two"]
        currency = location_info["currency"]
        cuisines = location_info["cuisines"]
        rating = location_info["aggregate_rating"]
        
        
        html = "<p><strong>{}</strong></p>"
        html += "<p>City:{}"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, city, price_for_two, currency, cuisines, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker([location_info['latitude'], 
                       location_info['longitude']],
                       popup=popup).add_to(marker_cluster)
        
    return mapa



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
    """
    Esta funcao tem a responsabilidade de Renomiar
    
    Tipos de Rename:
    
    1. Modifica os nomes das colunas para (underscored_string).
    2. Modifica as palavras maiúsculas em minúsculas colocando _ entre elas.
    3. Modifica os espaços deixando o valor da variável juntos.
    4. lista todas as colunas do DataFrame e guarda na variável.
    5. Usando a funcao map pego a variavel title e comparo com a variavel cols_old, fazendo as modificacoes
    6. Faço o mesmo processo usando o map para a variavel spaces, tiro todos os espaços da variavel cols_old.
    7. Faço o mesmo processo usando o map para a variavel snakecase, transformo os valores da varivels cols_old em snakecase.
    8. Por ultimo guardo os valores como columns no DataFrame.
    
    Input: DataFrame
    Output: DataFrame Limpo 


    """
    
    
    
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
    
    """
    Esta funcao tem a responsabilidade Limpar e Modificar.
    
    1. Primeiro removo os valores NaNs.
    2. Chamo a Função para motificar minhas colunas no DataFrame.
    3. Apago os valores duplicados.
    4. Uso a Função country_name para motificar minha coluna.
    5. Uso a Função create_price_type para motificar minha coluna.
    6. Uso a Função color_name para motificar minha coluna.
    7. Removo os valores que tem virgula e assumo o primeiro valor da linha.
    
    Input: DataFrame
    Output: DataFrame Limpo
    

    """
   
    
    
    df = df.dropna()
    
    df = rename_columns(df)
    
    df = df.drop_duplicates()
    
    df["country"] = df.loc[:, "country_code"].apply(lambda x: country_name(x))
    
    
    df["price_type"] = df.loc[:, "price_range"].apply(lambda x: create_price_type(x))

    df["color_name"] = df.loc[:, "rating_color"].apply(lambda x: color_name(x))
                                                    
    df["cuisines"] = df.loc[:,'cuisines'].apply(lambda x: x.split(",")[0])
    
    
    return df


#---------------------------------------------------------

#---------------------- Inicio da Estrutura Lógica do Código---------------------------------




#----------------
#Import Dataset
#----------------
data = pd.read_csv('datasets/zomato.csv')

df1 = data_process(data)


data_metric = df1.copy()

#=======================================
# BARRA LATERAL NO STREAMLIT
#=======================================


image_path = open('logomata.png','rb')

image = image_path.read()

st.sidebar.image(image)


st.sidebar.markdown("""___""")

#===============================================================================================

st.sidebar.markdown(' ## Filtros')

country_options = st.sidebar.multiselect(label = 'Selecione os Paises Que Deseja Visualizar ',
               options=df1.loc[:,'country'].unique().tolist(),
               default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"])
st.sidebar.markdown("""___""")
#===============================================================================================



# Ligando o filtro aos dados 

# Filtro do País
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]
#--------------------------------------------------------------



#=======================================
#  Layout NO STREAMLIT
#=======================================
st.title(' Visão Geral - Mata Fome')


st.title(""" Informações Dos Restaurantes Cadastrados no APP""")


col1,col2,col3,col4,col5 = st.columns(5,gap="large")
    
    
with col1:
    #1. Quantos restaurantes únicos estão registrados?
    
    
  
    rest_unicos = data_metric.loc[:,'restaurant_id'].nunique()
    col1.metric('Restaurantes acessíveis', rest_unicos)
    

    

with col2:
        #2. Quantos países únicos estão registrados?
        países_uni = data_metric.loc[:,'country'].nunique()
        col2.metric('Países Únicos',países_uni)


with col3:
    # 3. Quantas cidades únicas estão registradas?

    city_uni = data_metric.loc[:,'city'].nunique()
    col3.metric('Cidades Únicas',city_uni)


    
with col4:
    ### 4. Qual o total de avaliações feitas?
    avali_rest = data_metric.loc[:,'votes'].sum()
    col4.metric('Total Avaliação',avali_rest)


    
with col5:
    ### 5. Qual o total de tipos de culinária registrados?

    type_culi = data_metric.loc[:,'cuisines'].nunique()
    col5.metric('Tipos de Culinárias',type_culi)


    
mapa = criando_map(df1)
    
folium_static(mapa, width=1024, height= 800)