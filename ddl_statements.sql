create table user_ (
	id int auto_increment,
    name_ longtext not null,
    email varchar(30) not null unique,
    password_ text not null,
    phone_number char(11) not null unique,
    address text(30) not null,
    primary key (id)
);

create table publisher(
	id int auto_increment,
    name_ longtext not null,
    primary key (id)
);

create table author(
	id int auto_increment,
    name_ longtext not null,
    primary key (id)
);

create table courses(
	id int auto_increment,
    name_ longtext not null,
    university longtext,
    professor longtext,
    term longtext,
    primary key (id)
);

create table book(
	id int auto_increment,
	number_of_pages int, 
    name_ longtext not null,
    book_image longblob,
    display boolean not null, /* user can create a book and choose not to sell at that moment */
    condition_ int not null, 
    publish_year int not null, 
    publisher_id int not null,
    courses_id int, 
    author_id int not null,
    primary key (id),
    foreign key (publisher_id) references publisher(id) on delete restrict on update cascade,
	foreign key (courses_id) references courses(id) on delete restrict on update cascade,
    foreign key (author_id) references author(id) on delete restrict on update cascade
);

create table price(
	id int auto_increment,
    price float not null,
    date_ datetime not null default current_timestamp,
    book_id int not null,
	primary key (id),
    foreign key (book_id) references book(id) on delete cascade on update cascade
); 

create table wishlist_1 (
	book_id int,
    user_id int, 
    foreign key (book_id) references book(id) on delete cascade,
    foreign key (user_id) references user_(id) on delete cascade
);

create table showcase (
	book_id int,
    user_id int, 
    foreign key (book_id) references book(id) on delete cascade,
    foreign key (user_id) references user_(id) on delete cascade
);


create table wishlist_2 (
	user_id int,
    book_name varchar(30),
    author_name varchar(30),
    foreign key (user_id) references user_(id) on delete cascade
);


create table basket (
	id int auto_increment,
	added_date datetime not null default current_timestamp,
    book_id int, 
    user_id int, 
    is_active boolean default 1,
    primary key (id),
    foreign key (book_id) references book(id) on delete cascade on update cascade,
    foreign key (user_id) references user_(id) on delete cascade on update cascade
);

create table order_ (
	id int auto_increment,
    user_id int, 
    seller_id int,
    price_id int,
    date_ datetime not null default current_timestamp,
    address text(30),
    payment_type varchar(25),
    total_cost float,
    point_ int,
    basket_id int,
    primary key (id),
    foreign key (user_id) references user_(id) on delete cascade,
    foreign key (basket_id) references basket(id) on delete cascade,
    foreign key (price_id) references price(id) on delete cascade on update cascade
);



