import os
import sqlalchemy

basedir = os.path.dirname(__file__)
database_file_path = os.path.join(basedir, "instance", "proj.sqlite3")
engine = sqlalchemy.create_engine(f"sqlite:///{'/Users/admin/Documents/practice3/vue3/Books/server/instance/proj.sqlite3'}")

try:
    engine.connect()
except sqlalchemy.exc.OperationalError as e:
    print(e)
    exit(1)

print("Database connection is working correctly.")



    