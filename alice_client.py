from flask import Flask, request, render_template_string
import requests
import base64

app = Flask(__name__)

# Fungsi Simulasi Enkripsi (Mengubah teks ke Base64)
def simple_encrypt(text):
    return base64.b64encode(text.encode()).decode()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Alice - Client</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background-color: #eef2f7; }
        .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        button { padding: 10px; cursor: pointer; border: none; border-radius: 5px; color: white; }
        .btn-normal { background-color: #f44336; }
        .btn-secure { background-color: #4CAF50; }
        input[type="text"] { width: 80%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👩 Alice's Device</h1>
        <p>Gunakan form ini untuk mengirim data ke Bob.</p>
        <form method="POST">
            <input type="text" name="message" placeholder="Ketik pesan atau password..." required>
            <br>
            <button type="submit" name="mode" value="normal" class="btn-normal">Kirim Biasa (Insecure)</button>
            <button type="submit" name="mode" value="secure" class="btn-secure">Kirim Terenkripsi (Secure)</button>
        </form>
        {% if status %}<p><strong>Status:</strong> {{ status }}</p>{% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    status = ""
    if request.method == 'POST':
        msg = request.form.get('message')
        mode = request.form.get('mode')
        
        display_msg = msg
        if mode == "secure":
            display_msg = f"ENCRYPTED_{simple_encrypt(msg)}"
        
        # Mengirim ke Eve (MITM) sebagai perantara
        try:
            requests.post('http://localhost:5002/intercept', json={"message": display_msg})
            status = f"Pesan '{display_msg}' terkirim ke jaringan!"
        except:
            status = "Error: Pastikan Eve (Port 5002) sudah dijalankan!"
            
    return render_template_string(HTML_TEMPLATE, status=status)

if __name__ == '__main__':
    app.run(port=5001)