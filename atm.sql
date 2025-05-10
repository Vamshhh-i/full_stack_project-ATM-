create database atm;
use atm;
drop table accounts;
create table ACCOUNTS(
 user_accno int,
 user_name varchar(40),
 user_email varchar(30),
 user_pin int,
 user_balance int
);
insert into ACCOUNTS values
(1001,"Katharasala Vamshi","vamshi19100@gmail.com",1234,10000),
    (1002,"Nuthakki Mahitha Choudary","nuthakimahitha16@gmail.com",5678,12000),
    (1003,"Harshitha chowdary","harshhh@gmail.com",Null,70000),
    (1004,"M varsha ","varsha1470@gmail.com",Null,20000);
select * from accounts;