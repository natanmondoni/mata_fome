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
    page_title='Visão País 🌎',
    page_icon='🍽',
    layout='wide')



def table_price(df1):
    df_aux=(df1[['average_cost_for_two','country','currency']]
            .groupby(['country','currency'])
            .mean()
            .sort_values('average_cost_for_two', ascending=False)
            .reset_index())
        
        
        
        
    fig = ff.create_table(df_aux)    
    
    fig.update_layout(
        margin = {'t':0, 'b':0},
        xaxis = {'domain': [0, 0]},
        xaxis2 = {'domain': [1, 1]},
        yaxis2 = {'anchor': 'x2', 'title': 'Goals'},
        width=1500)
        
    return fig




def plotly_culinaria(df1):
    df_aux =(df1[['cuisines','country']]
             .groupby('country')
             .nunique()
             .sort_values('cuisines', ascending=False) 
             .reset_index())

    fig = px.bar(df_aux, x='country',y='cuisines',
                 text_auto='.2s',
                 labels = {'country': 'Países', 'cuisines':'Quantidade De Culinárias Por Países'},height= 600)
        
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
       
        
    fig.update_layout(title_text="Quantidade De Culinárias Por Países",title_font_size=28)
           
            
    return fig









def plotly_nivel_high(df1):
    #3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?

    df_aux =(df1.loc[df1['price_range' ] >= 4, ['restaurant_id','country']]
             .groupby('country')
             .count()
             .sort_values('restaurant_id', ascending=False)
             .reset_index())


    fig = px.bar(df_aux, x='country' , y='restaurant_id',text_auto=True,labels = {'country': 'Países', 'restaurant_id':'Quantidade de Restaurantes'},height= 600) 
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(title_text="Restaurantes Com o Nível de Preço Alto",title_font_size=28)        
            
    return fig
        

def plotly_quantidade(df1):
        df_aux = df1[['country','city']].groupby('country').nunique().sort_values('city',ascending=False).reset_index()
        



        fig = px.bar(df_aux, x='country', y='city',facet_col_wrap =200,color='city',text_auto='.2s',labels = {'country': 'Países', 'city':'Quantidade de cidades'},height= 600)
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(title_text="Quantidade De Cidades Por País",
                          title_font_size=28)
        
        return fig
    



def plotly_restaurantes_por_pais(df1):

        df_aux = df1[['country','restaurant_id']].groupby('country').count().sort_values('restaurant_id', ascending=False).reset_index()


        fig = px.bar(df_aux,x='country',y='restaurant_id',text_auto='.2s',labels = {'country': 'Países', 'restaurant_name':'Quantidade de Restaurantes'},height= 600)
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(title_text="Quantidade De Restaurantes Por País",title_font_size=28)
        
        return fig
    




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

def get_attributes(num_attributes):
    num_attributes = df.select_dtypes(include=['int64', 'float64'])

    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    metricas = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()

    metricas.columns = ['ATTRIBUTES', 'MAX', 'MIN', 'MEAN', 'MEDIAN', 'STD']

    metricas
    
    return metricas


# Import Dataset
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


st.sidebar.markdown(' ## Filtros')

country_options = st.sidebar.multiselect(label = 'Selecione os Paises Que Deseja Visualizar ',
               options=df1.loc[:,'country'].unique().tolist(),
               default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"])
st.sidebar.markdown("""___""")
#===============================================================================================


# Ligando os filtros aos dados 

# Filtro do País
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]

#--------------------------------------------------------------





#=======================================
# LAYOUT LATERAL NO STREAMLIT
#=======================================

st.title(' Visão País 🌍')

 
    
with st.container():
         
    fig = plotly_quantidade(df1)
    st.plotly_chart(fig)
    
    fig =plotly_restaurantes_por_pais(df1)
    
    st.plotly_chart(fig)
   
        
with st.container():
    col1,col2 = st.columns(2)
    
    
    with col1:
        fig = plotly_nivel_high(df1)
        col1.plotly_chart(fig,use_container_width=True)
        
      

    
    with col2:
        fig = plotly_culinaria(df1)
        col2.plotly_chart(fig,use_container_width=True)
        
        
       




    
with st.container():
    st.title(' Média De Preço De Um Prato Para 2 Pessoas Por País')
    
    fig = table_price(df1)
    st.plotly_chart(fig)   

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
   





