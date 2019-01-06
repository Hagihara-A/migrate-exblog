# scrape-excite-blog
エキサイトブログをmovable type形式で出力するスクリプト
## 概要
エキサイトブログにはエクスポート機能がないのでスクレイピングして無理やりmovable type(MT)形式で無理やり出力させます。
現在、タイトル・本文・投稿日時のエクスポートには対応していますが、コメント・カテゴリ・その他の要素については対応していません。
また、サイト全体をMT形式で出力した際、.pickleというファイルが生成されますが、全て処理が終わった後ならば消していただいて大丈夫です。

## 使い方
```bash
git clone https://github.com/Hagihara-A/scrape-excite-blog.git
cd scrape-excite-blog
```
ここからはinput.jsonを編集します。input.jsonの内容はデフォルトで以下のようになっています
```json
{"isTest": true, "url": "https://staff.exblog.jp/", "years": [2018, 2019], "test_year": 2018, "test_month": 12, "container_path": "entries", "selector_entry": ".post", "selector_title": ".post-title", "selector_body": ".post-main", "selector_date": ".TIME", "output_path": "../migrate.mt.txt"}
```

- isTest: Trueにした場合、特定の月のみを出力することで動作確認が出来ます。この時引数test_yearとtest_monthの値が使われます。yearsは無視されます。
Falseにした場合、yearsで指定した範囲の記事を全て出力します。また、この時test_yearとtest_monthは無視されます。
- url: 出力したいブログのURLを入力してください
- container_path: 出力先のディレクトリ名を指定します。処理が終わった後はこのディレクトリは消していただいて結構です。
- selector_entry: タイトル・本文・投稿日時を全て含むCSSセレクタを指定します。
- selector_title: titleの親要素のCSSセレクタを指定します。
- selector_body: 本文の親要素のCSSセレクタを指定します。
- selector_date: 投稿日時の親要素のCSSセレクタを指定します。
- output_path: 出力ファイルの名前です。scrapeExciteBlog/codesからの相対パスになっています。

全て指定した後
```bash
python makeMTtext.py
```
でエクスポートできます。
## デモ
```bash
git clone https://github.com/Hagihara-A/scrape-excite-blog.git
cd scrape-excite-blog
python codes/makeMTText.py
```
とすればスタッフブログの2018年12月の記事を出力できます。

またinput.jsonの内容を以下のように編集すれば
```json
"isTest": false
```
スタッフブログの2018年1月~2018年12月の記事をエクスポートできます。

## ライセンス
MIT licenseです
