create table downloads (
  country       varchar(250),
  product       varchar(50),
  download_date date,
  amount        int,
  unique (country, product, download_date)
);

insert into downloads (country, product, download_date, amount)
values ('Russia', 'AppCode', '2014-01-01', 234),
  ('Russia', 'PyCharm', '2014-01-01', 532),
  ('Japan', 'RubyMine', '2015-10-01', 62),
  ('Germany', 'ReSharper', '2015-05-05', 1200);


create table customers (
  id      int primary key,
  name    varchar(250),
  country varchar(250)
);

insert into customers (id, name, country)
values (100, 'Vasya Pupkin', 'Russia'),
  (101, 'John Snow', 'United Kingdom'),
  (102, 'Apple', 'United States of America'),
  (103, 'Google', 'United States of America');


create table orders (
  id          int primary key,
  customer_id int references customers,
  order_date  date
);

insert into orders (id, customer_id, order_date)
values (543, 100, '2012-02-02'),
  (544, 101, '2012-02-02'),
  (545, 102, '2012-02-02'),
  (546, 103, '2012-02-03');

create table purchases
(
  id           int primary key,
  order_id     int references orders,
  product      varchar(50),
  price        decimal(10, 2),
  quantity     int,
  discount     decimal(10, 2),
  total_amount decimal(10, 2)
);

insert into purchases (id, order_id, product, price, quantity, discount, total_amount)
values (1001, 543, 'ReSharper', 200, 2, 0, 400),
  (1002, 543, 'IntelliJ Idea', 200, 1, 0, 200),
  (1003, 544, 'RubyMine', 100, 1, 0, 100);
;

select sum(amount)
from downloads
where country = 'Russia';


select sum(total_amount)
from purchases p
  join orders o on p.order_id = o.id
  join customers c on c.id = o.customer_id
where country = 'Russia' and extract(year from order_date) = 2012;


create table events (
  id                int primary key,
  title             varchar(200),
  named_entity1     varchar(300),
  named_entity2     varchar(300),
  action            varchar(200),
  place             varchar(200),
  event_start_date  date,
  event_finish_date date
);

insert into events (id, title, named_entity1, named_entity2, action, place, event_start_date, event_finish_date)
values (1, 'JetBrains released DataGrip 1.0', 'JetBrains', 'DataGrip', 'released', null, '2015-11-10', null),
  (2, 'Microsoft bought Xamarin', 'Microsoft', 'Xamarin', 'bought', null, '2016-02-15', null);

select min(event_start_date) from events where named_entity2 = 'DataGrip' and action = 'released';
