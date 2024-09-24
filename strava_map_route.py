from flask import Flask, render_template, request, redirect, url_for
import requests
from pprint import pprint

app = Flask(__name__)

# Strava API credentials
ACCESS_TOKEN = '223d76a8ac1db5254c380d7ba1235e524a5ad4fa'

# First page: asks for a postcode
@app.route('/', methods=['GET', 'POST'])
def postcode():
    if request.method == 'POST':
        postcode = request.form['postcode']
        return redirect(url_for('routes', postcode=postcode))
    return render_template('postcode.html')

# Second page: display running routes using Strava API
@app.route('/routes/<postcode>', methods=['GET'])
def routes(postcode):
    # (Optional) You can use an external API to convert postcode to lat/lng.
    # For now, we'll hardcode some lat/lng coordinates for demonstration purposes.
    latitude = 51.5074  # Example: central London
    longitude = -0.1278  # Example: central London

    # Strava API URL to get routes near a location
    url = f'https://www.strava.com/api/v3/athlete/routes'

    # Set up the authorization headers with the access token
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    # Make the API request to get routes
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        routes_data = response.json()  # This will return a list of routes
        pprint(routes_data)  # For debugging purposes
        return render_template('routes.html', postcode=postcode, routes=routes_data)
    else:
        return f"Error fetching routes from Strava: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)
