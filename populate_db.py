from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SportCatagory, Base, Item, User

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
Sport1 = SportCatagory(user_id=1, name="Soccer")
session.add(Sport1)
session.commit()


item1 = Item(user_id=1, name="TwoShingaurds", description="A shin guard or shin pad is a piece of equipment worn on the front of a player shin to protect them from injury. These are commonly used in sports including association football, baseball, ice hockey, field hockey, lacrosse, cricket, mountain bike trials, and other sports. This is due to either being required by the rules laws of the sport or worn voluntarily by the participants for protective measures.",
       sport=Sport1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="ThreeShingaurds", description="Two Shingaurds description",
       sport=Sport1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="FourShingaurds", description="Two Shingaurds description",
       sport=Sport1)

session.add(item3)
session.commit()


Sport2 = SportCatagory(user_id=1, name="Basketball")
session.add(Sport2)
session.commit()

Sport3 = SportCatagory(user_id=1, name="Baseball")
session.add(Sport3)
session.commit()

Sport4 = SportCatagory(user_id=1, name="Snowboarding")
session.add(Sport4)
session.commit()

Sport5 = SportCatagory(user_id=1, name="Rock Climbing")
session.add(Sport5)
session.commit()

Sport6 = SportCatagory(user_id=1, name="Foosball")
session.add(Sport6)
session.commit()

Sport7 = SportCatagory(user_id=1, name="Skating")
session.add(Sport7)
session.commit()

Sport8 = SportCatagory(user_id=1, name="Hockey")
session.add(Sport8)
session.commit()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


print "added sports!"