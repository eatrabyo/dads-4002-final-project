from sqlalchemy import create_engine
from omegaconf import OmegaConf


def mysql_engine(user, passw, host, port, database):
    engine = create_engine('mysql+pymysql://' + user + ':' + passw +
                           '@' + host + ':' + str(port) + '/' + database, echo=False)
    return engine


# load config
conf = OmegaConf.load('config.yaml')

main_db = mysql_engine(conf.user_local, conf.passw_local, conf.host_local,
                       conf.port_local, conf.database_local)
