from fastapi import FastAPI ,APIRouter
from api.endpoint import productList,productCategories

# Odczytaj zmienną środowiskową, aby określić nazwę usługi
# Domyślnie używaj "main" jako nazwy usługi




app = FastAPI(title='PROJECT_NAME', version="0.1.0")
api_router = APIRouter()
api_router.include_router(productList.router, prefix="/productList", tags=["productList"])
api_router.include_router(productCategories.router, prefix="/productCategories", tags=["productCategories"])
app.include_router(api_router, prefix='/api/v1/products')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)