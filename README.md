## 環境構築
・seleniumとChromeDriverをインストールする．  
・ChromeDriverがある場所にPATHを通す．  
以下のサイト参考  
https://qiita.com/memakura/items/20a02161fa7e18d8a693

## 設定
src/scraping.py のexecutable_pathにChromeDriverのパスを書く  
#### 詳細設定
・text_process.pyのclean_wordに除去したい文字を設定する．    
・字幕は時間を置かないと取れない場合があり，scrayping.pyでのget_japanese_text, get_english_textでは一瞬だけ動画を流し，その間に字幕を取っている．取れなければforループによりもう一度同じことを行なっている．scrayping.pyの70行目，90行目にforループの回数をしているが，回数が多いほど確実に字幕が取れる一方，計算量が多くなりプログラムが停止しやすくなり，実行時間も長くなる．
また，scrayping.py 26行目でページ遷移した後，scrayping.py 267行目でchromeを閉じた後に何秒待つかを設定できる．実行するPCに応じてループ回数や待ち時間を設定する方が良いかもしれない(77行目，97行目のコメントアウトを外して何回目で字幕を取れたか確認できる)

## 実行
get_subtitle/src 上で以下のようにmain.pyを実行．  
$ python main.py [次に実行するURLのインデックス]  
get_subtitle/Data/URL_list.tsv のURLから順にスクレイピングが行われる． 
途中からでも実行できるようにmain.pyの後に次に実行するURLのインデックス(integer)を入力．  
数話進むと，プログラムが停止してしまう．プログラムを終了させ，途中まで進んだURLのインデックスを python main.py の後に入力し，再度実行．
