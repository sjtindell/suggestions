from flask import request, jsonify
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app import app
from app.data_manager import load_data, calculate_scores

data_df = load_data()

app.config['CACHE_TYPE'] = 'simple' # could be Redis in prod
cache = Cache(app)

# rate limit to handle load
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=['200 per day", "50 per hour'],
    storage_uri='memory://',
)

@app.route('/suggestions')
@limiter.limit('10 per second') # faster than user can type for autocomplete
def suggestions():
    query = request.args.get('q', '')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    results_df = calculate_scores(data_df, query, latitude, longitude)
    suggestions = results_df.to_dict('records')

    response = {
        'suggestions': [
            {
                'name': f"{row['name']}, {row['admin1']}, {row['country']}",
                'latitude': row['lat'],
                'longitude': row['long'],
                'score': row['score']
            } for row in suggestions
        ]
    }

    return jsonify(response)
