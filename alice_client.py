from flask import Flask, request, render_template_string
import requests
import base64

app = Flask(__name__)

# Fungsi Simulasi Enkripsi (Mengubah teks ke Base64)
def simple_encrypt(text):
    return base64.b64encode(text.encode()).decode()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alice - Secure Terminal</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <!-- Font Awesome untuk Ikon -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #6366f1;
            --danger: #ef4444;
            --success: #10b981;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
        }

        body { 
            font-family: 'Inter', sans-serif; 
            background-color: var(--bg); 
            color: var(--text);
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container { 
            background: var(--card); 
            width: 100%;
            max-width: 450px;
            padding: 2rem; 
            border-radius: 1.5rem; 
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1);
        }

        .header { text-align: center; margin-bottom: 2rem; }
        .header i { font-size: 3rem; color: var(--primary); margin-bottom: 1rem; }
        .header h1 { margin: 0; font-size: 1.5rem; font-weight: 600; }
        .header p { color: #64748b; font-size: 0.9rem; margin-top: 0.5rem; }

        .input-group { margin-bottom: 1.5rem; }
        label { display: block; margin-bottom: 0.5rem; font-weight: 500; font-size: 0.9rem; }
        
        input[type="text"] { 
            width: 100%; 
            padding: 0.75rem 1rem; 
            border-radius: 0.75rem; 
            border: 1px solid #e2e8f0; 
            box-sizing: border-box;
            font-size: 1rem;
            transition: all 0.2s;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .button-stack { display: flex; flex-direction: column; gap: 0.75rem; }
        
        button { 
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.75rem; 
            cursor: pointer; 
            border: none; 
            border-radius: 0.75rem; 
            color: white; 
            font-weight: 500;
            font-size: 0.95rem;
            transition: transform 0.1s, opacity 0.2s;
        }

        button:active { transform: scale(0.98); }

        .btn-normal { background-color: var(--danger); }
        .btn-secure { background-color: var(--success); }
        
        .status-box {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 0.75rem;
            font-size: 0.85rem;
            line-height: 1.4;
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
        }

        .status-success { background-color: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
        .status-error { background-color: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }

        .footer-note {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.75rem;
            color: #94a3b8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <i class="fas fa-user-shield"></i>
            <h1>Alice's Device</h1>
            <p>Kirim pesan aman ke Bob melalui jaringan</p>
        </div>

        <form method="POST">
            <div class="input-group">
                <label for="message">Pesan Rahasia</label>
                <input type="text" id="message" name="message" placeholder="Masukkan pesan atau password..." required autocomplete="off">
            </div>

            <div class="button-stack">
                <button type="submit" name="mode" value="secure" class="btn-secure">
                    <i class="fas fa-lock"></i> Kirim Terenkripsi
                </button>
                <button type="submit" name="mode" value="normal" class="btn-normal">
                    <i class="fas fa-unlock"></i> Kirim Tanpa Enkripsi
                </button>
            </div>
        </form>

        {% if status %}
            <div class="status-box {% if 'Error' in status %}status-error{% else %}status-success{% endif %}">
                <i class="fas {% if 'Error' in status %}fa-exclamation-circle{% else %}fa-paper-plane{% endif %}"></i>
                <span>{{ status }}</span>
            </div>
        {% endif %}

        <div class="footer-note">
            Node: <strong>Alice (Port 5001)</strong> | Target: <strong>Eve (Port 5002)</strong>
        </div>
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
        is_secure = False
        if mode == "secure":
            display_msg = f"ENCRYPTED_{simple_encrypt(msg)}"
            is_secure = True
        
        try:
            # Simulasi pengiriman ke Eve (MITM)
            requests.post('http://localhost:5002/intercept', json={"message": display_msg}, timeout=2)
            status = f"Berhasil! Pesan {'(Terenkripsi)' if is_secure else '(Polos)'} telah dilepas ke jaringan."
        except requests.exceptions.ConnectionError:
            status = "Error: Node 'Eve' (Port 5002) tidak aktif. Pesan gagal dikirim."
        except Exception as e:
            status = f"Error: {str(e)}"
            
    return render_template_string(HTML_TEMPLATE, status=status)

if __name__ == '__main__':
    app.run(port=5001, debug=True)