from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

# Create Flask app - Vercel requires specific configuration
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            header {
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .search-section {
                margin-bottom: 30px;
            }
            .search-box {
                display: flex;
                gap: 10px;
                max-width: 400px;
                margin: 0 auto;
            }
            #cityInput {
                flex: 1;
                padding: 12px 16px;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            button {
                padding: 12px 24px;
                background: #00b894;
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: background 0.3s ease;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            button:hover {
                background: #00a085;
            }
            .weather-card {
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                text-align: center;
                margin: 20px auto;
                max-width: 500px;
                display: none;
            }
            .temperature {
                font-size: 4rem;
                font-weight: 300;
                color: #0984e3;
            }
            .loading {
                text-align: center;
                color: white;
                display: none;
            }
            .error {
                background: #ff6b6b;
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px auto;
                max-width: 500px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🌤️ Weather Dashboard</h1>
                <p>Get current weather information for any city</p>
            </header>
            
            <div class="search-section">
                <div class="search-box">
                    <input type="text" id="cityInput" placeholder="Enter city name..." value="London" />
                    <button onclick="getWeather()">Get Weather</button>
                </div>
            </div>
            
            <div id="loading" class="loading">
                <p>Loading weather data...</p>
            </div>
            
            <div id="weatherResult" class="weather-card">
                <h2 id="cityName"></h2>
                <div class="weather-info">
                    <div class="temp-section">
                        <span id="temperature" class="temperature"></span>
                        <span class="unit">°C</span>
                    </div>
                    <p id="description" style="font-size: 1.2rem; color: #636e72; margin: 20px 0;"></p>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px;">
                        <div style="padding: 10px; background: #f8f9fa; border-radius: 8px;">
                            <strong>Feels like:</strong> <span id="feelsLike"></span>°C
                        </div>
                        <div style="padding: 10px; background: #f8f9fa; border-radius: 8px;">
                            <strong>Humidity:</strong> <span id="humidity"></span>%
                        </div>
                        <div style="padding: 10px; background: #f8f9fa; border-radius: 8px;">
                            <strong>Wind:</strong> <span id="windSpeed"></span> km/h
                        </div>
                        <div style="padding: 10px; background: #f8f9fa; border-radius: 8px;">
                            <strong>Updated:</strong> <span id="timestamp"></span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div id="error" class="error">
                <p id="errorMessage"></p>
            </div>
        </div>
        
        <script>
            async function getWeather() {
                const cityInput = document.getElementById('cityInput');
                const city = cityInput.value.trim();
                
                if (!city) {
                    showError('Please enter a city name');
                    return;
                }
                
                showLoading(true);
                hideError();
                hideWeatherResult();
                
                try {
                    const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
                    const data = await response.json();
                    
                    if (response.ok) {
                        displayWeather(data);
                    } else {
                        showError(data.error || 'Failed to fetch weather data');
                    }
                } catch (error) {
                    showError('Network error. Please try again.');
                } finally {
                    showLoading(false);
                }
            }

            function displayWeather(data) {
                document.getElementById('cityName').textContent = data.city;
                document.getElementById('temperature').textContent = data.temperature;
                document.getElementById('description').textContent = data.description;
                document.getElementById('feelsLike').textContent = data.feels_like;
                document.getElementById('humidity').textContent = data.humidity;
                document.getElementById('windSpeed').textContent = data.wind_speed;
                document.getElementById('timestamp').textContent = new Date().toLocaleString();
                
                document.getElementById('weatherResult').style.display = 'block';
            }

            function showLoading(show) {
                document.getElementById('loading').style.display = show ? 'block' : 'none';
            }

            function showError(message) {
                document.getElementById('errorMessage').textContent = message;
                document.getElementById('error').style.display = 'block';
            }

            function hideError() {
                document.getElementById('error').style.display = 'none';
            }

            function hideWeatherResult() {
                document.getElementById('weatherResult').style.display = 'none';
            }

            document.getElementById('cityInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    getWeather();
                }
            });

            // Load default weather on page load
            window.addEventListener('load', function() {
                getWeather();
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city', 'London')
    
    try:
        # Using wttr.in API which is reliable and free
        url = f"https://wttr.in/{city}?format=j1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            weather_data = {
                'city': city.title(),
                'temperature': current['temp_C'],
                'description': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_speed': current['windspeedKmph'],
                'feels_like': current['FeelsLikeC'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return jsonify(weather_data)
        else:
            return jsonify({'error': f'Weather data not found for {city}'}), 404
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout. Please try again.'}), 408
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Weather service temporarily unavailable'}), 503
    except KeyError as e:
        return jsonify({'error': 'Invalid weather data received'}), 502
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'service': 'Weather Dashboard API'
    })

# This is required for Vercel
def handler(request):
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True)