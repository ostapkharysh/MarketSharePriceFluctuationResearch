
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from db_management.DB import Base, Agency, News, db_link



class DatabaseManager:

    def __init__(self, db = None):
        self.Base = db


    def add_agency(self, agency_name):
        engine = create_engine(db_link)  # pool_size=20, max_overflow=0
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

        data = session.query(Agency).all()
        print(data)
        if agency_name in [el.name for el in data]:
            return "There is already a Table with such name: {}".format(agency_name)

        # Insert a Agency in the agency table
        new_agency = Agency(name=agency_name)
        session.add(new_agency)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

        return "The new table {} is created.".format(agency_name)

    def add_news(self, d_t, ttl, ar_txt, lnk, agency_name):
        # Insert an news in the address table

        engine = create_engine(db_link)
        engine.pool_timeout = 60
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        try:

            cur_agency = session.query(Agency).filter_by(name=agency_name).first()
            new_news = News(date_time=d_t, title=ttl, article_text=ar_txt, link=lnk, agency=cur_agency)
            session.add(new_news)
            try:
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()

        except IntegrityError:
            session.rollback()
            return 'The link provided seems to exist in DB: {}'.format(lnk)

        except InvalidRequestError:
            session.rollback()
            return 'You are requesting access to the non-existing source'

        return "The news has been successfully added"