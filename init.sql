Create table idc(
	id int not null auto_increment primary key,
	name varchar(200),
	msg varchar(200)
);

Create table mac(
	id int not null auto_increment primary key,
	name varchar(200),
	ip varchar(200),
	port int,
	idc_id varchar(200),
	disk int,
	msg varchar(200)

);