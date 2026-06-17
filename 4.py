from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h1>医療用品在庫管理システム</h1>

    <table border="1">
        <tr>
            <th>商品名</th>
            <th>在庫数</th>
            <th>発注点</th>
        </tr>
        <tr>
            <td>マスク</td>
            <td>100</td>
            <td>20</td>
        </tr>
        <tr>
            <td>消毒液</td>
            <td>50</td>
            <td>10</td>
        </tr>
        <tr>
            <td>体温計</td>
            <td>3</td>
            <td>5</td>
        </tr>
    </table>

    <h2>⚠ 在庫不足商品</h2>
    <p>体温計（在庫3、発注点5）</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
