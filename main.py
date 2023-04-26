import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
from matplotlib import pyplot as plt

st.set_page_config(
    page_title='ENACOM: Reporte de Accesos a Internet Zonas y Tecnología en Cara al Incremento del Nivel del Mar',
    layout='wide'
)

'# ENACOM: Reporte de Accesos a Internet Zonas y Tecnología en Cara al Incremento del Nivel del Mar '


@st.cache_data
def get_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)


dataset1 = 'https://datosabiertos.enacom.gob.ar/rest/datastreams/275028/data.csv'
dataset2 = 'https://datosabiertos.enacom.gob.ar/rest/datastreams/279175/data.csv'
dataset3 = 'https://datosabiertos.enacom.gob.ar/rest/datastreams/290237/data.csv'


txt = 'Ingrese el valor deseado del KPI'

placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()


def etl(ds: str):
    """Aplica las transformaciones adecuadas a cada dataset en particular"""
    regiones = ['Catamarca', 'Jujuy', 'Chubut', 'La rioja', 'Mendoza', 'Neuquén', 'Salta', 'San juan', 'Tucumán']

    if ds.lower() == 'dataset1':
        pe_in = get_data(dataset1)
        df = pe_in.copy()
        df['Accesos por cada 100 hogares'] = df['Accesos por cada 100 hogares'].str.replace(',', '.').astype(float)
        return df

    if ds.lower() == 'dataset2':
        tec_lo = get_data(dataset2)
        tec_lo_copy = tec_lo.copy()
        tec_lo_copy['WIRELESS'].replace('- 0', '0', inplace=True)
        tec_lo_copy['WIRELESS'] = tec_lo_copy['WIRELESS'].astype(float)
        tec_lo_copy = tec_lo_copy[tec_lo_copy.Provincia.str.capitalize().isin(regiones) == True]
        df = tec_lo_copy.groupby('Provincia')['WIRELESS'].sum().round()
        df = df.reset_index()
        return df

    if ds.lower() == 'dataset3':
        vel_bajada = get_data(dataset3)
        vel_bajada_copy = vel_bajada.copy()
        del vel_bajada_copy['Unnamed: 4']
        del vel_bajada_copy['Unnamed: 5']
        vel_bajada_copy = vel_bajada_copy[vel_bajada_copy.Provincia.str.capitalize().isin(regiones) == True]
        return vel_bajada_copy

    if ds.lower() == 'dataset4':
        vel_bajada = get_data(dataset3)
        vel_bajada_copy2 = vel_bajada.copy()
        del vel_bajada_copy2['Unnamed: 4']
        del vel_bajada_copy2['Unnamed: 5']
        vel_bajada_copy2 = vel_bajada_copy2[vel_bajada_copy2.Provincia.str.capitalize().isin(regiones) == False]
        return vel_bajada_copy2


def kpi1_func(df: pd.DataFrame, provincia: str, year: int, KPI:int):
    
    df = df[df.Provincia.str.lower() == provincia.lower()]
    df = df[df['Año'] == year]
    df.sort_values('Trimestre', ascending=True, inplace=True)

    valores = df['Accesos por cada 100 hogares'].values
    aumento_accesos = []

    for i in range(len(valores) - 1):
        porcentaje = ((valores[i + 1] - valores[i]) / valores[i]) * 100
        aumento_accesos.append(porcentaje)

    promedio = sum(aumento_accesos) / len(aumento_accesos)

    meta1 = (sum(valores) * KPI) / 100

    print(f'Porcentajes de aumento entre cuartiles: {aumento_accesos}')
    print(f'Promedio de aumento: {round(promedio, 2)}%')
    print(f'Se requieren {round(meta1)} nuevas conexiones para lograr un aumento de {KPI}% el siguiente trimestre')

    return round(meta1), df, round(promedio, 2)


def kpi2_func(df, KPI):

    sum(df.WIRELESS)

    valores = df.WIRELESS.values

    meta2 = round((sum(df.WIRELESS) * (KPI / 100)))
    print(f'Para lograr un aumento del {KPI}% en las conexiones de tipo Wireless en las regiones montañosas de Argentina, se deben lograr una cantidad de {meta2} nuevos accesos.')

    return round(meta2), df


def kpi3_func(df, provincia, year, KPI):

    df = df[df.Provincia.str.lower() == provincia.lower()]
    df = df[df.Año == year]
    df.sort_values('Trimestre', ascending=True, inplace=True)

    valores = df['Mbps (Media de bajada)'].values

    aumento_vel = []

    for i in range(len(valores) - 1):
        porcentaje = ((valores[i + 1] - valores[i]) / valores[i]) * 100
        aumento_vel.append(porcentaje)

    promedio = sum(aumento_vel) / len(aumento_vel)

    meta3 = (sum(valores) * KPI) / 100

    print(f'Porcentaje de aumento entre cuartiles: {aumento_vel}')
    print(f'Promedio de aumento: {round(promedio, 2)}%')
    print(f'Se deben aumentar {round(meta3, 2)} Mbps para lograr un aumento del {KPI}% en la velocidad de bajada en las regiones montañosas el siguiente trimestre')

    return round(meta3, 2), df, round(promedio, 2)


