from flask import Flask, request, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)
intercepted_data = []

# Fungsi untuk mendapatkan timestamp saat ini
def get_time():
    return datetime.now().strftime("%H:%M:%S")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TERMINAL - EVE_MITM</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --hacker-green: #00ff41;
            --hacker-red: #ff3e3e;
            --bg-black: #0a0a0a;
            --terminal-gray: #1a1a1a;
        }

        body { 
            background-color: var(--bg-black); 
            color: var(--hacker-green); 
            font-family: 'Fira Code', monospace; 
            margin: 0;
            padding: 20px;
            overflow-x: hidden;
        }

        /* Efek Scanline (Garis-garis monitor lama) */
        body::before {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 2;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        .terminal-window {
            border: 1px solid #333;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
            padding: 20px;
            background: rgba(10, 10, 10, 0.9);
            min-height: 90vh;
        }

        .header {
            border-bottom: 1px solid var(--hacker-green);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .status-line { font-size: 0.8rem; margin-bottom: 5px; opacity: 0.8; }
        
        .log-entry {
            margin-bottom: 10px;
            line-height: 1.5;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .timestamp { color: #888; margin-right: 10px; }
        .tag-intercept { background: var(--hacker-red); color: white; padding: 0 5px; font-weight: bold; margin-right: 10px; }
        .payload { color: #fff; font-weight: bold; word-break: break-all; }
        .forward-msg { color: #008f11; font-size: 0.8rem; margin-left: 20px; }

        .cursor {
            display: inline-block;
            width: 10px;
            height: 1.2rem;
            background: var(--hacker-green);
            vertical-align: middle;
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0; }
        }

        .glitch {
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* Scrollbar ala Hacker */
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: #000; }
        ::-webkit-scrollbar-thumb { background: var(--hacker-green); }

    </style>
    <meta http-equiv="refresh" content="3">
</head>
<body>
    <div class="terminal-window">
        <div class="header">
            <div class="glitch">😈 EVE_MITM_SNIFFER v2.0.4</div>
            <div class="status-line">LISTENING ON PORT: 5002...</div>
            <div class="status-line">TARGET_IP: 127.0.0.1 (ALICE) -> 127.0.0.1 (BOB)</div>
            <div class="status-line">STATUS: <span style="color: var(--hacker-red)">SNIFFING_ACTIVE</span></div>
        </div>

        <div id="logs">
            <div class="log-entry">
                <span class="timestamp">[{{ start_time }}]</span>
                <span style="color: #666;">System initialization... Ready.</span>
            </div>

            {% for log in logs %}
            <div class="log-entry">
                <span class="timestamp">[{{ log.time }}]</span>
                <span class="tag-intercept">PACKET_SNIFFED</span>
                <span style="color: var(--hacker-green);">PAYLOAD:</span> 
                <span class="payload">"{{ log.data }}"</span>
                <div class="forward-msg">
                    <i class="fas fa-arrow-right"></i> Forwarding to 127.0.0.1:5000... <span style="color: var(--hacker-green);">[OK]</span>
                </div>
            </div>
            {% endfor %}
            
            <div class="log-entry">
                <span class="timestamp">[{{ current_time }}]</span>
                <span style="color: var(--hacker-green);">root@eve:~$</span> <span class="cursor"></span>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/intercept', methods=['POST'])
def intercept():
    data = request.json.get('message')
    
    # Simpan data dengan timestamp
    intercepted_data.insert(0, {
        "time": get_time(),
        "data": data
    })
    
    # Meneruskan data ke Bob (Forwarding)
    try:
        requests.post('http://localhost:5000/receive', json={"message": data}, timeout=1)
    except:
        pass
    
    return {"status": "success"}

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE, 
        logs=intercepted_data, 
        current_time=get_time(),
        start_time="00:00:01"
    )

if __name__ == '__main__':
    # Eve mendengarkan di port 5002
    app.run(port=5002)