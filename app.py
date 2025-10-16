from flask import Flask, render_template_string, Response
import sqlite3
import datetime
import io
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("mqtt_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, wilgotnosc, timestamp FROM pomiary ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

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
        <meta http-equiv="refresh" content="30">
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f5f5f5;
                flex-direction: column;
            }
            .card {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
                font-size: 28px;
                text-align: center;
                margin: 10px 0;
                width: 280px;
            }
            .value {
                font-weight: bold;
                color: #d9534f;
            }
            a {
                text-decoration: none;
                color: inherit;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <a href="/temperatura">Temperatura: <span class="value">{{ temperatura }}</span> °C</a>
        </div>
        <div class="card">
            Wilgotność: <span class="value">{{ wilgotnosc }}</span> %
        </div>
    </body>
    </html>
    """

    return render_template_string(html, temperatura=temperatura, wilgotnosc=wilgotnosc)


@app.route("/temperatura")
def temperatura_page():
    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")

    conn = sqlite3.connect("mqtt_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT temperatura, timestamp FROM pomiary WHERE date(timestamp)=? ORDER BY timestamp",
        (today,)
    )
    rows = cursor.fetchall()
    conn.close()

    # Zamień timestamp na ISO 8601 dla Chart.js
    labels = [row[1].replace(" ", "T") for row in rows]  # 'YYYY-MM-DD HH:MM:SS' -> 'YYYY-MM-DDTHH:MM:SS'
    values = [row[0] for row in rows]

    html = """
    <html>
    <head>
        <title>Wykres temperatury</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/luxon@3.3.0/build/global/luxon.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-luxon@1.3.1"></script>
    </head>
    <body style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
        <h2 style="margin-bottom: 10px;">Wykres temperatury z dzisiejszego dnia</h2>
        
        <!-- kontener dla wykresu -->
        <div style="width: 1000px; max-width: 90%; height: 300px; display:flex; justify-content:center;">
            <canvas id="chart"></canvas>
        </div>

        <a href="/" 
        style="margin-top: 20px; padding: 10px 20px; background-color: #007bff; color: white; border-radius: 6px; text-decoration: none;">
        Powrót
        </a>

        <script>
        const ctx = document.getElementById('chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ labels|safe }},
                datasets: [{
                    label: 'Temperatura (°C)',
                    data: {{ values|safe }},
                    borderColor: 'red',
                    backgroundColor: 'rgba(255,0,0,0.2)',
                    fill: true,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,  // pozwala na automatyczne skalowanie
                maintainAspectRatio: false,  // pozwala zmieniać proporcje
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour',
                            displayFormats: { hour: 'HH:mm' },
                            tooltipFormat: 'HH:mm'
                        },
                        adapters: {
                            date: { zone: 'Europe/Warsaw' }
                        },
                        title: { display: true, text: 'Czas' }
                    },
                    y: {
                        display: true,
                        title: { display: true, text: 'Temperatura (°C)' }
                    }
                }
            }
        });
        </script>
    </body>

    </html>
    """

    return render_template_string(html, labels=labels, values=values)



if __name__ == "__main__":
    app.run(host="192.168.34.15", port=5000, debug=True)


