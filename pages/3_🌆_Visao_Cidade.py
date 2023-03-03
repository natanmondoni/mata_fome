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
    page_title='Visão Cidade 🌆 ',
    page_icon='🍽',
    layout='wide')




def plotly_reserva(df1, col):
    ### 6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
        

    df_aux = (df1.loc[df1[col] == 1 , ['city', 'restaurant_name','restaurant_id']]
              .groupby(['restaurant_name','city'])
              .count()
              .sort_values('restaurant_id', ascending=False)
              .reset_index().head(10))
        
        
    fig4 = px.bar(df_aux,
                 x='city',
                 y='restaurant_id',
                 color='restaurant_name',
                     
                 text_auto='.s',
                 labels = {'city':'Cidades','restaurant_id':'Quantidade De Restaurantes'})
    fig4.update_traces(textfont_size=12,textangle=0,textposition='outside',cliponaxis=False)
        
    return fig4





def table_price(df1):
    df_aux = (df1[['city','average_cost_for_two']]
              .groupby('city')
              .mean()
              .sort_values('average_cost_for_two', ascending=False)
              .reset_index())

    return df_aux



def plotly_nota_4(df1):
    df_aux = (df1.loc[df1['aggregate_rating'] >=4,['city','country','aggregate_rating']]
              .groupby(['city','country'])
              .count()
              .sort_values('aggregate_rating', ascending=False)
              .reset_index().head(10))
        
    fig3 = px.bar(df_aux,
                 x='city',
                 y='aggregate_rating',
                 text_auto='.2s',
                 color='city',
                 width=300,
                 height=500,
                labels = {'city': 'Cidades', 'aggregate_rating':'Quantidade Restaurantes'})
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig3.update_layout(title_text='Top 10 De Cidades Com Nota 4',title_font_size=20)
        
    return fig3




def plotly_culinaria(df1):
    #5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
        
    df_aux = (df1[['city', 'cuisines']]
              .groupby('city')
              .nunique()
              .sort_values('cuisines',ascending=False) 
              .reset_index().head(10))
    fig2 = px.bar(df_aux,
                 x='city',
                 y='cuisines',
                 color='city',
                 text_auto='.2s',
                 width=300,
                 height=500,
                 labels = {'city': 'Cidades', 'cuisines':'Nomes dos Restaurantes'}) 
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig2.update_layout(title_text="Top 10 De Cidades Com Culinária Distinta",title_font_size=20)
    
    return fig2



def plotly_restaurante_for_city(df1):
            
        
            #1. Qual o nome da cidade que possui mais restaurantes registrados?
        
            df_aux = (df1[['city','restaurant_id','country']]
                      .groupby(['city','country'])
                      .count()
                      .sort_values(['restaurant_id','city'], ascending=[False,True])
                      .reset_index().head(10))
        
            fig1 = px.bar(df_aux, x='city',y='restaurant_id',
                         text_auto='.2s',
                         color='country',
                         labels = {'city': 'Cidades','restaurant_name':'Nomes dos Restaurantes'},
                         width=300,
                         height=500)
        
            fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
       
        
            fig1.update_layout(title_text="Top 10 Quantidade De Restaurante Por Cidade",title_font_size=19)
            
            return fig1


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

country_options = st.sidebar.multiselect(label = 'Selecione os Paises Que Deseja Visualizar (E as cidades do País que selecionar serão exibidas )',
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

st.title(' Visão Cidade 🏙️')

st.markdown('## 📍 Mata Sua Procura De Comida Aqui')

with st.container():
    
    col1,col2,col3 = st.columns(3,gap="small")

    with col1:
        
        fig1 = plotly_restaurante_for_city(df1)
        
        col1.plotly_chart(fig1,use_container_width=True)
        
        
        
        

        
    with col2:
        fig2 = plotly_culinaria(df1)
        
        col2.plotly_chart(fig2,use_container_width=True)
                     
        
        
        
        
    with col3:
        fig3 = plotly_nota_4(df1)
        col3.plotly_chart(fig3)
        
        
        
        


with st.container():
    st.title(' Cidades Com a Média De Pratos Para Duas Pessoas')
    
    df_aux = table_price(df1)
        
    st.dataframe(df_aux,use_container_width=True)
        
        
        
        
        
with st.container():
    st.title('Quantidade De Restaurantes Que Fazem Reservas')
    fig4 = plotly_reserva(df1 , col='has_table_booking')
        
    st.plotly_chart(fig4,use_container_width=True)
      
    
        
        
with st.container():
    st.title('Quantidade De Restaurantes Que Fazem Entregas')
        
    fig4 = plotly_reserva(df1 , col='is_delivering_now')
        
    st.plotly_chart(fig4,use_container_width=True)
        
        

   

    
with st.container():
    st.title('Quantidade De Restaurantes Que Fazem Pedidos Online')
    
    fig4 = plotly_reserva(df1 , col='has_online_delivery')


    st.plotly_chart(fig4,use_container_width=True) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
   
    
        

    






























