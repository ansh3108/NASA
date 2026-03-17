import requests
from flask import Flask, render_template 

app = Flask(__name__)

NASA_API_KEY = 'HJ9wMZq8bcduhcQCP8jKywhrKiUrK2sXRMwJLk3P'

@app.route('/')
def index():
    url  = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    res = requests.get(url)
    data = res.json()
    return render_template('index.html', data=data)

@app.route('/mars')
def mars():
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={NASA_API_KEY}"
    response= requests.get(url)
    data = response.json()
    photos= data.get('latest_photos', [])[:12]
    return render_template('mars.html', photos=photos)

@app.route('/iss')
def iss():
    return render_template('iss.html')

if __name__ == '__main__':
    app.run(debug=True)