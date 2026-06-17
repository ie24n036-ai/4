from flask import Flask, render_template_string
import pymysql

app = Flask(__name__)

@app.route("/")
def index():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="あなたのパスワード",
        database="medical_inventory"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    html = """
    <h1>医療用品在庫管理システム</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>商品名</th>
            <th>在庫数</th>
            <th>発注点</th>
            <th>価格</th>
        </tr>
        {% for p in products %}
        <tr>
            <td>{{ p[0] }}</td>
            <td>{{ p[1] }}</td>
            <td>{{ p[2] }}</td>
            <td>{{ p[3] }}</td>
            <td>{{ p[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, products=products)

if __name__ == "__main__":
    app.run(debug=True)
