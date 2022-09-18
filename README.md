# Market Tool

 - [東証上場銘柄一覧](https://www.jpx.co.jp/markets/statistics-equities/misc/01.html)
 - [新市場区分の選択結果](https://www.jpx.co.jp/equities/market-restructure/results/index.html)
 - ~~[Twitter API](https://developer.twitter.com/ja)~~
 - ~~[Slack](https://slack.com/intl/ja-jp/)~~
 - ~~[Incoming Webhook](https://slack.com/apps/A0F7XDUAZ--incoming-webhook-?tab=more_info)~~

---

### 機能

 - [x] 市場データ集計
 - [x] 営業日判定
 - [x] 市場トレンド取得
 - [x] ~~Twitter・Slackボット~~

---

### 構成

```
├─data
│  ├─logs
│  ├─market_data
│  └─totalling_data
├─src
│  └─...
├─.env
├─.gitignore
├─main.py
├─README.md
├─requirements.txt
└─settings.py
```

`main.py`を実行することで`data`フォルダ直下に、
ログ格納用の`logs`フォルダ、
市場データ(csv)格納用の`market_data`フォルダ、
市場データを集計した画像ファイル格納用の`totalling_data`フォルダが作成されます。
その他、銘柄情報を取得する`data_j.csv`ファイルが`data`直下にダウンロードされます。
`data_j.csv`は1ヵ月おきに更新され、各フォルダも1ヵ月毎に作成されます。
また、2022年の場合、祝日などの情報が書かれた`2022.txt`が新たに作成されます。
これは、1年おきに新たなファイルが作成されます。

***

### ~~`.env`~~

<details>
<summary>...</summary>

`WEB_HOOK_URL`には[Incoming Webhook](https://slack.com/apps/A0F7XDUAZ--incoming-webhook-?tab=more_info)
から取得したURLを追記してください。
`WEB_HOOK_URL`以外には、TwitterAPIから取得した各種キーを追記してください。以下はテンプレートです。

```
WEB_HOOK_URL=
API_KEY=
API_KEY_SECRET=
BEARER_TOKEN=
ACCESS_TOKEN=
ACCESS_TOKEN_SECRET=
```

<details>
