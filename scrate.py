


from bs4 import BeautifulSoup
import requests #HTTP操作用
import time

# アクセスしたいWebサイトのURL
base_url = 'https://www.data.jma.go.jp/stats/etrn/view/10min_a1.php?prec_no=44&block_no=1002&year=2024&month=01&day=05&view=p1'

# Webサーバにリクエストを出す．レスポンスを変数に格納しておく
r = requests.get(base_url)

soup = BeautifulSoup(r.content, 'html.parser') # HTMLソースをBeautifulSoupオブジェクトに変換する（プログラムで扱いやすくするため）
print(type(soup))

import requests
from bs4 import BeautifulSoup
import time

# 対象のURLのベース部分
base_url = 'https://www.data.jma.go.jp/stats/etrn/view/10min_a1.php?prec_no=44&block_no=1002&year=2024&month=01&day='

# 対象の日付パターン
days = ['05', '06', '07', '08', '09']

# データを格納するリスト
data_list = []

# 各日付に対してデータを取得
for day in days:
    time.sleep(0.1)
    # ページの取得
    response = requests.get(base_url + day + '&view=p1')

    # HTMLの解析
    soup = BeautifulSoup(response.text, 'html.parser')

    # 対象となる<tr>タグを取得
    tr_tags = soup.select('tr[style="text-align:right;"]')

    # 各<tr>タグのデータを辞書に追加
    for tr_tag in tr_tags:
        td_tags = tr_tag.find_all('td')[:3]  # 1つ目から3つ目までの<td>タグ
        td_texts = [td.get_text(strip=True) for td in td_tags]
        date_str = '2024/01/' + day + '/' + td_texts[0]
        data_dict = {
            'thyme': date_str,
            'rain': td_texts[1],
            'tem': td_texts[2]
        }
        data_list.append(data_dict)

import sqlite3
path = '/Users/araiyuya/Desktop/onegai/'
db_name = 'scraping_data.sqlite'
# DBに接続する
con = sqlite3.connect(path + db_name)
# SQLを実行するためのオブジェクトを取得
cur = con.cursor()
# テーブルを削除するSQL文
sql_drop_table = 'DROP TABLE IF EXISTS scrape_data;'
# テーブルを削除
cur.execute(sql_drop_table)

path = '/Users/araiyuya/Desktop/onegai/'

# ローカル（自分のMac）
# path = '../db/'

# DBファイル名
db_name = 'scraping_data.sqlite'


# DBに接続する（指定したDBファイル存在しない場合は，新規に作成される）
con = sqlite3.connect(path + db_name)


# print(type(con))

# 2．SQLを実行するためのオブジェクトを取得
cur = con.cursor()

# 3．実行したいSQLを用意する
# テーブルを作成するSQL
# CREATE TABLE テーブル名（カラム名 型，...）;
sql_create_table = 'CREATE TABLE scrape_data (thyme text, rain int, tem int);'

# 4．SQLを実行する
cur.execute(sql_create_table)

# 5．必要があればコミットする（データ変更等があった場合）
# 今回は必要なし




# 2．SQLを実行するためのオブジェクトを取得
cur = con.cursor()

# データを挿入するSQL
sql_insert_data = 'INSERT INTO scrape_data (thyme, rain, tem) VALUES (?, ?, ?);'

# 各辞書型データをデータベースに挿入
for data_dict in data_list:
    cur.execute(sql_insert_data, (data_dict['thyme'], data_dict['rain'], data_dict['tem']))

# コミットする
con.commit()

# DBへの接続を閉じる
con.close()