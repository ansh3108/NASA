import requests
from flask import Flask, render_template 

app = Flask(__name__)

NASA_API_KEY = 'HJ9wMZq8bcduhcQCP8jKywhrKiUrK2sXRMwJLk3P'

@app.route('/')
def index():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    res = requests.get(url)
    data = res.json()
    return render_template('index.html', data=data)

@app.route('/mars')
def mars():
    
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos?sol=1000&api_key={NASA_API_KEY}"
    
    try:
        res = requests.get(url, timeout=15) 
        res.raise_for_status()
        data = res.json()
        
        photos = data.get('photos', [])[:12]
        
        if not photos:
            return "NASA returned 200 OK but the photo list is empty. Try Sol 500."

        return render_template('mars.html', photos=photos)

    except Exception as e:
        return f"Network Error: {e}. If you see Name.com, your DNS is blocking NASA."


@app.route('/iss')
def iss():
    return render_template('iss.html')


if __name__ == '__main__':
    app.run(debug=True)