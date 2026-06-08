# Reversi Brain - Python API

リバーシ（オセロ）プロジェクトのバックエンド（APIサーバー）です。
FastAPIを使用して構築されています。

## プロジェクト概要

本リポジトリは、オセロのコアロジック（盤面管理、勝敗判定、AIによる次の一手計算）を担当します。
WebクライアントやモバイルアプリからのAPIリクエストを受け取り、計算結果をJSON形式で返却します。

## 使用技術
- Python 3.11+
- FastAPI
- Uvicorn (ASGIサーバー)
- Pydantic (データバリデーション)
- uv (パッケージ管理)

## 環境構築と起動方法

### 1. 仮想環境の作成と有効化
`bash
uv venv
source .venv/bin/activate
`

### 2. 依存パッケージのインストール
`bash
uv pip install -r requirements.txt
`

### 3. 開発サーバーの起動
`bash
uvicorn src.main:app --reload
`
起動後、[http://localhost:8000/docs](http://localhost:8000/docs) にアクセスするとSwagger UIでAPIの仕様が確認できます。