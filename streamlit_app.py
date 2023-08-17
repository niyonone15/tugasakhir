import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu
from utils import forecast

st.title("Prediksi Harga Emas")

#navigasi sidebar
with st.sidebar:
    selected = option_menu("Prediksi Harga Emas", ['Homepage', 'Data Harga Emas', 'Harian', 'Bulanan'],
        icons=['house','box', 'calendar', 'calendar'], menu_icon="...", default_index=0)
    selected


if selected == 'Harian':
    with st.sidebar:
        day = st.slider('Berapa hari?', 0, 100)
    with st.spinner('proses inference model...'):
        model_path = 'best_model.h5'
        data_path = 'harga_emas.csv'
        df, df_fore = forecast(model_path, data_path, day)
    st.write('Prediksi Data Harian')
    
    trace1 = go.Scatter(
        x = df.index,
        y = df['Harga'],
        mode = 'lines',
        name = 'Data',
        line = {'color': '#636EFA', 'width': 2}
    )

    trace2 = go.Scatter(
        x = df_fore['forecast_dates'],
        y = df_fore['price'],
        mode = 'lines',
        name = 'Forecast',
        line = {'color': '#FF6692', 'width': 2}
    )

    layout = go.Layout(
        title = "Price Prediction",
        xaxis = {'title' : "Date"},
        yaxis = {'title' : "Close"}
    )
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.dataframe(df_fore, width=500)

### Bulanan
if selected == 'Bulanan':
    with st.sidebar:
        month = st.selectbox(
            'Pilih Bulan',
            (1, 2, 3))
    if month == 1 :
        with st.sidebar:
            day = st.slider('Berapa hari?', 0, 31)
    if month == 2 : 
        with st.sidebar:
            temp = 28 
            day = st.slider('Berapa hari?',  0, 28)
            day = day+temp
    if month == 3 :
        with st.sidebar:
            temp = 28 + 28
            day = st.slider('Berapa hari?',  0, 31)
            day = day + temp     
    
    with st.spinner('proses inference model...'):
        model_path = 'best_model.h5'
        data_path = 'harga_emas.csv'
        df, df_fore = forecast(model_path, data_path, day)
    st.write('Prediksi Data Bulanan')

    df_fore['month'] = df_fore['forecast_dates'].dt.month
    df_show = df_fore[df_fore['month'] == month]

    trace1 = go.Scatter(
        x = df_show['forecast_dates'],
        y = df_show['price'],
        mode = 'lines',
        name = 'Data',
        line = {'color': '#FF6692', 'width': 2}
    )

    layout = go.Layout(
        title = "Price Prediction",
        xaxis = {'title' : "Date"},
        yaxis = {'title' : "Close"}
    )
    fig = go.Figure(data=[trace1], layout=layout)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.dataframe(df_show, width=500)

### Load DataFrame
if selected == 'Data Harga Emas':
    st.write('Data Harga Emas dari Tanggal 03 Januari 2019 sampai 03 Januari 2023 dari Website pusatdata.kontan.co.id. Dataset yang telah diambil dengan jumlah data yang digunakan sebanyak 1285 baris.')
    excel_file = 'harga_emasss.xlsx'
    sheet_name = 'Sheet1'
    title="Data Harga Emas Tahun 2019-2023"
    df = pd.read_excel(excel_file,
                    sheet_name=sheet_name,
                    usecols='A:B',
                    header=0)
    st.dataframe(df)

### Home Page
if selected == 'Homepage':
    st.subheader('Selamat Datang')
    st.write('Niyo None - 064001900041 Program Studi Teknik Informatika.')
    st.write('Pada dashboard prediksi harga emas, disini akan menampilkan beberapa kondisi prediksi harga emas yang dapat dibagi per prediksi dari harian hingga bulanan. Dalam melakukan prediksi harian dapat diatur sesuai dengan keinginan contoh. Jika ingin menampilkan prediksi selama 15 hari dapat diatur sesuai dengan hari yang ditentukan, begitu juga dengan bulan dapat diatur sesuai dengan prediksi hingga bulan yang telah diatur, yang nantinya akan menampilkan grafik dan tabel dari prediksi tersebut.')
