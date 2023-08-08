from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID

from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("59d23710-84af-4837-9f20-02e085290021"),
        first_name="Tina",
        last_name="Sengkara",
        gender=Gender.female,
        roles=[Role.student.value]
    ),
    User(
        id=UUID("8024389e-ab17-40c3-aa42-89b4a191afb6"),
        first_name="Radja",
        last_name="Pramujara",
        gender=Gender.male,
        roles=[Role.admin.value, Role.user.value]
    ),
]

@app.get("/")
def root(): 
    return {"Hello": "Aleza"} 

@app.get("/api/v1/users", response_model=List[User]) 
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id" : user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
        raise HTTPException (
            status_code=404,
            detail=f"user with id : {user_id} does not exists"
        )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
                return
    raise   HTTPException(
        status_code=404,
        detail=f"user with id : {user_id} does not exists"
    )