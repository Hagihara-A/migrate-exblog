# migrate-exblog
エキサイトブログをmovable type形式で出力するスクリプト
## 概要
エキサイトブログにはエクスポート機能がないのでスクレイピングしてmovable type(MT)形式で出力します。(FC2を使ってもエクスポートは可能です。)
現在、タイトル・本文・投稿日時・カテゴリのエクスポートには対応していますが、コメント・その他の要素については対応していません。
## クイックスタート
```bash
pip install git+https://github.com/Hagihara-A/migrate-exblog
migrate-exblog --url=<url>
```
これだけでエクスポートが出来ます。

## 使い方
```bash
migrate-exblog --url=<url> --html=<html> --test --verbose
```
引数の説明
- --url: 移行元のエキサイトブログのurlです。
- --html: 以下で説明する、構造htmlのパスを指定します。
- --test: 一月だけ試しに出力することができます。
- --verbose: 進行状況を表示します。

### html引数について
管理画面トップ> デザイン設定(左のメニューの中)> 編集(現在使用中のスキンのもの)> 本文(HTML&CSS編集のタブ)

にあるhtmlをコピーしてファイルに保存したもののパスを指定してください。このhtmlにはブログ本文の構造が書かれています。これを構造htmlと呼ぶことにします。

デフォルトでは``./structure.html``です。

## 構造htmlがわからない場合
パスワードを忘れたなどの理由で構造htmlがわからない場合、本文などのクラスを直接指定することができます。

とすることで、カレントディレクトリに``migrate-conf.json``が生成されます。``migrate-conf.json``には移行作業のために必要な情報の雛形が記載されています。


ここからは``migrate-conf.json``を編集します。内容はデフォルトで以下のようになっています
```json
{
    "url": "https://staff.exblog.jp/",
    "class_post": "post",
    "class_title": "post-title",
    "class_body": "post-main",
    "class_tail": "post-tail",
    "one_month": true
}
```
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
とすればデフォルトで設定されている、。

## ライセンス
MIT licenseです
