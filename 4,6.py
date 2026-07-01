from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# 在庫データをPythonのディクショナリで管理
inventory = {
    "1": {"name": "マスク", "stock": 100, "threshold": 20},
    "2": {"name": "消毒液", "stock": 50, "threshold": 10},
    "3": {"name": "体温計", "stock": 3, "threshold": 5}
}
# 次に追加する商品のIDを管理するためのカウンター
next_id = 4

@app.route("/", methods=["GET", "POST"])
def index():
    global next_id
    
    # 【各種処理】ボタンが押されてデータが送られてきた場合（POST）
    if request.method == "POST":
        action = request.form.get("action")
        
        # 1. 通常の更新（変更）処理
        if action == "update":
            new_inventory = {}
            for key in list(inventory.keys()):
                # 削除ボタンが押された行はスキップ
                if request.form.get(f"delete_{key}"):
                    continue
                
                name = request.form.get(f"name_{key}")
                stock = int(request.form.get(f"stock_{key}", 0))
                threshold = int(request.form.get(f"threshold_{key}", 0))
                
                # ★★★ 修正箇所：在庫数が発注点より多かった場合、発注点分を引く ★★★
                if stock > threshold:
                    stock = stock - threshold
                
                if name:
                    new_inventory[key] = {
                        "name": name,
                        "stock": stock,
                        "threshold": threshold
                    }
            inventory.clear()
            inventory.update(new_inventory)
            
        # 2. 新しい商品の追加処理
        elif action == "add":
            add_name = request.form.get("add_name")
            add_stock = int(request.form.get("add_stock", 0))
            add_threshold = int(request.form.get("add_threshold", 0))
            
            # ★★★ 修正箇所：追加時も在庫数が発注点より多かった場合、発注点分を引く ★★★
            if add_stock > add_threshold:
                add_stock = add_stock - add_threshold
            
            if add_name:
                inventory[str(next_id)] = {
                    "name": add_name,
                    "stock": add_stock,
                    "threshold": add_threshold
                }
                next_id += 1
                
        # 処理が終わったら、ページをリロード（再表示）する
        return redirect(url_for("index"))

    # 【表示処理】通常のページアクセスの場合（GET）
    table_rows = ""
    shortage_items = ""

    for key, data in inventory.items():
        name = data["name"]
        stock = data["stock"]
        threshold = data["threshold"]

        # 「商品名」「在庫数」「発注点」のすべてを入力フォームにする
        table_rows += f"""
        <tr>
            <td>
                <input type="text" name="name_{key}" value="{name}" style="width: 120px;" required>
            </td>
            <td>
                <input type="number" name="stock_{key}" value="{stock}" min="0" style="width: 60px;">
            </td>
            <td>
                <input type="number" name="threshold_{key}" value="{threshold}" min="0" style="width: 60px;">
            </td>
            <td>
                <button type="submit" name="delete_{key}" value="1" style="color: red; padding: 2px 5px;">削除</button>
            </td>
        </tr>
        """

        # 前回の修正：発注点を下回っている、または在庫が10個未満の場合に忠告を表示
        if stock < threshold or stock < 10:
            reasons = []
            if stock < threshold:
                reasons.append(f"発注点{threshold}未満")
            if stock < 10:
                reasons.append("在庫10個未満")
                
            reason_str = "・".join(reasons)
            shortage_items += f"<p>⚠️ <strong>{name}</strong>（現在庫: {stock}個 / 理由: {reason_str}）</p>"

    # 不足商品がない場合のメッセージ
    if not shortage_items:
        shortage_items = "<p>現在、在庫不足の商品はありません。</p>"

    # 画面全体のHTML
        # 画面全体のHTML
    return f"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>医療用品在庫管理システム</title>

<style>
body {{
    font-family: "Yu Gothic", sans-serif;
    background: linear-gradient(to right,#d7f0ff,#eef8ff);
    margin:0;
    padding:30px;
}}

.container {{
    max-width:1000px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0 5px 15px rgba(0,0,0,0.2);
}}

h1 {{
    text-align:center;
    color:#0066aa;
}}

h2 {{
    color:#0066aa;
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th {{
    background:#2196F3;
    color:white;
    padding:12px;
}}

td {{
    padding:10px;
    text-align:center;
}}

tr:nth-child(even) {{
    background:#f5f5f5;
}}

input {{
    padding:5px;
    border-radius:5px;
    border:1px solid #aaa;
}}

button {{
    background:#2196F3;
    color:white;
    border:none;
    border-radius:6px;
    padding:8px 15px;
    cursor:pointer;
}}

button:hover {{
    background:#0b72c9;
}}

.shortage {{
    background:#fff3f3;
    border-left:8px solid red;
    padding:15px;
    border-radius:10px;
}}

.addbox {{
    background:#f0f9ff;
    padding:15px;
    border-radius:10px;
}}
</style>

</head>

<body>

<div class="container">

<h1>🏥 医療用品在庫管理システム 💊</h1>

<div style="text-align:center;">
<img src="https://cdn-icons-png.flaticon.com/512/2785/2785544.png" width="100">
</div>

<form method="POST">
<input type="hidden" name="action" value="update">

<table border="1">
<tr>
<th>商品名</th>
<th>在庫数</th>
<th>発注点</th>
<th>操作</th>
</tr>

{table_rows}

</table>

<br>

<button type="submit">
💾 データを更新する
</button>

</form>

<hr>

<h2>➕ 新しい商品を追加する</h2>

<div class="addbox">

<form method="POST">

<input type="hidden" name="action" value="add">

商品名：
<input type="text" name="add_name" required>

在庫数：
<input type="number" name="add_stock" value="0">

発注点：
<input type="number" name="add_threshold" value="0">

<button type="submit">
追加
</button>

</form>

</div>

<h2>⚠ 在庫不足商品</h2>

<div class="shortage">

{shortage_items}

</div>

</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
