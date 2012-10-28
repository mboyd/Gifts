drop table if exists users;
create table users (
	id integer primary key autoincrement,
	name string not null,
	email string not null,
	pw_hash string not null,
	pw_salt string not null
);

drop table if exists gifts;
create table gifts (
	id integer primary key autoincrement,
	user_id integer not null,
	title string not null,
	url string not null,
	price integer not null,
	desc string
);

insert into users (id, name, email, pw_hash, pw_salt) values (1, "Merritt", "mboyd", "HASHSALT", "SALT");
insert into users (id, name, email, pw_hash, pw_salt) values (2, "Emily", "eboyd", "HASHSALT", "SALT");
insert into users (id, name, email, pw_hash, pw_salt) values (3, "Forrest", "eboyd", "HASHSALT", "SALT");
insert into users (id, name, email, pw_hash, pw_salt) values (4, "Mom", "eboyd", "HASHSALT", "SALT");
insert into users (id, name, email, pw_hash, pw_salt) values (5, "Dad", "eboyd", "HASHSALT", "SALT");


insert into gifts (user_id, title, url, price, desc) values (1, "Foo", "http://foo.com", 50, "It's a foo");
insert into gifts (user_id, title, url, price, desc) values (1, "Bar construction kit", "http://foo.com", 10, "It's a foo");

insert into gifts (user_id, title, url, price, desc) values (2, "Pony (shetland, female)", "http://foo.com", 1000, "It's a foo");
insert into gifts (user_id, title, url, price, desc) values (2, "Tony Hawk's totally radical skateboard, dude", "http://foo.com", 85, "It's a foo");