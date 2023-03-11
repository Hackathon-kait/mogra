# mogra

ひつじさんのメモ
  
## よく使うコマンド  
  
git branch ：今いるブランチを見る  
  
git switch ブランチ名 ：指定したブランチに飛ぶ  
  
git switch -c ブランチ名 ：今いるブランチから新しくブランチをきる  
  
git pull　：developブランチに移動し作業前に使用し最新の情報を取り込む  
  
git rebase　ブランチ名　：作業ブランチに移動し基本developを指定して取り込む  
  git
  
## ブランチの命名規則 
  
developブランチから切り、「feature/#(イシュー番号)_わかりやすい名前」のブランチを作る。  
  
例：feature/#1_header  
  
※絶対日本語使わない  
  
## CSSについて
  
基本的に読み込むcssはstyle.cssだけでいい。  
  
cssを追加したいときはstyleフォルダにcssファイルを入れてstyle.cssにインポートする。  

基本のカラーを使用したいときは以下のclassを使う。  
  
class:  main  濃いオレンジ  
  sub   薄いオレンジ  

※複数のclassを使いたいときは1個目と2個目のclass名の間に半角スペース


これが見えればできている


環境構築の仕方

djangoのフォルダの中に「.env」ファイルを作成
中に
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=db
MYSQL_USER=db-user
MYSQL_PASSWORD=password

を記述し
mysqlのフォルダをコピーしてきて

docker-compose up -dを実行する
