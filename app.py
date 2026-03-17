import requests
from flask import Flask, render_template 

app = Flask(__name__)

NASA_API_KEY = 'HJ9wMZq8bcduhcQCP8jKywhrKiUrK2sXRMwJLk3P' #pls dont abuse


def fetch_mars_gallery_photos(limit=12):
    url = "https://images-api.nasa.gov/search"
    params = {
        "q": "curiosity rover mars",
        "media_type": "image",
        "year_start": "2012",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    items = response.json().get("collection", {}).get("items", [])
    photos = []

    for item in items:
        data = item.get("data", [{}])[0]
        image_links = [
            link for link in item.get("links", [])
            if link.get("render") == "image" and link.get("href")
        ]

        if not image_links:
            continue

        photos.append(
            {
                "img_src": image_links[0]["href"],
                "earth_date": data.get("date_created", "Unknown")[:10],
                "camera": {
                    "full_name": data.get("title", "Curiosity Rover Archive")
                },
            }
        )

        if len(photos) >= limit:
            break

    return photos

@app.route('/')
def index():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    res = requests.get(url)
    data = res.json()
    return render_template('index.html', data=data)

@app.route('/mars')
def mars():
    try:
        photos = fetch_mars_gallery_photos()
        return render_template('mars.html', photos=photos, error_message=None)
    except requests.RequestException:
        return render_template(
            'mars.html',
            photos=[],
            error_message='Mars gallery is temporarily unavailable. Please try again later.'
        )

@app.route('/iss')
def iss():
    return render_template('iss.html')

if __name__ == '__main__':
    app.run(debug=True)


app = app #for vercel