from flask import Flask, render_template, request, jsonify
import requests
import os
import json
import random
from datetime import datetime, timedelta
import time

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'your_api_key_here')
WEATHER_CACHE = {}
CACHE_DURATION = 600  # 10 minutes

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
    
    # Check cache first
    cache_key = city.lower()
    if cache_key in WEATHER_CACHE:
        cached_data, timestamp = WEATHER_CACHE[cache_key]
        if time.time() - timestamp < CACHE_DURATION:
            return jsonify(cached_data)
    
    try:
        # Using wttr.in API with better error handling
        url = f"https://wttr.in/{city}?format=j1"
        headers = {
            'User-Agent': 'WeatherDashboard/2.0'
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
                'temperature': int(current.get('temp_C', 20)),
                'description': current.get('weatherDesc', [{'value': 'Unknown'}])[0]['value'],
                'humidity': int(current.get('humidity', 50)),
                'wind_speed': float(current.get('windspeedKmph', 10)),
                'feels_like': int(current.get('FeelsLikeC', 20)),
                'pressure': int(current.get('pressure', 1013)),
                'visibility': int(current.get('visibility', 10)),
                'uv_index': int(current.get('uvIndex', 5)),
                'cloud_cover': int(current.get('cloudcover', 30)),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'weather_code': current.get('weatherCode', '113'),
                'wind_direction': current.get('winddir16Point', 'N'),
                'precipitation': float(current.get('precipMM', 0))
            }
            
            # Add forecast data if available
            if 'weather' in data and len(data['weather']) > 0:
                forecast = []
                for day_data in data['weather'][:5]:  # Next 5 days
                    forecast.append({
                        'date': day_data.get('date', ''),
                        'max_temp': int(day_data.get('maxtempC', 25)),
                        'min_temp': int(day_data.get('mintempC', 15)),
                        'description': day_data.get('hourly', [{}])[0].get('weatherDesc', [{'value': 'Unknown'}])[0]['value'] if day_data.get('hourly') else 'Unknown'
                    })
                weather_data['forecast'] = forecast
            
            # Cache the result
            WEATHER_CACHE[cache_key] = (weather_data, time.time())
            
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

@app.route('/api/weather/extended/<city>')
def get_extended_weather(city):
    """Get extended weather information including air quality and alerts"""
    try:
        # This would integrate with additional APIs for comprehensive data
        extended_data = {
            'air_quality': {
                'aqi': random.randint(50, 150),
                'pm25': random.randint(10, 50),
                'pm10': random.randint(20, 80),
                'o3': random.randint(30, 120),
                'status': 'Moderate'
            },
            'sun_times': {
                'sunrise': '06:30 AM',
                'sunset': '07:45 PM',
                'daylight_hours': 13.25
            },
            'moon_phase': {
                'phase': 'Waxing Crescent',
                'illumination': 25,
                'emoji': '🌒'
            },
            'weather_alerts': []
        }
        
        return jsonify(extended_data)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch extended weather data'}), 500

@app.route('/api/activities')
def get_weather_activities():
    """Get activity recommendations based on weather conditions"""
    temp = request.args.get('temp', type=int, default=20)
    condition = request.args.get('condition', default='sunny').lower()
    humidity = request.args.get('humidity', type=int, default=50)
    
    activities = []
    
    # Temperature-based activities
    if temp >= 25:
        activities.extend([
            {'name': 'Swimming', 'emoji': '🏊', 'category': 'outdoor'},
            {'name': 'Beach Volleyball', 'emoji': '🏐', 'category': 'outdoor'},
            {'name': 'Ice Cream Shopping', 'emoji': '🍦', 'category': 'leisure'}
        ])
    elif temp >= 15:
        activities.extend([
            {'name': 'Hiking', 'emoji': '🥾', 'category': 'outdoor'},
            {'name': 'Cycling', 'emoji': '🚴', 'category': 'outdoor'},
            {'name': 'Outdoor Photography', 'emoji': '📸', 'category': 'creative'}
        ])
    else:
        activities.extend([
            {'name': 'Museum Visit', 'emoji': '🏛️', 'category': 'indoor'},
            {'name': 'Hot Chocolate', 'emoji': '☕', 'category': 'leisure'},
            {'name': 'Indoor Rock Climbing', 'emoji': '🧗', 'category': 'indoor'}
        ])
    
    # Weather condition-based activities
    if 'rain' in condition:
        activities.extend([
            {'name': 'Reading', 'emoji': '📚', 'category': 'indoor'},
            {'name': 'Board Games', 'emoji': '🎲', 'category': 'indoor'},
            {'name': 'Cooking', 'emoji': '👨‍🍳', 'category': 'indoor'}
        ])
    elif 'sunny' in condition:
        activities.extend([
            {'name': 'Picnic', 'emoji': '🧺', 'category': 'outdoor'},
            {'name': 'Gardening', 'emoji': '🌱', 'category': 'outdoor'},
            {'name': 'Outdoor Sports', 'emoji': '⚽', 'category': 'outdoor'}
        ])
    
    return jsonify({'activities': activities[:6]})  # Return top 6 activities

