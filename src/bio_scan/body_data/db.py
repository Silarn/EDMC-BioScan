from typing import Optional
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class CommanderData(Base):
    __tablename__ = "commanders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(22), unique=True)


class System(Base):
    __tablename__ = 'systems'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    
    planets: Mapped[list['Planet']] = relationship(
        back_populates="planet", cascade="all, delete-orphan"
    )

    stars: Mapped[list['Star']] = relationship(
        back_populates="star", cascade="all, delete-orphan"
    )


class Planet(Base):
    """ Model for planet data """
    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))
    planet: Mapped[list['System']] = relationship(back_populates='planets')
    name: Mapped[str] = mapped_column(String(32))
    type: Mapped[Optional[str]] = mapped_column(String(32))
    body_id: Mapped[Optional[int]]
    atmosphere: Mapped[Optional[str]] = mapped_column(String(32))
    gasses: Mapped[list['PlanetGas']] = relationship(
        back_populates='gas', cascade='all, delete-orphan'
    )
    volcanism: Mapped[Optional[str]] = mapped_column(String(32))
    distance: Mapped[Optional[float]]
    gravity: Mapped[Optional[float]]
    temp: Mapped[Optional[float]]
    parent_stars: Mapped[list['PlanetParentStar']] = relationship(
        back_populates='star', cascade='all, delete-orphan'
    )
    bio_signals: Mapped[int] = mapped_column(default=0)
    floras: Mapped[list['PlanetFlora']] = relationship(
        back_populates='flora', cascade='all, delete-orphan'
    )
    materials: Mapped[Optional[str]]
    mapped: Mapped[bool] = mapped_column(default=False)


class PlanetGas(Base):
    __tablename__ = 'planet_gasses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    gas: Mapped['Planet'] = relationship(back_populates='gasses')
    gas_name: Mapped[str]
    percent: Mapped[float]


class PlanetParentStar(Base):
    __tablename__ = 'planet_parent_stars'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    star_id: Mapped[int] = mapped_column(ForeignKey('stars.id'))
    star: Mapped['Planet'] = relationship(back_populates='parent_stars')
    priority: Mapped[int]


class PlanetFlora(Base):
    __tablename__ = 'planet_flora'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    flora: Mapped['Planet'] = relationship(back_populates='floras')
    genus: Mapped[str]
    species: Mapped[Optional[str]]
    colors: Mapped[Optional[str]]
    scans: Mapped[int] = mapped_column(default=0)
    __table_args__ = (UniqueConstraint("planet_id", "genus", name="_planet_genus_constraint"),
                      )


class FloraScans(Base):
    __tablename__ = 'flora_scans'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commander_id: Mapped[int] = mapped_column(ForeignKey('commanders.id'))
    flora_id: Mapped[int] = mapped_column(ForeignKey('planet_flora.id'))
    count: Mapped[int] = mapped_column(default=0)
    __table_args__ = (UniqueConstraint('commander_id', 'flora_id', name='_cmdr_flora_constraint'),
                      )


class Star(Base):
    __tablename__ = 'stars'

    """ Holds all attributes, getters, and setters for star data. """
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))
    star: Mapped[list['System']] = relationship(back_populates='stars')
    name: Mapped[str]
    type: Mapped[str] = mapped_column(default='')
    body_id: Mapped[int]
    luminosity: Mapped[str] = mapped_column(default='')