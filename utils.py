import pandas as pd
import numpy as np
import re
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


def forecast(model_path, data_path, day):

    model = load_model(model_path)

    #import data
    df = pd.read_csv(data_path, sep =";")

    df['Harga'] =  df['Harga'].apply(lambda x: re.sub('[^0-9]','', str(x)))
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], format="%d/%m/%Y")

    df.set_index('Tanggal', inplace=True)
    df = df.sort_index()

    df['Harga'] = df['Harga'].astype(np.int64)

    scaler = MinMaxScaler(feature_range = (0, 1))
    df_norm = scaler.fit_transform(df)
    df_norm = df_norm.reshape((-1,1))

    look_back = 2

    ## PREDICTTT

    close_data = df_norm.reshape((-1))

    def predict(num_prediction, model):
        prediction_list = close_data[-look_back:]

        for _ in range(num_prediction):
            x = prediction_list[-look_back:]
            x = x.reshape((1, look_back, 1))
            out = model.predict(x)[0][0]
            prediction_list = np.append(prediction_list, out)
        prediction_list = prediction_list[look_back-1:]

        return prediction_list

    def predict_dates(num_prediction):
        last_date = df.index.values[-1]
        prediction_dates = pd.date_range(last_date, periods=num_prediction+1).tolist()
        return prediction_dates
        

    #prediksi 100 hari ke depan
    num_prediction = day
    forecast = predict(num_prediction, model)
    forecast_dates = predict_dates(num_prediction)

    #data normalisasi (0-1) diinverse untuk mendapatkan nilai asli untuk visualisasi
    forecast = scaler.inverse_transform([forecast])

    # create a dictionary from the lists
    data = {'forecast_dates': forecast_dates, 'price': forecast.reshape(-1)}

    # create a dataframe from the dictionary
    df_fore = pd.DataFrame(data)

    # print the dataframe
    df_fore['price'] = df_fore['price'].astype(np.int64)

    return df, df_fore