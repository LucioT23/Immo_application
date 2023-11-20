import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
import base64
import warnings
warnings.filterwarnings('ignore')


pd.set_option('display.max_row',111)
pd.set_option('display.max_column',111)

# pour nommer la page
st.set_page_config(page_title="SuperImmo!!!", page_icon=":house:",layout="wide")

st.title(' :house: Immo Data Analyze')
# Pour remonter le titre dans la page
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(" :file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename) #, encoding = "ISO-8859-1")

st.sidebar.header("Choose your filter: ")

# Create for Number of room
nb_rooms = st.sidebar.multiselect("Nombre de chambre", df['Number Room'].unique())
if not nb_rooms:
    df2 = df.copy()
else:
    df2 = df[df['Number Room'].isin(nb_rooms)]

# Create for City
city = st.sidebar.multiselect("Ville", df2["City"].unique())
if not city:
    df3 = df2.copy()
else:
    df3 = df2[df2["City"].isin(city)]

# Create for Type of house
typologie = st.sidebar.multiselect("Type de logement",df3["type_logement"].unique())
if not typologie:
    df4 = df3.copy()
else:
    df4 = df3[df3["type_logement"].isin(typologie)]

# Create for Equipement
# Liste des équipements à filtrer
equipements_a_filtrer = ['piscine', 'jacuzzi', 'acces plage']
selected_equipement = st.sidebar.multiselect("Equipement", equipements_a_filtrer)

if not selected_equipement:
    df5 = df4.copy()
else:
    df5 = df4[df4['Test_Equipment'].apply(lambda x: all(equip in x for equip in selected_equipement))]


with st.expander("Data"):
    #st.write(df5) #.style.background_gradient(cmap="Oranges")
    st.dataframe(df5.style.background_gradient(cmap="Oranges"))



# Filter the data based on Number of room, City and Typologie

if not nb_rooms and not city and not typologie and not selected_equipement:
    filtered_df = df5
elif not nb_rooms and not city and not selected_equipement:
    filtered_df = df5[df5["type_logement"].isin(typologie)]
elif not nb_rooms and not typologie and not selected_equipement:
    filtered_df = df5[df5["City"].isin(city)]
elif not typologie and not city and not selected_equipement:
    filtered_df = df5[df5["Number Room"].isin(nb_rooms)]
elif not typologie and not city and not nb_rooms:
    filtered_df = df5[df5['Test_Equipment'].apply(lambda x: all(equip in x for equip in selected_equipement))]

elif nb_rooms and city:
    filtered_df = df5[df5["Number Room"].isin(nb_rooms) & df5["City"].isin(city)]
elif nb_rooms and typologie:
    filtered_df = df5[df5["Number Room"].isin(nb_rooms) & df5["type_logement"].isin(typologie)]
elif city and typologie:
    filtered_df = df5[df5["City"].isin(city) & df5["type_logement"].isin(typologie)]

elif nb_rooms and city and selected_equipement:
    filtered_df = df5[df5["Number Room"].isin(nb_rooms) & df5["City"].isin(city) & (df5['Test_Equipment'].apply(lambda x: all(equip in x for equip in selected_equipement)))]
elif nb_rooms and typologie and selected_equipement:
    filtered_df = df5[df5["Number Room"].isin(nb_rooms) & df5["type_logement"].isin(typologie) & (df5['Test_Equipment'].apply(lambda x: all(equip in x for equip in selected_equipement)))]
elif city and typologie and selected_equipement:
    filtered_df = df5[df5["City"].isin(city) & df5["type_logement"].isin(typologie) & (df5['Test_Equipment'].apply(lambda x: all(equip in x for equip in selected_equipement)))]

elif city:
    filtered_df = df5[df5["City"].isin(city)]
elif typologie:
    filtered_df = df5[df5["type_logement"].isin(typologie)]
elif nb_rooms:
    filtered_df = df5[df5["Number Room"].isin(nb_rooms)]
elif selected_equipement:
    filtered_df = df5[df5['Test_Equipment'].apply(lambda x: all(equip in x for equip in selected_equipement))]
else:
    filtered_df = df5[df5["Number Room"].isin(nb_rooms) & df5["City"].isin(city) & df5["type_logement"].isin(typologie) & (df5['Test_Equipment'].apply(lambda x: all(equip in x for equip in selected_equipement)))]

col1, col2, col3 = st.columns((3))
with col1:
    st.subheader("Prix par nuit en fonction du nb de chambre")
    #fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
    #             template = "seaborn")

    # Scatter plot des annonces par prix et par nombre de chambres
    fig = px.scatter(filtered_df, x="Number Room", y='euros', template = "seaborn") #,color="piscine")
    fig.update_layout(yaxis_title="Prix € par nuit", xaxis_title = "Nombre de chambres")
    st.plotly_chart(fig,use_container_width=True) #, height = 200)

with col2:
    st.subheader("Prix médian par nuit")
    fig = px.box(filtered_df, x="Number Room", y='euros', template = "seaborn") #template="gridon"
    fig.update_layout(yaxis_title="Prix € par nuit", xaxis_title = "Nombre de chambres")
    st.plotly_chart(fig,use_container_width=True)

with col3:
    st.subheader("Prix moyen par nuit")
    rooms = filtered_df.groupby(by = "Number Room", as_index = False)['euros'].mean()
    fig = px.box(rooms, x="Number Room", y='euros', template = "seaborn") #template = "plotly_dark"
    fig.update_layout(yaxis_title="Prix € par nuit", xaxis_title = "Nombre de chambres")
    st.plotly_chart(fig,use_container_width=True)


st.subheader("Localisation des biens")
fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", color="euros", color_continuous_scale=px.colors.cyclical.IceFire,
                       size_max=15, zoom=11,mapbox_style="carto-positron")
