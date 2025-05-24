#main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from middleware import *
from schemas import *
from typing import Optional, List
import requests

URL_ACCOUNT_SERVICE = os.getenv("URL_ACCOUNT_SERVICE")
URL_AUTH_SERVICE = os.getenv("URL_AUTH_SERVICE")
URL_EXCHANGE_SERVICE = os.getenv("URL_EXCHANGE_SERVICE")
URL_PRODUCT_SERVICE = os.getenv("URL_PRODUCT_SERVICE")
URL_ORDER_SERVICE = os.getenv("URL_ORDER_SERVICE")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/")
def read_root():
    return {"message": "Gateway microservice is up!"}

@app.post("/register", response_model=UserReadDTO, status_code=201)
async def register_gateway(payload: UserCreateDTO):
    try:
        response = requests.post(URL_ACCOUNT_SERVICE + "/account/register", json=payload.dict())
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))
        
        user = response.json()
        return UserReadDTO(
            uuid=user["uuid"], 
            username=user["username"], 
            email=user["email"]
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/login", response_model=UserReadDTO, status_code=200)
async def login_gateway(payload: UserLoginDTO):
    try:
        response = requests.post(URL_AUTH_SERVICE + "/auth/login", json=payload.dict())

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

        session_token = response.cookies.get("session_token")
        if not session_token:
            raise HTTPException(status_code=500, detail="Session token not found in login response")

        user = response.json()

        client_response = JSONResponse(content=user)
        client_response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            samesite="lax"
        )

        return client_response

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/exchange/{currency1}/{currency2}", status_code=200)
async def exchange_gateway(currency1: str, currency2: str, request: Request):
    try:
        session_token = request.cookies.get("session_token")
        headers = {
            "Authorization": f"Bearer {session_token}"
        }
        
        response = requests.get(URL_EXCHANGE_SERVICE + f"/exchange/{currency1}/{currency2}", 
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))
        
        return response.json()


    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/product", response_model=ProductReadDTO, status_code=201)
async def create_product_gateway(payload: ProductCreateDTO, request: Request):
    try:
        session_token = request.cookies.get("session_token")
        headers = {"Authorization": f"Bearer {session_token}"}

        response = requests.post(URL_PRODUCT_SERVICE + "/product", json=payload.dict(), headers=headers)

        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

        return response.json()

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/product", response_model=List[ProductReadDTO], status_code=200)
async def get_all_products_gateway(request: Request):
    try:
        session_token = request.cookies.get("session_token")
        headers = {"Authorization": f"Bearer {session_token}"}

        response = requests.get(URL_PRODUCT_SERVICE + "/product", headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

        return response.json()

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/product/{id}", response_model=ProductReadDTO, status_code=200)
async def get_product_by_id_gateway(id: int, request: Request):
    try:
        session_token = request.cookies.get("session_token")
        headers = {"Authorization": f"Bearer {session_token}"}

        response = requests.get(URL_PRODUCT_SERVICE + f"/product/{id}", headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

        return response.json()

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/product/{id}", response_model=ProductReadDTO, status_code=200)
async def delete_product_gateway(id: int, request: Request):
    try:
        session_token = request.cookies.get("session_token")
        headers = {"Authorization": f"Bearer {session_token}"}

        response = requests.delete(URL_PRODUCT_SERVICE + f"/product/{id}", headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

        return response.json()

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/order", response_model=OrderReadDTO, status_code=201)
async def create_order_gateway(payload: OrderCreateDTO, request: Request):
    try:
        session_token = request.cookies.get("session_token")
        headers = {"Authorization": f"Bearer {session_token}"}

        response = requests.post(
            URL_ORDER_SERVICE + "/order",
            json=payload.dict(),
            headers=headers
        )

        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

        return response.json()

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/order", response_model=List[OrderShortReadDTO], status_code=200)
async def get_all_orders_gateway(request: Request):
    try:
        session_token = request.cookies.get("session_token")
        headers = {"Authorization": f"Bearer {session_token}"}

        response = requests.get(
            URL_ORDER_SERVICE + "/order",
            headers=headers
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

        return response.json()

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/order/{id}", response_model=OrderReadDTO, status_code=200)
async def get_order_by_id_gateway(id: int, request: Request):
    try:
        session_token = request.cookies.get("session_token")
        headers = {"Authorization": f"Bearer {session_token}"}

        response = requests.get(
            URL_ORDER_SERVICE + f"/order/{id}",
            headers=headers
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail"))

        return response.json()

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))