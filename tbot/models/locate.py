from unicodedata import name
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

from tbot.models.database import Base


# class PlayerScore(Base):
#     __tablename__ = "playerscore"

#     user_id = Column(BigInteger, primary_key=True,
#                      unique=True, autoincrement=False)
#     score = Column(Integer, default=0)

class Locate(Base):

    __tablename__ = 'location'
    __tableargs__ = {
        'comment': 'Контент, привязанный к локации'
    }

    location_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String(128), comment='Наименование темы')
    lat = Column(String(128), comment='Координата')
    lon = Column(String(128), comment='Координата')
    # location = Column(Geometry('POINT'))
    description = Column(Text, comment='Описание темы')

    def __repr__(self):
        return f'{self.location_id} {self.name} {self.lat} {self.lon}'

    async def add_fake_data(session):
        point = [('57.95150366443563', '102.7431531417659'),
                 ('57.95158217906014', '102.74267119452682'),
                 ('57.95164258578099', '102.74232709179691'),
                 ('57.95181193855095', '102.74111271989159'),
                 ('57.95187218178018', '102.74019942516564'),
                 ('57.95198061933527', '102.73927099296084'),
                 ('57.95215331550237', '102.73820127759477'),
                 ('57.952168777695036', '102.73751953673947')
                 ]
        for lat, lon in point:
            print(lat, lon)
            loc = Locate(
                name=f'name',
                lat = lat,
                lon = lon,
                description = f'descr'
            )
            session.add(loc)
        await session.commit()
    
            
