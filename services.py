from datetime import date, timedelta
from databases.models import User, Favorite
from databases.connection import async_session
from sqlalchemy import delete
from sqlalchemy.future import select
from aiohttp import ClientSession
from schemas import DaySummaryOutput

# ----------------------------------------------------------------

class UserService():
    async def create_user(name: str):
        async with async_session() as session:
           session.add(User(name=name))
           await session.commit()
           
    async def delete_user(user_id: int):
        async with async_session() as session:
            await session.execute(delete(User).where(User.id==user_id))
            await session.commit()
    
    async def list_users():
        async with async_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()
            
    async def get_user_by_id(user_id: int):
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id==user_id))
            return result.scalar()
            
            
class FavoriteService():
    async def add_favorite(user_id: int, symbol: str):
        async with async_session() as session:
            session.add(Favorite(user_id=user_id, symbol=symbol))
            await session.commit()

    async def delete_favorite(user_id: int, symbol: str):
        async with async_session() as session:
            await session.execute(delete(Favorite).where(
                Favorite.user_id==user_id, 
                Favorite.symbol==symbol)
            )
            await session.commit()
            

# ---------------------------------------------------------------------


class AssetsService():
    async def day_symmary(symbol: str):
        async with ClientSession() as session:
            yesterday = str(date.today() - timedelta(days=1))
            
            base_url = "https://www.mercadobitcoin.net/api/{symbol}/day-summary/{date}"
            
            yesterday = yesterday.replace('-', '/')            
            url = base_url.format(symbol=symbol, date=yesterday)
           
            try:
                response = await session.get(url=url)
                data = await response.json()
                dso = DaySummaryOutput(
                    symbol=symbol, 
                    date=yesterday,
                    highest=data.get('highest', 0),
                    lowest=data.get('lowest', 0),
                    details='Success'
                )
            except Exception as err:
                dso = DaySummaryOutput(
                    symbol=symbol, 
                    date=yesterday,
                    highest=0, lowest=0,
                    details=f'ERROR ==>> {str(err)}'
                )
            finally:
                return dso.model_dump()
                
        