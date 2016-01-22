drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  date text not null,
  time text not null,
  user text not null,
  likes integer
);

drop table if exists users;
create table users (
  name text not null,
  username text not null,
  password text not null
);