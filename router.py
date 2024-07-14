from http.client import HTTPException
from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("", response_model=schemas.UserInDB)
async def create_user(user: Annotated[schemas.UserCreate, Depends()], db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.UserInDB)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=schemas.UserInDB)
async def update_user(user_id: int, user: Annotated[schemas.UserUpdate, Depends()], db: AsyncSession = Depends(get_db)):
    db_user = await crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=schemas.UserInDB)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
