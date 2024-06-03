from typing import List
from asyncio import gather
from fastapi import APIRouter, HTTPException
from services import (
    UserService, FavoriteService, 
    AssetsService
)
from schemas import (
    UserCreateInput, StandartOutput, 
    ErrorOutput, UserFavoriteAddInput,
    DaySummaryOutput, UserListOutput, 
)

user_router = APIRouter(prefix='/user')
assets_router = APIRouter(prefix='/assets')

@user_router.get("/list", response_model=List[UserListOutput], responses={401: {'model': ErrorOutput}})
async def users_list():
    try:
        return await UserService.list_users()
    except Exception as err:
        raise HTTPException(401, detail=str(err))

@user_router.post("/create", response_model=StandartOutput, responses={401: {'model': ErrorOutput}})
async def create_user(user_input: UserCreateInput):
    try:
        await UserService.create_user(name=user_input.name)
        return StandartOutput(message='201 OK')
    except Exception as err:
        raise HTTPException(401, detail=str(err))

@user_router.delete("/delete/{user_id}", response_model=StandartOutput, responses={401: {'model': ErrorOutput}})
async def delete_user(user_id: int):
    try:
        await UserService.delete_user(user_id)
        return StandartOutput(message='200 OK')
    except Exception as err:
        raise HTTPException(401, detail=str(err))

@user_router.post("/favorite/add", response_model=StandartOutput, responses={401: {'model': ErrorOutput}})
async def add_user_favorite(favorite_add: UserFavoriteAddInput):
    try:
        await FavoriteService.add_favorite(
            user_id=favorite_add.user_id,
            symbol=favorite_add.symbol
        )
        return StandartOutput(message='201 OK')
    except Exception as err:
        raise HTTPException(401, detail=str(err))


@user_router.delete("/favorite/delete/{user_id}", response_model=StandartOutput, responses={401: {'model': ErrorOutput}})
async def delete_user_favorite(user_id: int, symbol: str):
    try:
        await FavoriteService.delete_favorite(user_id, symbol)
        return StandartOutput(message='200 OK')
    except Exception as err:
        raise HTTPException(401, detail=str(err))


@assets_router.get("/day_symmary/{user_id}", response_model=List[DaySummaryOutput], responses={401: {'model': ErrorOutput}})
async def day_symmary(user_id: int):
    try:
        user = await UserService.get_user_by_id(user_id)
        list_of_symbols = [favo.symbol for favo in user.favorites]
        unique_symbols = set(list_of_symbols)
        tasks = [
            AssetsService.day_symmary(one_symbol) 
            for one_symbol in unique_symbols
        ]
        
        return await gather(*tasks)
              
    except Exception as err:
        raise HTTPException(401, detail=str(err))
