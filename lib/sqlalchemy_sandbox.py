#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine,desc,Index,Column,DateTime,Integer,String,func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base=declarative_base()

class Student(Base):
    __tablename__='students'

    id = Column(Integer(),primary_key=True)
    name=Column(String())
    email=Column(String(55))
    grade=Column(Integer())
    birthday=Column(DateTime())
    enrolled_date=Column(DateTime(),default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: "\
                + f"{self.name}, "\
                + f"Grade {self.grade}"
                

if __name__== '__main__':
    engine=create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session=sessionmaker(bind=engine)

    session=Session()

    albert_einstein=Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )
    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )
    eve_johnson=Student(
        name="Eve Johnson",
        email="eve.johnson@eden.edu",
        grade=10,
        birthday=datetime(
            year=1910,
            month=3,
            day=31
        ),
    )

    

    session.bulk_save_objects([eve_johnson,alan_turing,albert_einstein])

    # TEMPORARY ADD GRADE
    # for student in session.query(Student):
    #     student.grade += 1

    #ADD GRADE AND UPDARE
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    session.commit()

#READ RECORDS
    names = session.query(Student.name).all()

#ORDERING
    student_by_name=session.query(
        Student.name,Student.grade).order_by(
            desc(Student.grade)).all()
#LIMITING
    oldest_student = session.query(
            Student.name, Student.birthday).order_by(
            Student.birthday).first()#limit(1).all()

    student_count = session.query(func.count(Student.id)).first()

#FILTERING
    # query = session.query(Student).filter(Student.name.like('%Alan%'),
    #     Student.grade == 11).all()

    # for record in query:
    #     print(record.name)

#PRINT
    # print([(student.name,
    #     student.grade) for student in session.query(Student)])

#DELETION
    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")

    query.delete()

    albert_einstein = query.first()

    print(albert_einstein)

