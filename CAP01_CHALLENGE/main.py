from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt

app = FastAPI()

class Payload(BaseModel):
    numbers: List[int]

class BinarySearchPayload(BaseModel):
    numbers: List[int]
    target: int

# Fake db
fake_db = {"users": {}}

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def oauth2_scheme(token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/register")
def register(username: str, password: str):
    if username in fake_db["users"]:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_password = get_password_hash(password)
    fake_db["users"][username] = hashed_password
    return {"message": "User registered successfully"}

@app.post("/login")
def login(username: str, password: str):
    if username not in fake_db["users"]:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    hashed_password = fake_db["users"][username]
    if not verify_password(password, hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token}

@app.post("/bubble-sort")
def bubble_sort(payload: Payload, token: str = Depends(oauth2_scheme)):
    numbers = payload.numbers
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return {"numbers": numbers}

@app.post("/filter-even")
def filter_even(payload: Payload, token: str = Depends(oauth2_scheme)):
    numbers = payload.numbers
    even_numbers = [num for num in numbers if num % 2 == 0]
    return {"even_numbers": even_numbers}

@app.post("/sum-elements")
def sum_elements(payload: Payload, token: str = Depends(oauth2_scheme)):
    numbers = payload.numbers
    return {"sum": sum(numbers)}

@app.post("/max-value")
def max_value(payload: Payload, token: str = Depends(oauth2_scheme)):
    numbers = payload.numbers
    return {"max": max(numbers)}

@app.post("/binary-search")
def binary_search(payload: BinarySearchPayload, token: str = Depends(oauth2_scheme)):
    numbers = payload.numbers
    target = payload.target
    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == target:
            return {"found": True, "index": mid}
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return {"found": False, "index": -1}