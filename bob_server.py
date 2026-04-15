from flask import Flask, request, render_template_string
import base64

app = Flask(__name__)
received_logs = []

# Fungsi Simulasi Dekripsi (Mengembalikan Base64 ke Teks Asli)
def simple_decrypt(encoded_text):
    try:
        pure_code = encoded_text.replace("ENCRYPTED_", "")
        return base64.b64decode(pure_code).decode()
    except:
        return "Gagal Dekripsi"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bob - Server</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background-color: #f0f4f8; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #3f51b5; color: white; }
        .raw { color: #888; font-family: monospace; }
        .decrypted { font-weight: bold; color: #2e7d32; }
    </style>
</head>
<body>
    <h1>🏠 Bob's Database Server</h1>
    <table>
        <tr>
            <th>Data Masuk (Traffic)</th>
            <th>Pesan yang Dibaca Bob</th>
        </tr>
        {% for log in logs %}
        <tr>
            <td class="raw">{{ log.raw }}</td>
            <td class="decrypted">{{ log.decrypted }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/receive', methods=['POST'])
def receive():
    data = request.json.get('message')
    
    # Logika Dekripsi Otomatis
    if data.startswith("ENCRYPTED_"):
        decrypted_msg = simple_decrypt(data)
    else:
        decrypted_msg = data
        
    received_logs.append({"raw": data, "decrypted": decrypted_msg})
    return {"status": "success"}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, logs=received_logs)

if __name__ == '__main__':
    app.run(port=5000)