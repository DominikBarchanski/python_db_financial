from fastapi import FastAPI ,APIRouter
from api.endpoint import Balance,expense
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "*",
]

app = FastAPI(title='PROJECT_NAME', version="0.1.0")
api_router = APIRouter()
api_router.include_router(Balance.router, prefix="/balance", tags=["balance"])
api_router.include_router(expense.router, prefix="/expense", tags=["expense"])
app.include_router(api_router, prefix='/api/v1/balance')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)