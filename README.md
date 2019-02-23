# migrate-exblog
エキサイトブログをmovable type形式で出力するスクリプト
## 概要
エキサイトブログにはエクスポート機能がないのでスクレイピングしてmovable type(MT)形式で出力します。(FC2を使ってもエクスポートは可能です。)
現在、タイトル・本文・投稿日時のエクスポートには対応していますが、コメント・カテゴリ・その他の要素については対応していません。
## クイックスタート
```bash
pip install git+https://github.com/Hagihara-A/migrate-exblog
migrate-exblog make-conf
migrate-exblog migrate
```
これだけで移行作業が出来ます。

## 使い方
正しく移行するには正しい設定をしなければいけません。

```bash
migrate-exblog make-conf
```
とすることで、カレントディレクトリに``migrate-conf.json``が生成されます。``migrate-conf.json``には移行作業のために必要な情報の雛形が記載されています。


ここからは``migrate-conf.json``を編集します。内容はデフォルトで以下のようになっています
```json
{
    "url": "https://staff.exblog.jp/",
    "date": {
        "2018": [
            12
        ]
    },
    "selector_title": ".post-title",
    "selector_body": ".post-main"
}
}
```
- url: 出力したいブログのURLを入力してください
- date: 出力したい年と月を辞書（オブジェクト）形式で入力してください。以下に詳しいdateの書き方があります。
- selector_title: タイトルを含むdivのクラスをCSSセレクタ形式で指定します。
- selector_body: 本文を含むdivのクラスをCSSセレクタ形式で指定します。

セレクタ−の指定は間違えやすいと思うのでデフォルトの値を参考にしてみてください。
## dateの記法
### 年の期間の指定方法
2015年のみを出力したい場合は"2015"とすれば良いです。
2000~2019年を出力したい場合は"2001-2019"の様に年と年を -（ハイフン） でつないでください。
### 月の指定方法
"all"とすれば1~12月を指定したのと同じことになります。
もし1~3月のみを出力したいのであれば、[1,2,3]としてください。
### 例

```json
"date": {
  "2018": [12]
}
```
これは2018年12月のみを出力します。
```json
"date": {
  "2015-2018": "all"
}
```
これは2015~2018年の全ての記事を出力します。
```json
"date": {
  "2005-2011": [1,2,6,8]
}
```
これは2005~2011年の1,2,6,8月の記事のみを出力します。
```json
"date": {
  "2001": [11,12],
  "2002-2008": "all" ,
  "2009-2019": [1,6,12]
}
```
とすることもできます。
## コマンドのオプション
migrate-exblog のサブコマンドには
1. make-conf
2. migrate

の２つがあります。
### make-conf
```bash
usage: migrate-exblog make-conf [-h] [--config-file-path CONFIG_FILE_PATH]

<--config-file-path>に設定ファイルを作成します.デフォルトは./migrate-conf.jsonです.

optional arguments:
  -h, --help            show this help message and exit
  --config-file-path CONFIG_FILE_PATH
                        設定ファイルのパスを指定してください.
```

### migrate
```bash
usage: migrate-exblog migrate [-h] [--conf-path CONF_PATH]
                              [--output-path OUTPUT_PATH]

ブログを出力します.

optional arguments:
  -h, --help            show this help message and exit
  --conf-path CONF_PATH
                        設定ファイルのパスを指定してください.デフォルトでは./migrate-conf.jsonです.
  --output-path OUTPUT_PATH
                        出力ファイルのパスを指定してください。デフォルトでは./migrate.mt.txtです.
```

## デモ
```bash
pip install git+https://github.com/Hagihara-A/migrate-exblog
migate-exblog make-conf
migrate-exblog migrate
```
とすればデフォルトで設定されている、スタッフブログの2018年12月の記事を出力できます。

またmigrate-conf.jsonを以下のように編集すると
```json
"date":{
  "2000-2019": "all"
}
```
スタッフブログの2000年1月~2019年12月を走査し、記事をエクスポートできます。

## ライセンス
MIT licenseです
