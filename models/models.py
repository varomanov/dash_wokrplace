from sqlalchemy import create_engine, ForeignKey, String, Date, DateTime, Integer, Boolean, select
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, Session
from sqlalchemy.sql import func
from datetime import date, datetime, timedelta
from typing import List, Optional

engine = create_engine('sqlite:///booking.db')


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = 'persons'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(50))
    created: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp()
    )
    updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp()
    )

    bookings: Mapped[List['Booking']] = relationship(back_populates='person')


class Place(Base):
    __tablename__ = 'places'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    place: Mapped[str] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp()
    )
    updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp()
    )

    bookings: Mapped[List['Booking']] = relationship(back_populates='place')


class Booking(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    place_id: Mapped[int] = mapped_column(ForeignKey('places.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey('persons.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    booked_date: Mapped[date] = mapped_column(Date, nullable=True)
    is_free: Mapped[bool] = mapped_column(Boolean, default=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp()
    )
    updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp()
    )

    person: Mapped['Person'] = relationship(back_populates='bookings')
    place: Mapped['Place'] = relationship(back_populates='bookings')


def get_users():
    with Session(engine) as session:
        stmt = select(Person).order_by(Person.fullname.asc())
        return [x.fullname for x in session.execute(stmt).scalars()]
    

if __name__ == '__main__':

    # добавить сотрудников и места
    with Session(engine) as session:
        person_lst = [
            {'name': 'Vladimir Romanov', 'email': 'vladimirromanov@mailcom', 'department': 'Sales'},
            {'name': 'Sergey Petrov', 'email': 'sergeypetrov@mailcom', 'department': 'HR'},
            {'name': 'Olga Safonova', 'email': 'olgasafonova@mailcom', 'department': 'Marketing'},
            {'name': 'Egor Ershov', 'email': 'egorershov@mailcom', 'department': 'Research'},
            {'name': 'Oleg Sverdlov', 'email': 'olegsverdlov@mailcom', 'department': 'SFE'},
        ]

        places_lst = [
            {'place': '827/01', 'is_active': True},
            {'place': '827/02', 'is_active': True},
            {'place': '827/03', 'is_active': True},
            {'place': '827/04', 'is_active': True},
            {'place': '827/05', 'is_active': False},
            {'place': '827/06', 'is_active': True},
            {'place': '827/07', 'is_active': True},
            {'place': '827/08', 'is_active': False},
            {'place': '827/09', 'is_active': True},
            {'place': '827/10', 'is_active': True},
            {'place': '827/11', 'is_active': True},
            {'place': '827/12', 'is_active': True},
        ]

        for person in person_lst:
            new_person = Person(fullname=person['name'], email=person['email'], department=person['department'])
            session.add(new_person)
            # session.commit()

        for place in places_lst:
            new_place = Place(place=place['place'], is_active=place['is_active'])
            session.add(new_place)
            # session.commit()
    
        for d in range(0, 15):
            all_places = session.execute(select(Place)).scalars()
            for p in all_places:
                fill_booking = Booking(place_id=p.id, booked_date=datetime.today() + timedelta(0))
                session.add(fill_booking)
                # session.commit()
