from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Free weather API (no key required for basic usage)
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city', 'London')
    
    # Using a free weather service (you can replace with OpenWeatherMap API key)
    try:
        # Alternative free weather API
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            weather_data = {
                'city': city,
                'temperature': current['temp_C'],
                'description': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph'],
                'feels_like': current['FeelsLikeC'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return jsonify(weather_data)
        else:
            return jsonify({'error': 'City not found'}), 404
            
    except Exception as e:
        return jsonify({'error': 'Weather service unavailable'}), 500

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True)