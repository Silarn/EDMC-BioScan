"""
The database structure models and helper functions for BioScan data
"""
from typing import Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint, select, Column, Float, Engine, text, SmallInteger, \
    Table, MetaData
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.ddl import CreateTable

from EDMCLogging import get_plugin_logger

db_version: int = 2
logger = get_plugin_logger('BioScan')


class Base(DeclarativeBase):
    pass


class Commander(Base):
    __tablename__ = 'commanders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(22), unique=True)


class Metadata(Base):
    __tablename__ = 'metadata'

    key: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    value: Mapped[str] = mapped_column(nullable=False, default='')


class System(Base):
    """ DB model for system data """
    __tablename__ = 'systems'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    x: Mapped[float] = mapped_column(default=0.0)
    y: Mapped[float] = mapped_column(default=0.0)
    z: Mapped[float] = mapped_column(default=0.0)
    region: Mapped[Optional[int]] = mapped_column(SmallInteger)

    planets: Mapped[list['Planet']] = relationship(
        back_populates='planet', cascade='all, delete-orphan'
    )

    stars: Mapped[list['Star']] = relationship(
        back_populates='star', cascade='all, delete-orphan'
    )


class Planet(Base):
    """ DB model for planet data """
    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))
    planet: Mapped[list['System']] = relationship(back_populates='planets')
    name: Mapped[str] = mapped_column(String(32))
    type: Mapped[str] = mapped_column(String(32), default='')
    body_id: Mapped[int]
    atmosphere: Mapped[str] = mapped_column(String(32), default='')
    gasses: Mapped[list['PlanetGas']] = relationship(
        back_populates='gas', cascade='all, delete-orphan'
    )
    volcanism: Mapped[Optional[str]] = mapped_column(String(32))
    distance: Mapped[float] = mapped_column(default=0.0)
    gravity: Mapped[float] = mapped_column(default=0.0)
    temp: Mapped[Optional[float]]
    parent_stars: Mapped[str] = mapped_column(default='')
    bio_signals: Mapped[int] = mapped_column(default=0)
    floras: Mapped[list['PlanetFlora']] = relationship(
        back_populates='flora', cascade='all, delete-orphan'
    )
    materials: Mapped[str] = mapped_column(default='')
    mapped: Mapped[bool] = mapped_column(default=False)


class PlanetGas(Base):
    __tablename__ = 'planet_gasses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    gas: Mapped['Planet'] = relationship(back_populates='gasses')
    gas_name: Mapped[str]
    percent: Mapped[float]

    def __repr__(self) -> str:
        return f'PlanetGas(gas_name={self.gas_name!r}, percent={self.percent!r})'


class PlanetFlora(Base):
    __tablename__ = 'planet_flora'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    flora: Mapped['Planet'] = relationship(back_populates='floras')
    scans: Mapped[list['FloraScans']] = relationship(back_populates='scan', cascade='all, delete-orphan')
    waypoints: Mapped[list['Waypoint']] = relationship(back_populates='waypoint', cascade='all, delete-orphan')
    genus: Mapped[str]
    species: Mapped[str] = mapped_column(default='')
    color: Mapped[str] = mapped_column(default='')
    __table_args__ = (UniqueConstraint('planet_id', 'genus', name='_planet_genus_constraint'),
                      )


class FloraScans(Base):
    __tablename__ = 'flora_scans'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commander_id: Mapped[int] = mapped_column(ForeignKey('commanders.id'))
    flora_id: Mapped[int] = mapped_column(ForeignKey('planet_flora.id'))
    scan: Mapped['PlanetFlora'] = relationship(back_populates='scans')
    count: Mapped[int] = mapped_column(default=0)
    __table_args__ = (UniqueConstraint('commander_id', 'flora_id', name='_cmdr_flora_constraint'),
                      )


class Waypoint(Base):
    __tablename__ = 'flora_waypoints'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commander_id: Mapped[int] = mapped_column(ForeignKey('commanders.id'))
    flora_id: Mapped[int] = mapped_column(ForeignKey('planet_flora.id'))
    waypoint: Mapped['PlanetFlora'] = relationship(back_populates='waypoints')
    type: Mapped[str] = mapped_column(nullable=False, default='tag')
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)


class Star(Base):
    """ DB model for star data """
    __tablename__ = 'stars'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))
    star: Mapped[list['System']] = relationship(back_populates='stars')
    name: Mapped[str] = mapped_column(nullable=False)
    body_id: Mapped[int] = mapped_column(nullable=False)
    distance: Mapped[float] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(default='')
    luminosity: Mapped[str] = mapped_column(default='')


class CodexScans(Base):
    __tablename__ = 'codex_scans'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commander_id: Mapped[int] = mapped_column(ForeignKey('commanders.id'))
    region: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    biological: Mapped[str] = mapped_column(nullable=False, default='')
    __table_args__ = (UniqueConstraint('commander_id', 'region', 'biological', name='_cmdr_bio_region_constraint'),)


class JournalLog(Base):
    __tablename__ = 'journal_log'

    journal: Mapped[str] = mapped_column(String(32), primary_key=True)


def modify_table(engine: Engine, table: type[Base]):
    new_table_name = f'{table.__tablename__}_new'
    connection = engine.connect()
    connection.execute(text(f'PRAGMA foreign_keys=off'))
    connection.commit()
    metadata = MetaData()
    columns: list[Column] = [column.copy() for column in table.__table__.columns.values()]
    args = []
    if hasattr(table, '__table_args__'):
        for arg in table.__table_args__:
            if type(arg) == UniqueConstraint:
                args.append(arg.copy())
            else:
                args.append(arg)
    new_table = Table(new_table_name, metadata, *columns, *args)
    statement = text(str(CreateTable(new_table).compile(engine)))
    connection.execute(statement)
    statement = text(f'INSERT INTO `{new_table_name}` SELECT * FROM `{table.__tablename__}`')
    connection.execute(statement)
    statement = text(f'DROP TABLE `{table.__tablename__}`')
    connection.execute(statement)
    statement = text(f'ALTER TABLE `{new_table_name}` RENAME TO `{table.__tablename__}`')
    connection.execute(statement)
    connection.commit()
    connection.execute(text(f'PRAGMA foreign_keys=on'))
    connection.commit()
    connection.close()


def add_column(engine: Engine, table_name: str, column: Column):
    connection = engine.connect()
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    statement = text(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}')
    connection.execute(statement)
    connection.close()


def migrate(engine: Engine) -> None:
    """
    Database migration function. Checks existing DB version, runs any necessary migrations, and sets the new version
    in the metadata.

    :param engine: DB connection engine object
    """

    connection = engine.connect()
    version = connection.execute(select(Metadata).where(Metadata.key == 'version')).mappings().first()
    connection.close()
    try:
        if version:  # If the database version is set, perform migrations
            if int(version['value']) < 2:
                add_column(engine, 'systems', Column('x', Float(), default=0.0))
                add_column(engine, 'systems', Column('y', Float(), default=0.0))
                add_column(engine, 'systems', Column('z', Float(), default=0.0))
                add_column(engine, 'systems', Column('region', SmallInteger(), nullable=True))
                add_column(engine, 'stars', Column('distance', Float(), nullable=True))
                modify_table(engine, Star)
                modify_table(engine, Planet)
    except Exception as ex:
        logger.debug('Problem during migration', exc_info=ex)

    connection = engine.connect()
    connection.execute(insert(Metadata).values(key='version', value=db_version)
                       .on_conflict_do_update(index_elements=['key'], set_=dict(value='db_version')))
    connection.close()
