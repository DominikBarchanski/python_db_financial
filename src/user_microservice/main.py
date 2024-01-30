from fastapi import FastAPI, APIRouter
from api.endpoint import users, userGroup, addUserToGroup
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]

app = FastAPI(title='PROJECT_NAME', version="0.1.0")
api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(userGroup.router, prefix="/userGroup", tags=["userGroup"])
api_router.include_router(addUserToGroup.router, prefix="/addUserToGroup", tags=["addUserToGroup"])
app.include_router(api_router, prefix='/api/v1/accounts')
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
