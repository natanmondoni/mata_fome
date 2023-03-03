import streamlit as st

from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='🍽',
    layout="wide")


image_path = ('logomata.png')
image = Image.open( image_path)

st.sidebar.image(image, width=300)
                   
               
st.markdown(
    """
    # Mata Fome 🍽📲
    
    A empresa Mata Fome é uma marketplace de restaurantes.
    Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes.
    Os restaurantes fazem o cadastro dentro da plataforma da Mata Fome, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.
    
    ### Como Utilizar esse Growth Dashboard?
    
    - Visão Geral:
    
      - Métricas Gerais de comportamento. Números de restaurantes cadastrados, cidades, países, insighst de geolocalização.
    
    - Visão País:
      
      -  Indicadores de restaurantes cadastrados por país.
      -  Indicadores de cidades cadastradas.
      -  Média de preço.
      -  Quantidade de restaurantes cadastrados, com o nível de preço alto por país. 
      
    - Visão Cidade:
      
      - Quantidade de Restaurantes por cidade.
      - Indicadores de melhor culinária.
      - Indicadores de restaurantes que fazem reservas, pedidos online, entregas.
      
    - Visão Culinária:
    
      - Indicadores de avaliação.
      - Indicadores de restaurantes Italianos.
      
      
    ### Ask for Help
    
    - https://www.linkedin.com/in/natã-ferreira-lima-13300193/
    


""")