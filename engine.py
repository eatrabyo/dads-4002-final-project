from sqlalchemy import create_engine


def mysql_engine(user, passw, host, port, database):
    engine = create_engine('mysql+pymysql://' + user + ':' + passw +
                           '@' + host + ':' + str(port) + '/' + database, echo=False)
    return engine
