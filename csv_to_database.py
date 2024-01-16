import sqlite3


path = '/Users/araiyuya/Desktop/onegai/'

# ローカル（自分のMac）
# path = '../db/'

# DBファイル名
db_name = 'aircon.sqlite'

# DBに接続する（指定したDBファイル存在しない場合は，新規に作成される）
con = sqlite3.connect(path + db_name)


# 2．SQLを実行するためのオブジェクトを取得
cur = con.cursor()
# テーブルを削除するSQL文
sql_drop_table = 'DROP TABLE IF EXISTS aircon;'
# テーブルを削除
cur.execute(sql_drop_table)
# 3．実行したいSQLを用意する
# テーブルを作成するSQL
# CREATE TABLE テーブル名（カラム名 型，...）;
sql_create_table = 'CREATE TABLE aircon (thyme text, ON_OFF text);'

# 4．SQLを実行する
cur.execute(sql_create_table)

import csv
import sqlite3
# SQLiteデータベースに接続


# CSVファイルの読み込みとデータベースへの挿入
with open('//Users/araiyuya/Desktop/onegai/aircon.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # ヘッダー行がある場合、読み飛ばす
    next(csv_reader)
    for row in csv_reader:
        cur.execute('''
            INSERT INTO aircon (thyme, ON_OFF)
            VALUES (?, ?)
        ''', (row[0], row[1]))
# コミットとクローズ
con.commit()
con.close()