def kpi4_func(df, provincia, year, KPI):

    df = df[df.Provincia.str.lower() == provincia.lower()]
    df = df[df.Año == year]
    df.sort_values('Trimestre', ascending=True, inplace=True)

    valores = df['Mbps (Media de bajada)'].values

    variacion_vel = []

    for i in range(len(valores) - 1):
        porcentaje = ((valores[i + 1] - valores[i]) / valores[i]) * 100
        variacion_vel.append(porcentaje)

    promedio = sum(variacion_vel) / len(variacion_vel)

    meta4 = (sum(valores) * (KPI / 100))

    print(f'Porcentaje de variación entre cuartiles: {variacion_vel}')
    print(f'Promedio de variación: {round(promedio, 2)}%')
    print(f'Se deben disminuir {round(meta4, 2)} Mbps para lograr un descenso del {KPI}% en la velocidad de bajada en las regiones NO montañosas el siguiente trimestre')

    return round(meta4, 2), df, round(promedio,2)


with placeholder1.container():
    '### KPI1 -> Aumentar en un 2% el acceso al servicio de internet para el próximo trimestre, cada 100 hogares, por provincia.'
    data1 = etl('dataset1')
    provincia = data1.Provincia.unique().tolist()
    year = data1.Año.unique().tolist()
    prov_select = st.selectbox('Provincia', provincia)
    year_select = st.selectbox('Seleccione un año', year, key='1')
    kpi1 = st.text_input(txt, 2, key='11')
    KPI1, df1, var = kpi1_func(data1, prov_select, int(year_select), int(kpi1))
    col1, col2, col_a = st.columns([2, 1, 3])

with col1:
    st.dataframe(data1, 500)


with col2:
    col2.metric(
        label='Conexiones necesarias',
        value=KPI1
    )

    col2.metric(
        label='Promedio variación',
        value=f'{var}%'
    )

    with col_a:
        st.line_chart(df1, x='Trimestre', y='Accesos por cada 100 hogares')

################################################################

with placeholder2.container():
    '### KPI2 -> Aumentar la tecnología wireless en las regiones montañosas en un 10%'
    data2 = etl('dataset2')
    kpi2 = st.text_input(txt, '10', key='22')
    KPI2, df2 = kpi2_func(data2, int(kpi2))

    col3, col4, col_b = st.columns([2, 1, 3])

    with col3:
        st.dataframe(df2, 500)

    with col4:
        col4.metric(
            label='Conexiones necesarias',
            value=KPI2
        )

    with col_b:
        st.bar_chart(df2, x='Provincia')

    ################################################################

with placeholder3.container():
    '### KPI3 -> Subir en 7% de velocidad de bajada en cada una de las regiones montañosas para el próximo cuartil.'
    data3 = etl('dataset3')
    provincia = data3.Provincia.unique().tolist()
    year = data3.Año.unique().tolist()
    prov_select = st.selectbox('Provincia', provincia)
    year_select = st.selectbox('Año', year, key='3')
    kpi3 = st.text_input(txt, 7, key='33')
    KPI3, df3, var = kpi3_func(data3, prov_select, int(year_select), int(kpi3))

    col5, col6, col_c = st.columns([2, 1, 3])

    with col5:
        st.dataframe(data3, 500)

    with col6:
        col6.metric(
            label='Mbps',
            value=f'{KPI3}Mb/s',
        )

        col6.metric(
            label='Promedio de variacion',
            value=f'{var}%'
        )

    with col_c:
        st.line_chart(df3, x='Trimestre', y='Mbps (Media de bajada)')

################################################################

with placeholder4.container():
    '### KPI4 -> Disminuir en 2% la velocidad de bajada en las provincias que no son montañosas'
    data4 = etl('dataset4')
    provincia = data4.Provincia.unique().tolist()
    year = data4.Año.unique().tolist()
    prov_select = st.selectbox('Provincia', provincia)
    year_select = st.selectbox('Año', year, key='4')
    kpi4 = st.text_input(txt, 2, key='44')
    KPI4, df4, var = kpi4_func(data4, prov_select, int(year_select), int(kpi4))
    col7, col8, col_d = st.columns([2, 1, 3])

    with col7:
        st.dataframe(data4, 500)

    with col8:
        col8.metric(
            label='Mbps',
            value=f'{KPI4}Mb/s'
        )
        col8.metric(
            label='Promedio de variacion',
            value=f'{var}%'
        )

    with col_d:
        st.line_chart(df4, x='Trimestre', y='Mbps (Media de bajada)')
