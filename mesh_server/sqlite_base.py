import sqlite3
import csv

#test.dbを作成し、接続（すでに存在する場合は接続のみ）
con = sqlite3.connect("test.db")
cur = con.cursor()

#testテーブルを作成（IF NOT EXISTSは「存在しなければ作成する」という意味）
create_test = "CREATE TABLE IF NOT EXISTS test (id INTEGER, name TEXT, height INTEGER, weight INTEGER)"
cur.execute(create_test)

#testテーブルのデータを削除（何回もコード実行すると同じデータ追加されるので）
delete_test = "DELETE FROM TEST"
cur.execute(delete_test)

#csvファイルの指定
open_csv = open("sensor_data.csv")

#csvファイルを読み込む
read_csv = csv.reader(open_csv)

#next()関数を用いて最初の行(列名)はスキップさせる
next_row = next(read_csv)

#csvデータをINSERTする
rows = []
for row in read_csv:
    rows.append(row)

#executemany()で複数のINSERTを実行する
cur.executemany(
    "INSERT INTO test (id, name, height) VALUES (?, ?, ?)", rows)

#テーブルの変更内容保存
#csvも閉じておきましょう
con.commit()
open_csv.close()

#testテーブルの確認
select_test = "SELECT * FROM test"

print("----------------------------")
print("fetchall")
print("----------------------------")
print(cur.execute(select_test))
print(cur.fetchall())
print("----------------------------")
print("for文")
print("----------------------------")
for i in cur.execute(select_test):
    print(i)

#データベースの接続終了
con.close