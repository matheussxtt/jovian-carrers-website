import sqlalchemy as sa
import os
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

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


def load_job_from_db(id):
  with engine.connect() as conn:
    query = "SELECT * FROM jobs WHERE id="
    id = str(id)
    result = conn.execute(sa.text(query + id))
    row = result.fetchone()
    print(dict(row._mapping))
    if row:
      return dict(row._mapping)
    else:
      return None


#alternative: text("select * from jobs where id=:val"),val = id


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    metadata = MetaData()
    applications = Table('applications', metadata, autoload_with=engine)
    ins = applications.insert().values(job_id=job_id,
                                       full_name=data['full_name'],
                                       email=data['email'],
                                       education=data['education'],
                                       linkedin_url=data['linkedin_url'])
    conn.execute(ins)


#SQLAlchemy é ruim demais, voltar aqui na segunda
