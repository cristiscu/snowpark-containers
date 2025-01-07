# see https://quickstarts.snowflake.com/guide/intro_to_snowpark_container_services_with_python_api/index.html?index=..%2F..index#4
# see https://github.com/Snowflake-Labs/sfguide-intro-to-snowpark-container-services/tree/main/src/convert-api

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():

    data = request.get_json()
    if 'data' not in data:
        return jsonify({'error': 'Missing data key in request'}), 400

    data_out = []
    for item in data['data']:
        if not isinstance(item, list) or len(item) < 2:
            return jsonify({'error': 'Invalid data format'}), 400
        celsius = item[1]
        fahrenheit = celsius * 9./5 + 32
        data_out.append([item[0], fahrenheit])
    return jsonify({'data': data_out})

if __name__ == '__main__':
    app.run(debug=True)