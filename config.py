POSTGRES_URL = 'localhost'
POSTGRES_USER = 'postgres'
POSTGRES_PASS = '123'
POSTGRES_DB = ''

DB_URI = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PASS, url=POSTGRES_URL, db=POSTGRES_DB)