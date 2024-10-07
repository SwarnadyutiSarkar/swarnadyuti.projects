from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample GeoJSON data
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-73.935242, 40.730610]  # New York City
            },
            "properties": {
                "name": "New York City",
                "description": "The largest city in the United States."
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-118.243683, 34.052235]  # Los Angeles
            },
            "properties": {
                "name": "Los Angeles",
                "description": "Known for its Mediterranean climate."
            }
        }
    ]
}

@app.route('/geojson')
def get_geojson():
    return jsonify(geojson_data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
