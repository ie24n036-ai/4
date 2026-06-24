from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# 在庫データをPythonのディクショナリで管理
inventory = {
    "マスク": {"stock": 100, "threshold": 20},
    "消毒液": {"stock": 50, "threshold": 10},
    "体温計": {"stock": 3, "threshold": 5}
}

@app.route("/", methods=["GET", "POST"])
def index():
    # 【更新処理】ボタンが押されてデータが送られてきた場合（POST）
    if request.method == "POST":
        for item_name in inventory.keys():
            # フォームから新しい「在庫数」を取得して更新
            new_stock = request.form.get(f"stock_{item_name}")
            if new_stock is not None:
                inventory[item_name]["stock"] = int(new_stock)
            
            # フォームから新しい「発注点」を取得して更新（★追加）
            new_threshold = request.form.get(f"threshold_{item_name}")
            if new_threshold is not None:
                inventory[item_name]["threshold"] = int(new_threshold)
        
        # 更新が終わったら、ページをリロード（再表示）する
        return redirect(url_for("index"))

    # 【表示処理】通常のページアクセスの場合（GET）
    table_rows = ""
    shortage_items = ""

    for item_name, data in inventory.items():
        stock = data["stock"]
        threshold = data["threshold"]

        # 「在庫数」と「発注点」の両方を入力フォーム（input）にする（★修正）
        table_rows += f"""
        <tr>
            <td>{item_name}</td>
            <td>
                <input type="number" name="stock_{item_name}" value="{stock}" min="0" style="width: 60px;">
            </td>
            <td>
                <input type="number" name="threshold_{item_name}" value="{threshold}" min="0" style="width: 60px;">
            </td>
        </tr>
        """

        # 在庫が発注点を下回っているか自動判定
        if stock < threshold:
            shortage_items += f"<p>{item_name}（在庫{stock}、発注点{threshold}）</p>"

    # 不足商品がない場合のメッセージ
    if not shortage_items:
        shortage_items = "<p>現在、在庫不足の商品はありません。</p>"

    # 画面全体のHTML
    return f"""
    <h1>医療用品在庫管理システム</h1>

    <form method="POST">
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr>
                <th>商品名</th>
                <th>在庫数</th>
                <th>発注点</th>
            </tr>
            {table_rows}
        </table>
        <br>
        <button type="submit" style="padding: 5px 15px; font-weight: bold;">データを更新する</button>
    </form>

    <h2>⚠ 在庫不足商品</h2>
    {shortage_items}
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
