import sqlalchemy as sa
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

connect_args = {"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}}

engine = sa.create_engine(db_connection_string, connect_args=connect_args)


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(sa.text("select * from jobs"))
    print("type(result): ", type(result))

    jobs = []
    for row in result.all():
      jobs.append(row._mapping)
    return jobs
