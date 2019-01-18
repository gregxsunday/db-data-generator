delete from Country
DBCC CHECKIDENT (Country, RESEED, 0)
insert into Country (name)
values
('Poland'),
('Germany'),
('Czech Republic'),
('Russia'),
('Ukraine');

select * from Country