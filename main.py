from flask import Flask, jsonify, request
import asyncio
from pyppeteer import launch
import concurrent.futures
import requests
import re
import json

app = Flask(__name__)

def fetch_and_filter_movies(search_url, search_text):
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        movies_data = response.json()
        filtered_movies = [movie for movie in movies_data if search_text.lower() in movie.get('title', '').lower()]
        return filtered_movies
    except requests.RequestException as e:
        return {"error": f"Error fetching data: {e}"}

@app.route('/search', methods=['GET'])
def search_movies():
    search_text = request.args.get('query')
    if not search_text:
        return jsonify({"error": "No search text provided"}), 400
    search_url = "https://raw.githubusercontent.com/junioralive/spymovies/main/src/spymovies_data_v2.json"
    matching_movies = fetch_and_filter_movies(search_url, search_text)
    return jsonify(matching_movies)

def fetch_and_format_episode_info(glink):
    purl = glink.replace("https://rentry.org/", "").replace("https://rentry.co/", "")
    response = requests.get(f'https://rentry.org/api/raw/{purl}')
    streaminglinks = response.json()['content']
    formatdata = streaminglinks.replace("HubCloud [Instant DL]", "").replace("🔗 ", "").strip("\n")
    formatted_text = '\n'.join([line for line in formatdata.split('\n') if line.strip()])
    pattern = r"(.+)\s+(\bhttps://hubcloud\.lol/video/\w+\b)"
    matches = re.findall(pattern, formatted_text)
    matches_dict = {match[0].strip(): match[1] for match in matches}
    return json.dumps(matches_dict, indent=2)

@app.route('/fetch', methods=['GET'])
def api_fetch_episode_info():
    glink = request.args.get('url')
    if not glink:
        return jsonify({"error": "No glink provided"}), 400

    try:
        episode_info_json = fetch_and_format_episode_info(glink)
        return jsonify(json.loads(episode_info_json))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
async def scrape(url):
    try:
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)
        await page.waitForSelector('a.btn.btn-primary', {'visible': True})
        await page.click('a.btn.btn-primary')
        await page.waitForSelector('a.btn.btn-success.btn-lg.h6', {'visible': True, 'timeout': 10000})
        success_button = await page.querySelector('a.btn.btn-success.btn-lg.h6')
        href = await page.evaluate('(element) => element.getAttribute("href")', success_button)
        await browser.close()
        return {"success": True, "stream": href}
    except Exception as e:
        return {"success": False, "error": str(e)}

def run_scrape(url):
    return asyncio.get_event_loop().run_until_complete(scrape(url))

@app.route('/scrape', methods=['GET'])
def scrape_endpoint():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future = executor.submit(run_scrape, url)
        result = future.result()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, port=os.getenv("PORT", default=5000))