st.plotly_chart(fig,use_container_width=True, height = 500, width = 1000)

col1_repartition, col2_repartition, col3_repartition = st.columns((3))
with col1_repartition:
  st.subheader("Repartition des biens en %")
  rooms = filtered_df.groupby(by = "Number Room", as_index = False)['Title'].count()
  fig = px.pie(rooms, values='Title', names='Number Room')
  st.plotly_chart(fig,use_container_width=True)

with col2_repartition:
  st.subheader("Repartition des biens en Volume")
  rooms = filtered_df.groupby(by = "Number Room", as_index = False)['Title'].count()
  fig = px.bar(rooms, x="Number Room", y='Title')
  fig.update_layout(yaxis_title="Nb de logements", xaxis_title = "Nombre de chambres")
  st.plotly_chart(fig,use_container_width=True)

with col3_repartition:
  st.subheader("Repartition des biens par typologie")
  rooms_typo = filtered_df.groupby(by = ["Number Room",'type_logement'], as_index = False)['Title'].count()
  fig = px.bar(rooms_typo, x="Number Room", y="Title", color="type_logement")
  fig.update_layout(yaxis_title="Nb de logements par typologie", xaxis_title = "Nombre de chambres")
  st.plotly_chart(fig,use_container_width=True)
  

with st.expander("Nombre d'annonces par typologie"):
    rooms = filtered_df.groupby(by = "Number Room", as_index = False)['Title'].count()
    st.write(rooms.style.background_gradient(cmap="Blues"))
    #st.write(rooms) #.style.background_gradient(cmap="Oranges"))
    #csv = region.to_csv(index = False)   #.encode('utf-8')
    # Sauvegardez le DataFrame au format CSV en spécifiant l'encodage
    csv = rooms.to_csv(index=False) #region.to_csv('nom_du_fichier.csv', index=False)
    st.download_button("Download Data", data = csv, mime = "text/csv",
                    help = 'Click here to download the data as a CSV file') #, file_name = "Bien par chambre.csv"

# Create a treemap based on Region, category, sub-Category
st.subheader("Jours réservés")
st.write(f"La période de réservation est : {filtered_df['periode reservation'].iloc[0]}")

reservation_rooms = filtered_df.groupby(by = ["Number Room", 'Number annonce'], as_index = False)['jours reserves'].agg({'Nombre reservation': 'count', 'Total jours réservés': 'sum'})
# Modifie la colonne 'Nombre reservation' en fonction de la valeur de 'Total jours réservés'
reservation_rooms['Nombre reservation'] = reservation_rooms.apply(lambda row: 0 if row['Total jours réservés'] == 0 else row['Nombre reservation'], axis=1)
result_by_room = reservation_rooms.groupby('Number Room', as_index=False).agg({'Nombre reservation': 'sum','Total jours réservés': 'sum'})
result_by_room['Moyenne jours réservés par reservation'] = result_by_room['Total jours réservés'] / result_by_room['Nombre reservation']

col1_reservation, col2_reservation, col3_reservation = st.columns((3))
with col1_reservation:
  st.subheader("Nombre des biens réservés sur cette période")
  reservation_rooms_count = filtered_df.groupby(by = "Number Room", as_index = False)['jours reserves']
  fig3 = px.bar(reservation_rooms_count, x="Number Room", y='jours reserves', template = "seaborn")
  fig3.update_layout(yaxis_title="Nombre de biens réservés", xaxis_title = "Nombre de chambres")
  st.plotly_chart(fig3,use_container_width=True)

with col2_reservation:
  st.subheader("Nombre des biens réservés sur cette période")
  fig = px.bar(reservation_rooms, x="Number Room", y='Total jours réservés', template = "seaborn")
  fig.update_layout(yaxis_title="Nombre de jours réservés", xaxis_title = "Nombre de chambres")
  st.plotly_chart(fig,use_container_width=True)

with col3_reservation:
  st.subheader("Moyenne de nuits réservés par typologie")
  fig = px.bar(result_by_room, x="Number Room", y='Moyenne jours réservés par reservation')
  fig.update_layout(yaxis_title="Moyenne de jours réservés", xaxis_title = "Nombre de chambres")
  st.plotly_chart(fig,use_container_width=True)

# Filtrer les lignes avec des valeurs non nulles dans les colonnes pertinentes
df_filtered = filtered_df.dropna(subset=["City", "Number Room", "type_logement", "jours reserves"])
fig4 = px.treemap(df_filtered, path=["City", "Number Room", "type_logement"], values="jours reserves")
fig4.update_layout(width=800, height=650)
st.plotly_chart(fig4, use_container_width=True)

with st.expander("Nombre de réservations par typologie"):
    st.write(reservation_rooms.style.background_gradient(cmap="Blues"))
