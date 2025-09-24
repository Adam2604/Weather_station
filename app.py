from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

#Strona główna
@app.route("/")
def index():
    #łączenie z baza
    conn = sqlite3.connect("dane.db")
    cursor = conn.cursor()

    #pobieranie ostatnich 10 wpisów
    cursor.execute("SELECT czas, temat, wiadomosc FROM mqtt_dane ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    # HTML generowany w locie
    html = """
    <html>
    <head>
        <title>Dane MQTT</title>
    </head>
    <body>
        <h1>Ostatnie dane z MQTT</h1>
        <table border="1" cellpadding="5">
            <tr><th>Czas</th><th>Temat</th><th>Wiadomość</th></tr>
            {% for row in rows %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html, rows = rows)

if __name__ == "__main__":
    app.run(host="192.168.0.50", port = 5000, debug = True)