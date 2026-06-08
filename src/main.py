from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Reversi Brain API",
    description="オセロのコアロジックとAIを提供するAPIサーバー",
    version="1.0.0"
)

# Web（Next.js）からの通信を許可する設定 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# サーバー起動確認用の簡単な「Hello World」エンドポイント
@app.get("/")
def read_root():
    return {"message": "Reversi Brain API is running!"}