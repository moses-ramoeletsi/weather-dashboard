let currentWeatherData = null;
let isDarkTheme = false;

const weatherIcons = {
    'clear': '☀️',
    'sunny': '☀️',
    'partly cloudy': '⛅',
    'cloudy': '☁️',
    'overcast': '☁️',
    'rain': '🌧️',
    'light rain': '🌦️',
    'heavy rain': '⛈️',
    'snow': '❄️',
    'fog': '🌫️',
    'mist': '🌫️',
    'thunderstorm': '⛈️',
    'drizzle': '🌦️'
};

const funFacts = [
    "A single cloud can weigh more than a million pounds!",
    "Lightning strikes the Earth about 100 times per second.",
    "The highest recorded temperature on Earth was 134°F (56.7°C) in Death Valley.",
    "Antarctica is the windiest continent with winds reaching 200 mph.",
    "Raindrops are not actually tear-shaped - they're more like hamburger buns!",
    "The smell of rain has a name: petrichor.",
    "Snowflakes are not actually white - they're translucent!",
    "The average cumulus cloud weighs about 1.1 million pounds.",
    "Hail can grow as large as grapefruits in severe storms.",
    "Weather affects your mood more than you think - it's called meteoropathy!"
];

const weatherJokes = [
    "Why don't weather forecasters ever get tired? Because they're always under pressure!",
    "What did the hurricane say to the other hurricane? I have my eye on you!",
    "Why don't clouds ever get speeding tickets? Because they're always drifting!",
    "What's the difference between weather and climate? You can't weather a tree, but you can climate!",
    "Why did the weather reporter break up with the meteorologist? There was no chemistry!",
    "What do you call a grumpy meteorologist? A cloud with a silver lining!",
    "Why don't meteorologists ever play poker? Because they always fold under pressure!",
    "What did one raindrop say to another? Two's company, three's a cloud!"
];

const activities = {
    sunny: [
        { emoji: '🏖️', activity: 'Beach Day', description: 'Perfect for sunbathing!' },
        { emoji: '🚴', activity: 'Cycling', description: 'Great weather for biking!' },
        { emoji: '🧺', activity: 'Picnic', description: 'Ideal for outdoor dining!' },
        { emoji: '⚽', activity: 'Sports', description: 'Play your favorite game!' }
    ],
    rainy: [
        { emoji: '📚', activity: 'Reading', description: 'Cozy indoor time!' },
        { emoji: '🎬', activity: 'Movie Night', description: 'Perfect for Netflix!' },
        { emoji: '🍳', activity: 'Cooking', description: 'Try a new recipe!' },
        { emoji: '🧩', activity: 'Puzzles', description: 'Brain exercise time!' }
    ],
    cloudy: [
        { emoji: '📸', activity: 'Photography', description: 'Great natural lighting!' },
        { emoji: '🚶', activity: 'Walking', description: 'Perfect temperature!' },
        { emoji: '☕', activity: 'Café Hopping', description: 'Explore local spots!' },
        { emoji: '🎨', activity: 'Art', description: 'Creative inspiration!' }
    ],
    cold: [
        { emoji: '🏠', activity: 'Stay Cozy', description: 'Hot chocolate time!' },
        { emoji: '🧶', activity: 'Crafting', description: 'Perfect for DIY projects!' },
        { emoji: '🍲', activity: 'Cooking Soup', description: 'Warm comfort food!' },
        { emoji: '🛁', activity: 'Hot Bath', description: 'Ultimate relaxation!' }
    ]
};

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
        // Simulate API call with mock data
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockData = {
            city: city,
            temperature: Math.floor(Math.random() * 30) + 5,
            description: ['sunny', 'cloudy', 'rainy', 'partly cloudy'][Math.floor(Math.random() * 4)],
            feels_like: Math.floor(Math.random() * 30) + 5,
            humidity: Math.floor(Math.random() * 60) + 30,
            wind_speed: Math.floor(Math.random() * 20) + 5,
            uv_index: Math.floor(Math.random() * 10) + 1,
            timestamp: new Date().toLocaleString()
        };

        currentWeatherData = mockData;
        displayWeather(mockData);
        updateWeatherAnimation(mockData.description);
        generateFunFact();
        updateActivities(mockData);
        updateMoodMeter(mockData);
        getWeatherJoke();
        
    } catch (error) {
        showError('Failed to fetch weather data. Please try again.');
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
    document.getElementById('uvIndex').textContent = data.uv_index;

    document.getElementById('weatherResult').classList.remove('hidden');
    document.getElementById('activitiesSection').classList.remove('hidden');
    document.getElementById('moodMeter').classList.remove('hidden');
    document.getElementById('weatherJoke').classList.remove('hidden');
}

