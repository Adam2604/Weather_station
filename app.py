from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    # łączenie z bazą
    conn = sqlite3.connect("mqtt_data.db")
    cursor = conn.cursor()

    # pobieramy ostatnią wiadomość
    cursor.execute("SELECT payload, timestamp FROM pomiary ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    # jeżeli brak danych w bazie
    if row is None:
        temperatura = "brak danych"
    else:
        temperatura = row[0]

    html = """
    <html>
    <head>
        <title>Stacja pogodowa</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f5f5f5;
            }
            .card {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
                font-size: 32px;
                text-align: center;
            }
            .value {
                font-weight: bold;
                color: #d9534f;
            }
            .card {
                font-size: 32px; /* domyślnie na komputerze */
            }

            @media (max-width: 1081px) {
                .card {
                    font-size: 80px; /* większy napis na telefonach */
                    margin-top: -600px;
                }
            }

        </style>
    </head>
    <body>
        <div class="card">
            Temperatura: <span class="value">{{ temperatura }}</span> °C
        </div>
    </body>
    </html>
    """

    return render_template_string(html, temperatura=temperatura)

if __name__ == "__main__":
    app.run(host="192.168.0.50", port=5000, debug=True)

