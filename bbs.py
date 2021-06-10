#!/usr/bin/env python3
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

# MySQLデータベース接続用ライブラリ
import MySQLdb
con = None
cur = None
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

# CGIで実行した際のフォーム情報を取り出すライブラリ
import cgi
form_data = cgi.FieldStorage(keep_blank_values = True)

import os
from pathlib import Path
env_path = Path('.') / '.env'
from dotenv import load_dotenv
load_dotenv(dotenv_path = env_path, verbose = True)

# トップ画面のHTMLを出力する関数
def print_html():

	# html 開始
	print('<DOCTYPE html>')
	print('<html>')
	
	# head 出力
	print('<head>')
	print('<meta charset="UTF-8">')
	print('</head>')

	#body 開始
	print('<body>')
	print('<p>ひと言掲示板</p>')

	# 書き込みフォーム出力
	print( '<form action="" method="POST">' )
	print( '<input type="hidden" name="method_type" value="tweet">' )
	print( '<input type="text" name="poster_name" value="" placeholder="なまえ">' )
	print( '<br>' )
	print( '<textarea name="body_text" value="" placeholder="本文"></textarea>' )
	print( '<input type="submit" value="投稿">' )
	print( '</form>' )

	# 罫線を出力
	print('<hr>')
	# フォーム経由のアクセスならフォームの内容を表示
#	if( 'method_type' in form_data ):
#		print( "form_data[ 'method_type' ]: " + form_data[ 'method_type' ].value + '<br>')
#		print( "form_data[ 'poster_name' ]: " + form_data[ 'poster_name' ].value + '<br>')
#		print( "form_data[ 'body_text' ]: " + form_data[ 'body_text' ].value + '<br>')
#
	#書き込みの一覧を取得するSQL文を作成
	sql = "select * from posts"

#	# SQLを実行
	cur.execute( sql )
#	
#	# 取得した書き込みの一覧の全レコードを取り出し
	rows = cur.fetchall()
#
	# 全レコードから1レコードずつ取り出すループ処理
	for row in rows:
		print('<div class="meta">')
		print('<span class="id">' + str(row[ 'id' ]) + '</span>')
		print('<span class="name">' + str(row[ 'name' ]) + '</span>')
		print('<span class="date">' + str(row[ 'created_at' ]) + '</span>')
		print('</div>')
		print('<div class="message"><span>' + str(row[ 'body' ]) + '</span></div>')

	# body閉じ
	print('</body>')

	# html閉じ
	print('</html>')
 	
# フォーム経由のアクセス処理関数
def proceed_methods():
	# フォームの種類を取得(現在は書き込みのみ)
	method = form_data[ 'method_type' ].value

	# tweet (書き込み) ならば
	if( method == 'tweet' ):
		# 名前を取り出し
		poster_name = form_data[ 'poster_name' ].value
		# 投稿内容を取り出し
		body_text = form_data[ 'body_text' ].value
		
		# 投稿をデータベースに書き込むSQL文を作成
		sql = 'insert into posts ( name, body ) values ( %s, %s)'
		# 取り出した名前と投稿内容をセットしてSQLを実行
		cur.execute( sql, ( poster_name, body_text))
		con.commit()

	print('<!DOCTYPE html>')
	print('<html>')
	print('<head>')
	print('<meta http-equiv="refresh" content="5; url=./bbs.py">')
	print('</head>')
	print('<body>')
	print('処理が成功しました。5秒後に元のページに戻ります。')
	print('</body>')
	print('</html>')

# メイン処理実行関数
def main():
	# CGI実行のおまじない
	print('Content-Type: text/html; charset=utf-8' )
	print('')

	# ここでデータベースに接続しておく
	global con, cur
	try:
		con = MySQLdb.connect(
		      host = os.environ.get('bbs_db_host'),
		      user = str(os.environ.get('bbs_db_user')),
	       	      passwd = str(os.environ.get('bbs_db_pass')),
	       	      db = str(os.environ.get('bbs_db_name')),
	       	      use_unicode = True,
	       	      charset = 'utf8'
		)
		
	except MySQLdb.Error as e:
		print('データベース接続に失敗しました。')
		print( e )
		# データベースに接続できない場合はここで処理終了。
		exit()

	cur = con.cursor( MySQLdb.cursors.DictCursor )

#	# フォーム経由のアクセスかを判定
	if( 'method_type' in form_data ):
#		#フォーム経由のアクセスの場合。フォームの種類に従い処理実行
		proceed_methods()
	else:
#		# フォーム経由のアクセスでない場合、通常のトップ画面を表示
		print_html()

	#一通り処理が完了したら最後にデータベースを切断
	cur.close()
	con.close()

# Pythonスクリプトで実行された場合の処理を記述
if __name__ == "__main__":
	# main() を実行
	main()



#CREATE DATABASE IF NOT EXISTS `bbs` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
#
#USE bbs;
#
#CREATE TABLE IF NOT EXISTS `posts`(
#	`id` int unsigned NOT NULL AUTO_INCREMENT,
#	`name` varchar(255) NOT NULL,
#	`body` varchar(255) NOT NULL,
#	`created_at` datetime DEFAULT CURRENT_TIMESTAMP,
#	PRIMARY KEY (`id`)
#) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


