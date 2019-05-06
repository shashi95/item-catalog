from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datatime
from database_setup import SportCatagory, Base, Item

engine = create_engine('sqlite:///sports.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create sports
Sport1 = SportCatagory(name="Soccer")
session.add(Sport1)
session.commit()


item1 = Item( name="TwoShingaurds", description="A shin guard or shin pad is a piece of equipment worn on the front of a player shin to protect them from injury. These are commonly used in sports including association football, baseball, ice hockey, field hockey, lacrosse, cricket, mountain bike trials, and other sports. This is due to either being required by the rules laws of the sport or worn voluntarily by the participants for protective measures.",
       sport=Sport1)

session.add(item1)
session.commit()

item2 = Item( name="ThreeShingaurds", description="Two Shingaurds description",
       time_updated = datetime.datetime.now, sport=Sport1)

session.add(item2)
session.commit()

item3 = Item( name="FourShingaurds", description="Two Shingaurds description",
       time_updated = datetime.datetime.now, sport=Sport1)

session.add(item3)
session.commit()


Sport2 = SportCatagory( name="Basketball")
session.add(Sport2)
session.commit()

Sport3 = SportCatagory( name="Baseball")
session.add(Sport3)
session.commit()

Sport4 = SportCatagory( name="Frisbee")
session.add(Sport4)
session.commit()

Sport5 = SportCatagory( name="Snowboarding")
session.add(Sport5)
session.commit()

Sport6 = SportCatagory( name="Rock Climbing")
session.add(Sport6)
session.commit()

Sport7 = SportCatagory( name="Foosball")
session.add(Sport7)
session.commit()

Sport8 = SportCatagory( name="Skating")
session.add(Sport8)
session.commit()

Sport9 = SportCatagory( name="Hockey")
session.add(Sport9)
session.commit()


print "added sports!"