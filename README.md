# Market Tool

 - [JPX](https://www.jpx.co.jp/markets/statistics-equities/misc/01.html)
 - [Twitter API](https://developer.twitter.com/ja)
 - [Slack](https://slack.com/intl/ja-jp/)
 - [Incoming Webhook](https://slack.com/apps/A0F7XDUAZ--incoming-webhook-?tab=more_info)

***

### 機能

 - [x] 市場データ集計
 - [x] 営業日判定
 - [x] 市場トレンド取得
 - [x] Twitter・Slackボット

***

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

***

### `.env`

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
