insert into groups (group_id, user_name, group_name, date_created) values(DEFAULT, null, 'public', now());
insert into groups (group_id, user_name, group_name, date_created) values(DEFAULT, null, 'private', now());
insert into users(user_name, password, date_registered) values('admin', 'admin', now());
