from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, String, Integer, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('mysql+mysqlconnector://root:123456a@127.0.0.1:3306/test')
Session = sessionmaker(bind=engine)
session = Session()


class Vod(Base):
    # 表名
    __tablename__ = 'vod'

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(200))

    cover = Column(Text)

    intro = Column(Text)

    downloads = relationship('Download', backref='vod')

    play_bilibili = relationship('Play', uselist=False, backref='vod')

    actors = relationship('Actor', secondary='vod2actor', backref='vods')


class Actor(Base):
    # 表名
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(40))

    avatar = Column(Text)


# 一对一
class Play(Base):
    # 表名
    __tablename__ = 'play'

    id = Column(Integer, primary_key=True, autoincrement=True)

    url = Column(Text)

    vod_id = Column(Integer, ForeignKey('vod.id'))


# 一对多
class Download(Base):
    # 表名
    __tablename__ = 'download'

    id = Column(Integer, primary_key=True, autoincrement=True)

    url = Column(Text)

    # 迅雷/磁力/百度云
    type = Column(Text(20))

    vod_id = Column(Integer, ForeignKey('vod.id'))


# 多对多关系-中间表
class Vod2Actor(Base):
    # 表名
    __tablename__ = 'vod2actor'

    id = Column(Integer, primary_key=True, autoincrement=True)

    vod_id = Column(Integer, ForeignKey('vod.id'))

    actor_id = Column(Integer, ForeignKey('actor.id'))


def get_actors_by_vod_title(title):
    vod = session.query(Vod).filter_by(title=title).first()
    if vod:
        vod2Actors = session.query(Vod2Actor).filter_by(vod_id=vod.id).all()
        actors = [session.query(Actor).filter_by(id=item.actor_id).first() for item in vod2Actors]
        print('[get_actors_by_title]:%s' % actors)
        return actors
    return None


def get_actors_by_vod_title_with_relationship(title):
    vod = session.query(Vod).filter_by(title=title).first()
    if vod:
        actors = vod.actors
        print('[get_actors_by_title_with_relationship]:%s' % actors)
        return actors
    return None


def get_vods_by_actor_name_with_backref(name):
    actor = session.query(Actor).filter_by(name=name).first()
    if actor:
        vods = actor.vods
        print('[get_vods_by_actor_name_with_relationship]:%s' % vods)
        return vods
    return None


def get_play_by_vod_id_with_relationship(vid):
    vod = session.query(Vod).filter_by(id=vid).first()
    if vod:
        play = vod.play_bilibili
        print('[get_play_by_vod_id]:%s' % play)
        return play
    return None


def get_vod_by_play_id_with_backref(pid):
    play = session.query(Play).filter_by(id=pid).first()
    if play:
        vod = play.vod
        print('[get_vod_by_play_id]:%s' % vod)
        return vod
    return None


def get_downloads_by_vod_id_with_relationship(vid):
    vod = session.query(Vod).filter_by(id=vid).first()
    if vod:
        downloads = vod.downloads
        print('[get_downloads_by_vod_id]:%s' % downloads)
        return downloads
    return None


def get_vod_by_download_id_with_backref(did):
    download = session.query(Download).filter_by(id=did).first()
    if download:
        vod = download.vod
        print('[get_vod_by_download_id]:%s' % vod)
        return vod
    return None


def get_vod(vid):
    return session.query(Vod).filter_by(id=vid).first()


def insert_vod(vod):
    session.add(vod)
    session.commit()
    return vod


def delete_vod(vod):
    session.delete(vod)
    session.commit()


def update_vod(vod):
    # merge方法会通过主键值来判断当前实例是否存在于数据库中，如果存在，则更新; 否则新建
    # add方法则仅仅是新建
    session.merge(vod)
    session.commit()


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


def close_session():
    session.close()
