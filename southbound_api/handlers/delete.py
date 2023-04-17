from config import Base, engine

class Delete:

    def delete_db(self):
        Base.metadata.drop_all(engine)
