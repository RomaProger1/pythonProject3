import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Dict, List
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

#Заполнение данных
class Products(BaseModel):
    name: str
    products_id:int = 0
    description:str = ''
    price: float

#БД для хранение данных о продуктах
products_db: Dict[str,Products] = {}

#Создание карточки продуктов
@app.post('/products/', response_model=dict)
async def add_product(product: Products, ):
    product_id = str(len(products_db)+1)
    products_db[product_id] = product
    return {"id": product_id}

#Чтение карточки продукта
@app.get('/products/{produts_id}',response_model=Products)
async def read_product(product_id: str):
    product_id = products_db.get(product_id)
    if Products is None:
        raise HTTPException(status_code=404, detail="Продукция не найдена")
    return Products

#Скачивание списка
@app.get('/products_download',response_model=List[Products])
async def download_products():
    return list(products_db.values())

# Стартовая страница
@app.get('/', response_class = HTMLResponse)
def index():
    return "<b>  Здравствуйте! </b>"

# Запуск сервера приложения FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)