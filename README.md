# 異常検出器プログラム
機械に設置されたモジュールからの送信データをローカル、またはgoogle spreasheetに保存する．ローカルはdataディレクトリにモジュールのid名のファイルで保存される．google spreasheetはworksheetにid名ごとにシートを作成し、保存される. 
## requirements
```
$ sudo pip install pandas digi-xbee gspread oauth2client 
```

## 実行
```
$ cd mesh_server
$ python3 server.py
```

## 調整可能なパラメータ
```python:server.py
[...]
# ------------------  settings -------------------

# save data on local
local_save = True
local_csv_path = 'data/'

# Path for Google Docs oauth file
GDOCS_OAUTH_JSON       = 'dht22_spread/propane-net-346716-96d30a3aef97.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'database'

# -------------------------------------------------
[...]
```
mesh_server/sever.pyの上部にあるパラメータを設定することが可能。
- ```local_save``` 取得したデータをローカルに保存するフラグ
- ```local_csv_path``` ローカルで保存するディレクトリ
- ```GDOCS_OAUTH_JSON``` Google Docs oauth fileのパス
- ```GDOCS_SPREADSHEET_NAME``` 保存するspreadsheetのファイル名