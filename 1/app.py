from flask import Flask, request, jsonify
import requests
import concurrent.futures

app = Flask(__name__)

def fetch_numbers_from_url(url):
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
        data = response.json()
        return data.get("numbers", [])
    except (requests.exceptions.RequestException, ValueError):
        return []

@app.route('/numbers', methods=['GET'])
def fetch_and_merge_numbers():
    urls = request.args.getlist('ur')

    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    merged_numbers = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
        results = list(executor.map(fetch_numbers_from_url, urls))

    for numbers in results:
        merged_numbers.extend(numbers)

    merged_numbers = sorted(list(set(merged_numbers)))

    return jsonify({"numbers": merged_numbers}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
