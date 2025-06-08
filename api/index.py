from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Add CORS headers for better API compatibility
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city', 'London')
    
    if not city or len(city.strip()) == 0:
        return jsonify({'error': 'City name is required'}), 400
    
    # Clean the city name
    city = city.strip()
    
    try:
        # Using wttr.in API with better error handling
        url = f"https://wttr.in/{city}?format=j1"
        headers = {
            'User-Agent': 'WeatherDashboard/1.0'
        }
        
        response = requests.get(url, timeout=15, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if the API returned valid data
            if 'current_condition' not in data or len(data['current_condition']) == 0:
                return jsonify({'error': 'Weather data not available for this location'}), 404
            
            current = data['current_condition'][0]
            
            # Extract weather information with fallbacks
            weather_data = {
                'city': city.title(),
                'temperature': current.get('temp_C', 'N/A'),
                'description': current.get('weatherDesc', [{'value': 'Unknown'}])[0]['value'],
                'humidity': current.get('humidity', 'N/A'),
                'wind_speed': current.get('windspeedKmph', 'N/A'),
                'feels_like': current.get('FeelsLikeC', 'N/A'),
                'pressure': current.get('pressure', 'N/A'),
                'visibility': current.get('visibility', 'N/A'),
                'uv_index': current.get('uvIndex', 'N/A'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return jsonify(weather_data)
        
        elif response.status_code == 404:
            return jsonify({'error': f'City "{city}" not found. Please check the spelling.'}), 404
        else:
            return jsonify({'error': 'Weather service temporarily unavailable'}), 503
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout. Please try again.'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Unable to connect to weather service'}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Network error occurred'}), 503
    except Exception as e:
        # Log the error in production
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Add a catch-all route for better error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)