from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='task')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def show_today_tasks():
    today = datetime.today().date()
    rows = session.query(Table).filter(Table.deadline == today).all()
    print(f"Today: {today.day} {today.strftime('%b')}")
    if rows:
        for x in rows:
            print(f"{x.id}. {x}")
        print()
    else:
        print("Nothing to do!\n")


def show_week_tasks():
    today = datetime.today().date()
    for i in range(0, 7):
        rows = session.query(Table).filter(Table.deadline == (today + timedelta(days=i))).order_by(Table.deadline).all()
        i_day = today + timedelta(days=i)
        print(f"\n{i_day.strftime('%A')} {i_day.day} {i_day.strftime('%b')}")
        if rows:
            for x in range(1, len(rows) + 1):
                print(f"{x}. {rows[x - 1]}")
            print()
        else:
            print("Nothing to do!\n")


def show_all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    print("\nAll tasks:")
    for x in range(1, len(rows) + 1):
        print(f"{x}. {rows[x - 1]}. {rows[x - 1].deadline.day} {rows[x - 1].deadline.strftime('%b')}")
    print()


def missed_tasks():
    today = datetime.today().date()
    rows = session.query(Table).filter(Table.deadline < today).all()
    print('\nMissed tasks:')
    if rows:
        for i in range(1, len(rows) + 1):
            print(i, rows[i - 1])
        print()
    else:
        print('Nothing is missed!\n')


def add_task():
    task = input("\nEnter task\n")
    date_string = input("Enter deadline\n")
    row = Table(task=task, deadline=datetime.strptime(date_string, "%Y-%m-%d"))
    session.add(row)
    session.commit()
    print("The task has been added!\n")


def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    print("\nChose the number of the task you want to delete:\n")
    for x in range(1, len(rows) + 1):
        print(f"{x}. {rows[x - 1]}. {rows[x - 1].deadline.day} {rows[x - 1].deadline.strftime('%b')}")
    specific_row = rows[int(input()) - 1]
    session.delete(specific_row)
    session.commit()
    print('The task has been deleted!\n')


while True:
    print("1) Today's tasks\n"
          "2) Week's tasks\n"
          "3) All tasks\n"
          "4) Missed tasks\n"
          "5) Add task\n"
          "6) Delete task\n"
          "0) Exit")
    option = int(input())
    if option == 1:
        show_today_tasks()
    if option == 2:
        show_week_tasks()
    if option == 3:
        show_all_tasks()
    elif option == 4:
        missed_tasks()
    elif option == 5:
        add_task()
    elif option == 6:
        delete_task()
    elif option == 0:
        exit()
