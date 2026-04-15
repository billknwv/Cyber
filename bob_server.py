from flask import Flask, request, render_template_string
import base64

app = Flask(__name__)
received_logs = []

# Fungsi Simulasi Dekripsi
def simple_decrypt(encoded_text):
    try:
        pure_code = encoded_text.replace("ENCRYPTED_", "")
        return base64.b64decode(pure_code).decode()
    except:
        return "[Gagal Dekripsi: Data Korup]"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bob - Secure Server Receiver</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #4f46e5;
            --success: #10b981;
            --bg: #f1f5f9;
            --card: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }

        body { 
            font-family: 'Inter', sans-serif; 
            background-color: var(--bg); 
            color: var(--text-main);
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
        }

        .dashboard {
            width: 100%;
            max-width: 900px;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }

        .header h1 { 
            margin: 0; 
            font-size: 1.5rem; 
            display: flex; 
            align-items: center; 
            gap: 10px;
        }

        .status-badge {
            background: #dcfce7;
            color: #166534;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .card {
            background: var(--card);
            border-radius: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            border: 1px solid var(--border);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th {
            background: #f8fafc;
            padding: 1rem;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border);
        }

        td {
            padding: 1rem;
            border-bottom: 1px solid var(--border);
            vertical-align: top;
        }

        .raw-data {
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            color: #6366f1;
            background: #f5f3ff;
            padding: 4px 8px;
            border-radius: 4px;
            word-break: break-all;
        }

        .decrypted-msg {
            font-weight: 500;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tag {
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
        }
        .tag-secure { background: #e0f2fe; color: #0369a1; }
        .tag-plain { background: #fef3c7; color: #92400e; }

        .empty-state {
            padding: 4rem;
            text-align: center;
            color: var(--text-muted);
        }

        .refresh-btn {
            background: white;
            border: 1px solid var(--border);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }
        .refresh-btn:hover { background: #f8fafc; }
    </style>
    <!-- Auto Refresh setiap 5 detik untuk memantau trafik baru -->
    <meta http-equiv="refresh" content="5">
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1><i class="fas fa-server" style="color: var(--primary)"></i> Bob's Database Server</h1>
            <div style="display: flex; gap: 10px; align-items: center;">
                <div class="status-badge">
                    <span style="width: 8px; height: 8px; background: #22c55e; border-radius: 50%"></span>
                    Server Online
                </div>
                <button onclick="window.location.reload()" class="refresh-btn">
                    <i class="fas fa-sync-alt"></i> Refresh
                </button>
            </div>
        </div>

        <div class="card">
            <table>
                <thead>
                    <tr>
                        <th width="45%">Traffic Masuk (Raw Data)</th>
                        <th width="55%">Pesan Terinterpretasi</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td>
                            <div class="raw-data">{{ log.raw }}</div>
                        </td>
                        <td>
                            <div class="decrypted-msg">
                                {% if "ENCRYPTED_" in log.raw %}
                                    <span class="tag tag-secure"><i class="fas fa-lock"></i> SECURE</span>
                                {% else %}
                                    <span class="tag tag-plain"><i class="fas fa-unlock"></i> PLAIN</span>
                                {% endif %}
                                {{ log.decrypted }}
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            {% if not logs %}
            <div class="empty-state">
                <i class="fas fa-inbox fa-3x" style="margin-bottom: 1rem; opacity: 0.3"></i>
                <p>Belum ada trafik data yang masuk...</p>
            </div>
            {% endif %}
        </div>
        
        <p style="text-align: center; font-size: 0.8rem; color: var(--text-muted); margin-top: 1.5rem;">
            Endpoint: <code style="background: #e2e8f0; padding: 2px 5px; border-radius: 4px;">POST /receive</code> | Listening on Port 5000
        </p>
    </div>
</body>
</html>
'''

@app.route('/receive', methods=['POST'])
def receive():
    data = request.json.get('message')
    if not data:
        return {"status": "error", "message": "No data"}, 400
    
    # Logika Dekripsi Otomatis
    if data.startswith("ENCRYPTED_"):
        decrypted_msg = simple_decrypt(data)
    else:
        decrypted_msg = data
        
    # Tambahkan ke log (di posisi paling atas agar yang terbaru muncul pertama)
    received_logs.insert(0, {"raw": data, "decrypted": decrypted_msg})
    return {"status": "success"}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, logs=received_logs)

if __name__ == '__main__':
    app.run(port=5000)