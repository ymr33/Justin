import sqlite3

#Open database
conn = sqlite3.connect('user.db')

conn.execute('''drop table if exists users;''')
conn.execute('''create table users (
  username text primary key,
  password text not null
)''')

conn.execute('''drop table if exists user_inf;''')
conn.execute('''create table user_inf(
  watchlist_id integer primary key AUTOINCREMENT,
  username text,
  email TEXT,
  gender TEXT,
  weight INTEGER,
  age INTEGER,
  firstName TEXT,
  lastName TEXT,
  address1 TEXT,
  postcode TEXT,
  city TEXT,
  phone TEXT,
  foreign key(username) references users(username)
    )''')


conn.execute('''insert into users (username,password) values('stn131415','Stn131415~');''')
conn.execute('''insert into user_inf(username,email,gender,weight,age,firstName,lastName,address1,postcode,city,phone) values('stn131415','576664285@qq.com','male','63','25','leo','sun','aa','1111','sydney','047264467');''')
conn.commit()
conn.close()

