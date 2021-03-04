from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import orm
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from db_api import async_session
import asyncio
from schema import Base, User, Profile


async def main():
    async with async_session() as session:
        ed_user = User(name='ed')
        session.add(ed_user)
        await session.commit()

        # q = select(User).where(User.name == 'ed')
        # res = session.execute(q)
        # our_user = Session.query(User).filter_by(name='ed').first()
        # our_user


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
