from datetime import date, timedelta
from fastapi import APIRouter
from databases.models import User
import requests
from typing import List
from schemas import ErrorOutput, DaySummaryOutput

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(getenv("DATABASE_URL_SYNC"))
SessionLocal = sessionmaker(bind=engine)

sync_router = APIRouter(prefix='/sync')

@sync_router.get("/day_symmary/{user_id}", response_model=List[DaySummaryOutput], responses={401: {'model': ErrorOutput}})
def day_symmary(user_id: int):
    base_url = "https://www.mercadobitcoin.net/api/{symbol}/day-summary/{date}"
    yesterday = str(date.today() - timedelta(days=1))    
    yesterday = yesterday.replace('-', '/')

    with SessionLocal() as session:
        user = session.query(User).filter(User.id==user_id).first()
        list_of_symbols = [favo.symbol for favo in user.favorites]
    
    unique_symbols = set(list_of_symbols)
        
    final_result = list()
    for one_symbol in unique_symbols:
        url = base_url.format(symbol=one_symbol, date=yesterday)

        try:
            data = requests.get(url=url).json()
            dso = DaySummaryOutput(
                symbol=one_symbol, date=yesterday,
                highest=data.get('highest', 0),
                lowest=data.get('lowest', 0), 
                details='Success'
            )
        except Exception as err:
            dso = DaySummaryOutput(
                symbol=one_symbol, date=yesterday,
                highest=0, lowest=0, 
                details=f'ERROR --> {str(err)}'
            )
        finally:
            final_result.append(dso.model_dump())

    return final_result
