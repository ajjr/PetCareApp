-- Event date should be a timestamp
alter table event alter column date type timestamp using date::timestamp;
alter table event alter column date set default current_timestamp;
alter table event alter column add_timestamp set default current_timestamp;