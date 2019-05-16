# migrate-exblog
エキサイトブログから他のブログへ引っ越しするスクリプト。エキサイトブログにあるコンテンツをmovable type形式で出力します。
## 概要
エキサイトブログにはエクスポート機能がないのでスクレイピングしてmovable type(MT)形式で出力します。(FC2を使ってもエクスポートは可能です。)
現在、タイトル・本文・投稿日時・カテゴリのエクスポートには対応していますが、コメント・画像・その他の要素については対応していません。はてなブログは画像の引っ越しまでやってくれるのを確認済みです。
## クイックスタート
```bash
pip install git+https://github.com/Hagihara-A/migrate-exblog#egg=migrate_exblog
migrate-exblog --url=<url>
```
これだけでエクスポートが出来ます。

## 使い方
基本的には以下の様に使います
```bash
$ migrate-exblog --url=<url
```
ヘルプは以下です。
```bash
$ migrate-exblog -h
usage: migrate-exblog [-h] [-u URL] [-s STRUCTURE | -j STRUCTURE_JSON]
                      [-o OUTPUT] [-t] [-v]
                      {make-conf} ...

positional arguments:
  {make-conf}

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     移行元のエキサイトブログのURLを指定してください
  -s STRUCTURE, --structure STRUCTURE
                        構造htmlのパスを指定してください。デフォルトでは./structure.htmlです。
  -j STRUCTURE_JSON, --structure-json STRUCTURE_JSON
                        json形式の構造ファイルのパスを指定してください。デフォルトではconf.jsonです
  -o OUTPUT, --output OUTPUT
                        出力ファイルのパスを指定してください。デフォルトはmigrate.mt.txtです。
  -t, --test            一月だけ出力することができます。
  -v, --verbose         進行状況を表示します。

$ migrate-exblog make-conf -h
usage: migrate-exblog make-conf [-h] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        生成するテンプレートのパスを指定してください。デフォルトはconf.jsonです。
```

### structure引数について
管理画面トップ> デザイン設定(左のメニューの中)> 編集(現在使用中のスキンのもの)> 本文(HTML&CSS編集のタブ)

にあるhtmlをファイルに保存したもののパスを指定してください。このhtmlにはブログ本文の構造が書かれています。これを構造htmlと呼ぶことにします。

デフォルトでは``./structure.html``です。

## 構造htmlがわからない場合
パスワードを忘れたなどの理由で構造htmlがわからない場合、タイトル・本文・フッタ−のクラスを直接指定してエクスポートできます。

``migrate-exblog make-conf``とすることでカレントディレクトリに``conf.json``というテンプレートが生成されます。

テンプレートの内容は以下のようになっています
```bash
$ ls
$ migrate-exblog make-conf
$ ls
conf.json
$ cat conf.json
{
  "class_title": "post-title",
  "class_body": "post-main",
  "class_tail": "post-tail"
}
```
これは https://staff.exblog.jp/ のクラスを指定したものになります。自身で指定する際はこれを参考にして間違えないようにしてください。
## デモ
```bash
pip install git+https://github.com/Hagihara-A/migrate-exblog#egg=migrate_exblog
$ migate-exblog　make-conf
$ ls
conf.json
$ migrate-exblog --url=https://staff.exblog.jp/ -v -t
100%|██████████████████████████| 3/3 [00:02<00:00,  1.03it/s]
$ ls
conf.json  migrate.mt.txt
```
とすればデフォルトで設定されている、https://staff.exblog.jp/ の１ヶ月分の記事をエクスポートします。

## ファイルから引数を読み込む
```bash
$ migrate-exblog make-conf
$ cat > args.txt
--url=https://staff.exblog.jp/
-v
-t
$ ls
args.txt  conf.json
$ migrate-exblog @args.txt
args.txt  conf.json  migrate.mt.txt
```
のようにファイル名の前に@をつけることでファイルから引数を読み込めます。詳しくは https://docs.python.org/ja/3/library/argparse.html#fromfile-prefix-chars をご覧ください。
## ライセンス
MIT licenseです
