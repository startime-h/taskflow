#cat tables.sql | mysql -h 127.0.0.1 --port 3306 -u root -p123456
mysql -h 172.17.0.3 --port 3306 -u root -p123456 < create_db.sql 
mysql -h 172.17.0.3 --port 3306 -u root -p123456 < create_tables.sql
