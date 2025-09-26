from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    # łączenie z bazą
    conn = sqlite3.connect("mqtt_data.db")
    cursor = conn.cursor()

    # pobieramy ostatnią wiadomość
    cursor.execute("SELECT temperatura, wilgotnosc, timestamp FROM pomiary ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    # jeżeli brak danych w bazie
    if row is None:
        temperatura = "brak danych"
        wilgotnosc = "brak danych"
    else:
        temperatura = row[0]
        wilgotnosc = row[1]

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
                flex-direction: column; /* ustawiamy kolumnę, żeby karty były jedna pod drugą */
            }
            .card {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
                font-size: 28px;
                text-align: center;
                margin: 10px 0; /* odstęp między kartami */
                width: 280px; /* opcjonalnie, aby karty były równej szerokości */
            }
            .value {
                font-weight: bold;
                color: #d9534f;
            }
        </style>
    </head>
    <body>
        <div class="card">
            Temperatura: <span class="value">{{ temperatura }}</span> °C
        </div>
        <div class="card">
            Wilgotność: <span class="value">{{ wilgotnosc }}</span> %
        </div>
    </body>
    </html>
    """

    return render_template_string(html, temperatura=temperatura, wilgotnosc=wilgotnosc)

if __name__ == "__main__":
    app.run(host="192.168.0.50", port=5000, debug=True)

