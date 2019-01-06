# scrape-excite-blog
エキサイトブログをmovable type形式で出力するスクリプト
## 概要
エキサイトブログにはエクスポート機能がないので無理やりmovable type(MT)形式で無理やり出力させます。
現在、タイトル・本文・投稿日時のエクスポートには対応していますが、コメント・カテゴリ・その他の要素については対応していません。
また、サイト全体をMT形式で出力した際、.pickleというファイルが生成されますが、全て処理が終わった後ならば消していただいて大丈夫です。

## 使い方
```bash
git clone https://github.com/Hagihara-A/scrape-excite-blog.git
cd scrape-excite-blog
```
ここからは直接makeMTtext.pyを編集します。
```python
if __name__ == '__main__':
    exe = ExecStream(isTest=True,
                     url='',
                     years=(2000, 2020),
                     test_year=2018,
                     test_month=12,
                     excludeFunc=lambda y, m: True,
                     container_path=Path('entries'),
                     selector_entry='.POST',
                     selector_title='.POST_TTL',
                     selector_body='.POST_CON',
                     selector_date='.TIME',
                     output_path=Path('migrate.mt.txt'))
```

- isTest: Trueにした場合、特定の月のみを出力して、動作確認が出来ます。この時引数test_yearとtest_monthの値が使われます。yearsは無視されます。
Flaseにした場合、yearsで指定した範囲の記事を全て出力します。また、この時test_yearとtest_monthは無視されます。
- url: 出力したいブログのURLを入力してください
- excludeFunc: 除外したい月があるときに利用します。特定の日の除外には対応していません。(year, month)という引数を受け取り、Falseを返すとその月はスキップされます。
- container_path: 出力先のディレクトリ名を指定します。処理が終わった後は消していただいて結構です。
- selector_entry: タイトル・本文・投稿日時を全て含むCSSセレクタを指定します。
- selector_title: titleの親要素のCSSセレクタを指定します。
- selector_body: 本文の親要素のCSSセレクタを指定します。
- selector_date: 投稿日時の親要素のCSSセレクタを指定します。
- output_path: 出力ファイルの名前です。

全て指定した後
```bash
python makeMTtext.py
```
でエクスポートできます。
## デモ
```python
if __name__ == '__main__':
    exe = ExecStream(isTest=True,
                     url='https://staff.exblog.jp/',
                     years=(2000, 2020), # this arg is ignored
                     test_year=2018,
                     test_month=12,
                     excludeFunc=lambda y, m: True,
                     container_path=Path('entries'),
                     selector_entry='.post',
                     selector_title='.post-title',
                     selector_body='.post-main',
                     selector_date='.TIME',
                     output_path=Path('migrate.mt.txt'))
```
とすればスタッフブログの2018年12月の記事を出力できます。

```python
if __name__ == '__main__':
    exe = ExecStream(isTest=False, # changed
                     url='https://staff.exblog.jp/',
                     years=(2017, 2018), # changed
                     test_year=2018, # this arg is ignored
                     test_month=12, # this arg is ignored
                     excludeFunc=lambda y, m: True,
                     container_path=Path('entries'),
                     selector_entry='.post',
                     selector_title='.post-title',
                     selector_body='.post-main',
                     selector_date='.TIME',
                     output_path=Path('migrate.mt.txt'))
```
とすればスタッフブログの2017年1月~2018年12月の記事をエクスポートできます。

## ライセンス
MIT licenseです
