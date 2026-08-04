# daily-notifier

GitHub Actionsを利用して、翌日の生活情報を毎晩自動通知するシステムです。

現在はMVP（Minimum Viable Product：最小限の実用機能）の開発を進めています。

---

## プロジェクト概要

本プロジェクトでは、GitHub Actionsによる定期実行を利用し、天気などの生活情報を取得して通知するシステムを構築します。

主な目的は以下のとおりです。

* GitHub Actionsを利用した自動化システムの構築
* Pythonによる外部API連携
* 通知機能を拡張しやすい設計の実践
* AIエージェント（Codex CLI）を活用した開発手法の習得

---

## 開発方針

本プロジェクトでは、以下の方針で開発を進めています。

* 学習目的を重視する
* 保守性・可読性を優先する
* 実務で避けられるアンチパターンは採用しない
* 設計理由を理解しながら実装を進める
* AIエージェントを積極的に活用する

---

## 現在の開発状況


### 実装済み

* プロジェクトの作成
* Gitリポジトリの作成
* 開発方針・設計ドキュメントの整備
* GitHub ActionsによるPython実行
* GitHub Actionsの定期実行
* 気象庁JSONの取得
* JSONから必要な情報の抽出
* Pythonモジュール分割（config.py・weather.py・main.py）
* 取得情報を人間に読みやす形式に変換
*  メール送信
*  GitHub Secretsによる機密情報管理

### 未実装

以下は今後実装予定です。

* 24節季と72候の取得
* 気圧変化
* ごみ収集情報
* 定期実行の発火遅延の解消
* Aiで読みやすい形式に整える。

---

## 開発環境

| 項目      | 内容                 |
| ------- | ------------------ |
| OS      | Windows 11         |
| 言語      |  Python 3.14.6     |
| 利用ライブラリ |  requests  |
| エディタ    | Visual Studio Code |
| バージョン管理 | Git / GitHub       |
| CI/CD   | GitHub Actions     |


---

## ディレクトリ構成

現在は開発初期のため、ディレクトリ構成は変更される可能性があります。

```text
daily-notifier/
├── .github/workflows/
│   └── test.yml
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── format.py
│   ├── mailer.py
│   └── weather.py
├── main.py
├── .venv/（Git管理外）
├── .vscode/（Git管理外）
├── .env（Git管理外）
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ライセンス

未定

---

## 決定事項

### Python仮想環境

本プロジェクトでは、Pythonの仮想環境（`.venv`）を使用しています。

初回セットアップ

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```
仮想環境有効化後は、
```bash
python --version
```
でPython 3.14.6となることを確認してください。

### 依存ライブラリ

ライブラリをインストールする場合は、

```bash
pip install -r requirements.txt
```

### 天気予報データの取得

気象庁ホームページで公開されている予報JSONを利用しています。

採用理由

- APIキー不要
- 日本語の天気予報をそのまま利用できる
- 降水確率・最高気温・最低気温等必要な情報を取得できる

### GitHub Secrets

本プロジェクトでは、メールアドレスやパスワードなどの機密情報はGitHub Secretsで管理しています。

ローカル開発では `.env` を利用し、GitHub Actionsでは Secrets を環境変数として渡しています。