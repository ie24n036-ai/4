return f"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>医療用品在庫管理システム</title>

<style>

body{
    font-family: "Yu Gothic", sans-serif;
    background: linear-gradient(to right,#d7f0ff,#eef8ff);
    margin:0;
    padding:30px;
}

.container{
    max-width:1000px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0 5px 15px rgba(0,0,0,0.2);
}

h1{
    text-align:center;
    color:#0066aa;
}

h2{
    color:#0066aa;
}

table{
    width:100%;
    border-collapse:collapse;
}

th{
    background:#2196F3;
    color:white;
    padding:12px;
}

td{
    padding:10px;
    text-align:center;
}

tr:nth-child(even){
    background:#f5f5f5;
}

input{
    padding:5px;
    border-radius:5px;
    border:1px solid #aaa;
}

button{
    background:#2196F3;
    color:white;
    border:none;
    border-radius:6px;
    padding:8px 15px;
    cursor:pointer;
}

button:hover{
    background:#0b72c9;
}

.delete{
    background:#ff4d4d;
}

.delete:hover{
    background:#d50000;
}

.shortage{
    background:#fff3f3;
    border-left:8px solid red;
    padding:15px;
    border-radius:10px;
}

.addbox{
    background:#f0f9ff;
    padding:15px;
    border-radius:10px;
}

</style>

</head>

<body>

<div class="container">

<h1>🏥 医療用品在庫管理システム 💊</h1>

<div style="text-align:center;margin-bottom:20px;">
<img src="https://cdn-icons-png.flaticon.com/512/2966/2966483.png" width="120">
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

<h2>➕ 新しい商品を追加</h2>

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
