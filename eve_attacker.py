from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
intercepted_data = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Eve - MITM Attacker</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #1a1a1a; color: #00ff00; margin: 40px; }
        .terminal { background: #000; padding: 20px; border: 2px solid #333; border-radius: 5px; }
        .captured { color: #ff5555; border-bottom: 1px solid #333; padding: 5px 0; }
    </style>
</head>
<body>
    <div class="terminal">
        <h1>😈 Eve's Interceptor (Sniffer Log)</h1>
        <p>Mendengarkan lalu lintas data di jaringan...</p>
        <hr>
        {% for data in logs %}
        <div class="captured">
            [DATA CAPTURED]: {{ data }}
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route('/intercept', methods=['POST'])
def intercept():
    data = request.json.get('message')
    intercepted_data.append(data) # Mencuri data
    
    # Meneruskan data ke Bob (Forwarding)
    try:
        requests.post('http://localhost:5000/receive', json={"message": data})
    except:
        pass
    
    return {"status": "success"}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, logs=intercepted_data)

if __name__ == '__main__':
    app.run(port=5002)