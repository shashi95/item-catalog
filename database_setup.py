from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()

class SportCatagory(Base):
	"""All sports catagory having id and name for them"""
	__tablename__ = 'sport_category'

	id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = False)

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'name' : self.name
		}


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    sport_name = Column(Integer, ForeignKey('sport_category.name'))
    time_updated = Column(DateTime, default=datetime.now())
    sport = relationship(SportCatagory)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }



engine = create_engine('sqlite:///sports.db')
Base.metadata.create_all(engine)