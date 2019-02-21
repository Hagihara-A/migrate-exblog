# migrate-exblog
エキサイトブログをmovable type形式で出力するスクリプト
## 概要
エキサイトブログにはエクスポート機能がないのでスクレイピングしてmovable type(MT)形式で出力します。(FC2を使ってもエクスポートは可能です。)
現在、タイトル・本文・投稿日時のエクスポートには対応していますが、コメント・カテゴリ・その他の要素については対応していません。
## クイックスタート
```bash
pip install git+git@github.com:Hagihara-A/migrate-exblog
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
    "is_test": true,
    "url": "https://staff.exblog.jp/",
    "years": [
        2018,
        2019
    ],
    "test_year": 2018,
    "test_month": 12,
    "selector_post": ".post",
    "selector_title": ".post-title",
    "selector_body": ".post-main",
    "selector_foot": ".post-tail"
}
```

- is_test: Trueにした場合、特定の月のみを出力することで動作確認が出来ます。この時引数test_yearとtest_monthの値が使われます。yearsは無視されます。Falseにした場合、yearsで指定した範囲の記事を全て出力します。また、この時test_yearとtest_monthは無視されます。
- years: ある年だけを出力したい場合は"years": [2018, 2018]、もしくは単純に"years": 2018としてください。
- url: 出力したいブログのURLを入力してください
- selector_post: タイトル・本文・投稿日時を全て含むCSSセレクタを指定します。
- selector_title: タイトルを含むdivのクラスをCSSセレクタ形式で指定します。
- selector_body: 本文を含むdivのクラスをCSSセレクタ形式で指定します。
- selector_foot: 投稿日時を含むdivのクラスをCSSセレクタ形式で指定します。フッタ−はTIMEクラスを含むdivの親要素です。

セレクタ−の指定は間違えやすいと思うのでデフォルトの値を参考にしてみてください。

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
pip install git+git@github.com:Hagihara-A/migrate-exblog
migate-exblog make-conf
migrate-exblog migrate
```
とすればデフォルトで設定されている、スタッフブログの2018年12月の記事を出力できます。

またmigrate-conf.jsonを以下のように編集すると
```json
"is_test": false
"years": [2000, 2019]
```
スタッフブログの2000年1月~2019年12月を走査し、記事をエクスポートできます。

## ライセンス
MIT licenseです
