from flask import Flask

app = Flask(__name__)

@app.route('/lucky-otter-15', methods=['GET'])
def lucky_otter():
    return {"status": "Application is running"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
   