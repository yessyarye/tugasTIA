from flask import Flask, request, render_template, jsonify
import threading
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# Inisialisasi Flask
app = Flask(__name__)

# Fungsi untuk mengambil data cuaca dari OpenWeather API
def get_weather_data(api_key, city):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

# Fungsi untuk mengubah data cuaca ke DataFrame
def parse_weather_data(weather_data):
    df = pd.json_normalize(weather_data, record_path=['list'])
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    df.set_index('dt', inplace=True)
    df = df[['main.temp_max']]
    df.columns = ['Temp_Max']
    return df

# Route untuk halaman utama
@app.route('/')
def index():
    cities = ['Jakarta', 'Surabaya', 'Bandung', 'Yogyakarta', 'Medan']  # Daftar kota untuk combo box
    return render_template('index.html', cities=cities)

# Route untuk memproses data cuaca dan melakukan peramalan
@app.route('/forecast', methods=['POST'])
def forecast():
    # Ambil input dari pengguna
    api_key = request.form['api_key']
    city = request.form['city']
    days = int(request.form['days'])

    try:
        # Ambil dan parse data cuaca
        weather_data = get_weather_data(api_key, city)
        data = parse_weather_data(weather_data)

        # Siapkan data untuk model
        data['Hour'] = data.index.hour
        data['Day'] = data.index.dayofweek
        data['Month'] = data.index.month
        X = data[['Hour', 'Day', 'Month']]
        y = data['Temp_Max']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dtest = xgb.DMatrix(X_test, label=y_test)

        # Parameter untuk XGBoost
        params = {'objective': 'reg:squarederror', 'colsample_bytree': 0.3, 'learning_rate': 0.1, 'max_depth': 5, 'alpha': 10}
        model = xgb.train(params, dtrain, num_boost_round=100)

        # Peramalan masa depan
        future_hours = np.array([[i % 24, (i // 24) % 7, (i // 24) % 12 + 1] for i in range(len(data), len(data) + days * 24)])
        future_df = pd.DataFrame(future_hours, columns=['Hour', 'Day', 'Month'])
        future_dmatrix = xgb.DMatrix(future_df)
        future_predictions = model.predict(future_dmatrix)

        # Format hasil peramalan
        future_dates = pd.date_range(start=data.index[-1] + pd.DateOffset(hours=1), periods=days * 24, freq='H')
        forecast_df = pd.DataFrame({'Forecast_Temp_Max': future_predictions}, index=future_dates)

        # Plot hasil peramalan
        plt.figure(figsize=(10, 6))
        plt.plot(data['Temp_Max'], label='Actual Data', color='blue')
        plt.plot(forecast_df, label='Future Forecast', color='red', linestyle='--')
        plt.title(f'Future Forecast of Maximum Temperature in {city}')
        plt.xlabel('Date')
        plt.ylabel('Maximum Temperature (°C)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()

        # Simpan plot ke buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        return render_template('forecast.html', city=city, days=days, image_base64=image_base64)

    except Exception as e:
        return jsonify({'error': str(e)})

# Fungsi untuk menjalankan Flask di thread terpisah (opsional)
def run_app():
    app.run(debug=True, use_reloader=False)  # Menonaktifkan reloader untuk menghindari error di notebook

# Main
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