@app.route('/api/mood-analysis')
def analyze_weather_mood():
    """Analyze how weather conditions affect mood"""
    temp = request.args.get('temp', type=int, default=20)
    condition = request.args.get('condition', default='sunny').lower()
    humidity = request.args.get('humidity', type=int, default=50)
    uv_index = request.args.get('uv', type=int, default=5)
    
    mood_score = 50  # Base neutral mood
    
    # Temperature effects
    if 18 <= temp <= 24:
        mood_score += 25  # Optimal temperature range
    elif temp < 5 or temp > 35:
        mood_score -= 20  # Extreme temperatures
    elif temp < 10 or temp > 30:
        mood_score -= 10  # Uncomfortable temperatures
    
    # Weather condition effects
    mood_modifiers = {
        'sunny': 20,
        'clear': 20,
        'partly cloudy': 10,
        'cloudy': -5,
        'overcast': -10,
        'light rain': -15,
        'rain': -20,
        'heavy rain': -25,
        'thunderstorm': -30,
        'snow': 5,  # Many people enjoy snow
        'fog': -15
    }
    
    mood_score += mood_modifiers.get(condition, 0)
    
    # Humidity effects
    if humidity > 80:
        mood_score -= 15
    elif humidity < 30:
        mood_score -= 10
    
    # UV Index effects (vitamin D production)
    if 3 <= uv_index <= 6:
        mood_score += 10
    elif uv_index > 8:
        mood_score -= 5
    
    # Ensure score is within bounds
    mood_score = max(0, min(100, mood_score))
    
    # Determine mood category and recommendations
    if mood_score >= 80:
        mood_category = 'Excellent'
        emoji = '😊'
        recommendation = 'Perfect weather for outdoor activities!'
    elif mood_score >= 60:
        mood_category = 'Good'
        emoji = '🙂'
        recommendation = 'Great weather for most activities!'
    elif mood_score >= 40:
        mood_category = 'Fair'
        emoji = '😐'
        recommendation = 'Weather is okay, choose activities wisely.'
    elif mood_score >= 20:
        mood_category = 'Poor'
        emoji = '😕'
        recommendation = 'Weather might affect your mood. Consider indoor activities.'
    else:
        mood_category = 'Very Poor'
        emoji = '😔'
        recommendation = 'Stay cozy indoors and practice self-care.'
    
    return jsonify({
        'mood_score': mood_score,
        'category': mood_category,
        'emoji': emoji,
        'recommendation': recommendation,
        'factors': {
            'temperature_impact': 'Optimal' if 18 <= temp <= 24 else 'Suboptimal',
            'weather_impact': condition.title(),
            'humidity_impact': 'High' if humidity > 80 else 'Normal'
        }
    })

@app.route('/api/weather-jokes')
def get_weather_jokes():
    """Get weather-related jokes"""
    jokes = [
        "Why don't weather forecasters ever get tired? Because they're always under pressure!",
        "What did the hurricane say to the other hurricane? I have my eye on you!",
        "Why don't clouds ever get speeding tickets? Because they're always drifting!",
        "What's the difference between weather and climate? You can't weather a tree, but you can climate!",
        "Why did the weather reporter break up with the meteorologist? There was no chemistry!",
        "What do you call a grumpy meteorologist? A cloud with a silver lining!",
        "Why don't meteorologists ever play poker? Because they always fold under pressure!",
        "What did one raindrop say to another? Two's company, three's a cloud!",
        "Why don't hurricanes ever get dizzy? Because they're used to spinning!",
        "What do you call a weather app that doesn't work? A whether app!"
    ]
    
    return jsonify({
        'joke': random.choice(jokes),
        'total_jokes': len(jokes)
    })