function updateWeatherAnimation(description) {
    const animationElement = document.getElementById('weatherAnimation');
    const icon = weatherIcons[description.toLowerCase()] || '🌤️';
    animationElement.textContent = icon;
}

function generateFunFact() {
    const container = document.getElementById('funFactsContainer');
    const randomFact = funFacts[Math.floor(Math.random() * funFacts.length)];
    container.innerHTML = `<div class="fun-fact">${randomFact}</div>`;
}

function updateActivities(data) {
    const grid = document.getElementById('activitiesGrid');
    let activityType = 'sunny';
    
    if (data.description.includes('rain')) activityType = 'rainy';
    else if (data.description.includes('cloud')) activityType = 'cloudy';
    else if (data.temperature < 10) activityType = 'cold';

    const relevantActivities = activities[activityType] || activities.sunny;
    
    grid.innerHTML = relevantActivities.map(activity => `
        <div class="activity-card" onclick="selectActivity('${activity.activity}')">
            <div style="font-size: 2rem; margin-bottom: 10px;">${activity.emoji}</div>
            <h4>${activity.activity}</h4>
            <p style="font-size: 0.9rem; margin-top: 5px;">${activity.description}</p>
        </div>
    `).join('');
}

function updateMoodMeter(data) {
    const indicator = document.getElementById('moodIndicator');
    const emoji = document.getElementById('moodEmoji');
    const description = document.getElementById('moodDescription');
    
    let moodScore = 50; // Base mood
    
    // Weather factors
    if (data.description.includes('sunny')) moodScore += 30;
    else if (data.description.includes('rain')) moodScore -= 20;
    else if (data.description.includes('cloud')) moodScore += 10;
    
    // Temperature factors
    if (data.temperature >= 20 && data.temperature <= 25) moodScore += 20;
    else if (data.temperature < 5 || data.temperature > 35) moodScore -= 15;
    
    // Humidity factors
    if (data.humidity > 80) moodScore -= 10;
    
    moodScore = Math.max(0, Math.min(100, moodScore));
    
    indicator.style.left = `${moodScore}%`;
    
    if (moodScore >= 80) {
        emoji.textContent = '😊';
        description.textContent = 'Perfect weather for a great mood!';
    } else if (moodScore >= 60) {
        emoji.textContent = '🙂';
        description.textContent = 'Pretty good weather conditions!';
    } else if (moodScore >= 40) {
        emoji.textContent = '😐';
        description.textContent = 'Weather is okay, could be better.';
    } else {
        emoji.textContent = '😔';
        description.textContent = 'Weather might affect your mood today.';
    }
}

function getWeatherJoke() {
    const jokeElement = document.getElementById('jokeText');
    const randomJoke = weatherJokes[Math.floor(Math.random() * weatherJokes.length)];
    jokeElement.textContent = randomJoke;
}

function selectActivity(activity) {
    alert(`Great choice! ${activity} sounds perfect for this weather! 🎉`);
}

function quickSearch(city) {
    document.getElementById('cityInput').value = city;
    getWeather();
}

function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                // For demo purposes, we'll just use a default city
                document.getElementById('cityInput').value = 'Current Location';
                getWeather();
            },
            error => {
                showError('Unable to get your location. Please enter a city manually.');
            }
        );
    } else {
        showError('Geolocation is not supported by this browser.');
    }
}

function toggleTheme() {
    isDarkTheme = !isDarkTheme;
    document.body.classList.toggle('dark-theme', isDarkTheme);
    document.querySelector('.theme-toggle').textContent = isDarkTheme ? '☀️' : '🌙';
}

function showLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').classList.remove('hidden');
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function hideWeatherResult() {
    document.getElementById('weatherResult').classList.add('hidden');
    document.getElementById('activitiesSection').classList.add('hidden');
    document.getElementById('moodMeter').classList.add('hidden');
    document.getElementById('weatherJoke').classList.add('hidden');
}

// Event listeners
document.getElementById('cityInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        getWeather();
    }
});

// Initialize with default city
window.addEventListener('load', function() {
    document.getElementById('cityInput').value = 'London';
    getWeather();
});