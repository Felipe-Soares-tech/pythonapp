create table todolist(
"_lineNumber" serial primary key,
item varchar(250),
status varchar(100)
);

insert into todolist(item, status) values('Comprar Pão', 'Iniciado');

select * from todolist;

