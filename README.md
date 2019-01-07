# scrape-excite-blog
エキサイトブログをmovable type形式で出力するスクリプト
## 概要
エキサイトブログにはエクスポート機能がないのでスクレイピングしてmovable type(MT)形式で出力します。(FC2を使ってもエクスポートは可能です。)
現在、タイトル・本文・投稿日時のエクスポートには対応していますが、コメント・カテゴリ・その他の要素については対応していません。

## 使い方
```bash
git clone https://github.com/Hagihara-A/scrape-excite-blog.git
cd scrape-excite-blog
```
ここからはinput.jsonを編集します。input.jsonの内容はデフォルトで以下のようになっています
```json
{"isTest": true, "url": "https://staff.exblog.jp/", "years": [2018, 2019], "test_year": 2018, "test_month": 12, "selector_entry": ".post", "selector_title": ".post-title", "selector_body": ".post-main", "selector_date": ".TIME"}
```

- isTest: Trueにした場合、特定の月のみを出力することで動作確認が出来ます。この時引数test_yearとtest_monthの値が使われます。yearsは無視されます。
Falseにした場合、yearsで指定した範囲の記事を全て出力します。また、この時test_yearとtest_monthは無視されます。
- url: 出力したいブログのURLを入力してください
- selector_entry: タイトル・本文・投稿日時を全て含むCSSセレクタを指定します。
- selector_title: titleの親要素のCSSセレクタを指定します。
- selector_body: 本文の親要素のCSSセレクタを指定します。
- selector_date: 投稿日時の親要素のCSSセレクタを指定します。

全て指定した後
```bash
python codes/makeMTtext.py
```
でエクスポートを実行できます。migrate.mt.txtというファイルに出力されます。
## デモ
```bash
git clone https://github.com/Hagihara-A/scrape-excite-blog.git
cd scrape-excite-blog
python codes/makeMTText.py
```
とすればデフォルトで設定されている、スタッフブログの2018年12月の記事を出力できます。

またinput.jsonの内容を以下のように編集して、
```json
"isTest": false
"years": [2000, 2019]
```
```bash
python codes/makeMTtext.py
```
とすればスタッフブログの2000年1月~2019年12月を走査し、記事をエクスポートできます。

## ライセンス
MIT licenseです