@app.route('/api/weather-facts')
def get_weather_facts():
    """Get interesting weather facts"""
    facts = [
        "A single cloud can weigh more than a million pounds!",
        "Lightning strikes the Earth about 100 times per second.",
        "The highest recorded temperature on Earth was 134°F (56.7°C) in Death Valley.",
        "Antarctica is the windiest continent with winds reaching 200 mph.",
        "Raindrops are not actually tear-shaped - they're more like hamburger buns!",
        "The smell of rain has a name: petrichor.",
        "Snowflakes are not actually white - they're translucent!",
        "The average cumulus cloud weighs about 1.1 million pounds.",
        "Hail can grow as large as grapefruits in severe storms.",
        "Weather affects your mood more than you think - it's called meteoropathy!",
        "The wettest place on Earth receives over 460 inches of rain per year.",
        "A bolt of lightning is five times hotter than the surface of the sun.",
        "The wind on Neptune can reach speeds of 1,200 mph.",
        "Tornadoes can have wind speeds of over 300 mph.",
        "The largest hailstone ever recorded weighed nearly 2 pounds!"
    ]
    
    return jsonify({
        'fact': random.choice(facts),
        'category': 'weather_trivia',
        'total_facts': len(facts)
    })

@app.route('/api/weather-comparison')
def compare_weather():
    """Compare weather between multiple cities"""
    cities = request.args.get('cities', '').split(',')
    if len(cities) < 2:
        return jsonify({'error': 'Please provide at least 2 cities separated by commas'}), 400
    
    comparison_data = []
    
    for city in cities[:5]:  # Limit to 5 cities
        city = city.strip()
        if city:
            # This would normally fetch real data for each city
            # For demo purposes, generating mock data
            city_data = {
                'city': city.title(),
                'temperature': random.randint(5, 35),
                'condition': random.choice(['sunny', 'cloudy', 'rainy', 'partly cloudy']),
                'humidity': random.randint(30, 90),
                'wind_speed': random.randint(5, 25)
            }
            comparison_data.append(city_data)
    
    # Find extremes
    if comparison_data:
        hottest = max(comparison_data, key=lambda x: x['temperature'])
        coldest = min(comparison_data, key=lambda x: x['temperature'])
        most_humid = max(comparison_data, key=lambda x: x['humidity'])
        windiest = max(comparison_data, key=lambda x: x['wind_speed'])
        
        return jsonify({
            'cities': comparison_data,
            'analysis': {
                'hottest': hottest,
                'coldest': coldest,
                'most_humid': most_humid,
                'windiest': windiest
            }
        })
    
    return jsonify({'error': 'No valid cities provided'}), 400

@app.route('/api/clothing-suggestions')
def get_clothing_suggestions():
    """Get clothing suggestions based on weather"""
    temp = request.args.get('temp', type=int, default=20)
    condition = request.args.get('condition', default='sunny').lower()
    wind_speed = request.args.get('wind', type=int, default=10)
    humidity = request.args.get('humidity', type=int, default=50)
    
    suggestions = []
    
    # Temperature-based clothing
    if temp >= 30:
        suggestions.extend(['Light cotton t-shirt', 'Shorts', 'Sandals', 'Hat', 'Sunglasses'])
    elif temp >= 20:
        suggestions.extend(['T-shirt', 'Light pants', 'Sneakers', 'Light jacket (evening)'])
    elif temp >= 10:
        suggestions.extend(['Long sleeves', 'Jeans', 'Light sweater', 'Closed shoes'])
    elif temp >= 0:
        suggestions.extend(['Warm sweater', 'Jacket', 'Long pants', 'Boots', 'Scarf'])
    else:
        suggestions.extend(['Heavy coat', 'Warm layers', 'Winter boots', 'Gloves', 'Warm hat'])
    
    # Weather condition adjustments
    if 'rain' in condition:
        suggestions.extend(['Umbrella', 'Waterproof jacket', 'Water-resistant shoes'])
    
    if wind_speed > 20:
        suggestions.append('Windbreaker')
    
    if humidity > 80:
        suggestions.append('Breathable fabrics')
    
    return jsonify({
        'suggestions': list(set(suggestions)),  # Remove duplicates
        'weather_summary': f"{temp}°C, {condition}, {wind_speed} km/h wind"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'features': [
            'basic_weather',
            'extended_weather',
            'activity_recommendations',
            'mood_analysis',
            'weather_jokes',
            'weather_facts',
            'city_comparison',
            'clothing_suggestions'
        ]
    })

# Add a catch-all route for better error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)