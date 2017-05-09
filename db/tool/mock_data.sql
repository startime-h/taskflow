/*
 use test db
 */
use test;

/*
 table: user_info
 */
insert into 
user_info(id, user_id, user_name, user_password_hash,user_email)
values (1, 'user1_id', 'user1', 'user1password', 'user1@gmail.com'),
(2, 'user2_id', 'user2', 'user2password', 'user2@gmail.com'),
(3, 'user3_id', 'user3', 'user3password', 'user3@gmail.com'),
(4, 'user4_id', 'user4', 'user4password', 'user4@gmail.com'),
(5, 'user5_id', 'user5', 'user5password', 'user5@gmail.com');

/*
 table: project_info
 */
insert into 
project_info(id, project_id, project_name, create_user_id, create_time, permission_users)
values 
(1, 1, 'project1', 1, '2017-04-29 00:00:01', '1'),
(2, 2, 'project2', 2, '2017-04-29 00:01:01', '2'),
(3, 3, 'project3', 3, '2017-04-29 00:04:01', '3'),
(4, 4, 'project4', 4, '2017-04-29 00:08:01', '4,2'),
(5, 5, 'project5', 5, '2017-04-29 00:18:01', '5,3');

/*
 table: dag_info
 */
insert into 
dag_info(id, dag_id, dag_name, valid, project_id, create_user_id, create_time, expire_time, scheduler_interval, skip_failed, modify_time, dag_status, next_start_time, dag_json)
values 
(1, 1, 'dag1', 0, 1, 1, '2017-04-29 00:01:01', '2017-08-29 00:00:01', 3600, 0, '2017-04-29 00:01:02', 'NotRunning', '2017-04-29 00:02:01', '{"1":[3], "2":[3], "3":[]}'),
(2, 2, 'dag2', 1, 2, 2, '2017-04-29 00:09:01', '2017-09-29 00:00:01', 600, 1, '2017-04-29 00:09:02', 'NotRunning', '2017-04-29 00:09:01', '{"10":[]}');

/*
 table: task_info
 */
insert into 
task_info(id, dag_id, task_id, task_name, run_machine, run_user, run_dir, run_command, run_timeout, retry_times, task_status, modify_time)
values 
(1, 1, 1, 'task1', '172.17.0.3', 'root', '/home', 'ls -lsrt', 60, 5, 'NotRunning', '2017-04-29 00:00:01'),
(2, 1, 2, 'task2', '172.17.0.4', 'root', '/home', 'ls -lsrt', 60, 5, 'NotRunning', '2017-04-29 00:00:01'),
(3, 1, 3, 'task3', '172.17.0.5', 'root', '/home', 'ls -lsrt', 60, 5, 'NotRunning', '2017-04-29 00:00:01'),
(4, 2, 10, 'task10', '172.17.0.4', 'root', '/home', 'ls -lsrt', 60, 5, 'NotRunning', '2017-04-29 00:00:01');

/*
 tables: macheine_info
 */
insert into 
machine_info(id, machine_name, machine_ip)
values 
(1, 'machine1', '172.17.0.1'),
(2, 'machine2', '172.17.0.2'),
(3, 'machine3', '172.17.0.3'),
(4, 'machine4', '172.17.0.4'),
(5, 'machine5', '172.17.0.5');

/*
 table: dag_run_history
 */
insert into 
dag_run_history(id, dag_id, start_time, end_time, status)
values 
(1, 1, '2017-04-29 00:00:01', '2017-04-29 00:04:00', 'Terminated'),
(2, 2, '2017-04-29 01:00:01', '2017-04-29 08:04:00', 'Terminated');

/*
 table: task_run_history
 */
insert into 
task_run_history(id, task_id, start_time, end_time, status, stdout, stderr)
values 
(1, 1, '2017-04-29 00:00:01', '2017-04-29 01:00:00', 'Terminated', 'stdout', ''),
(2, 2, '2017-04-29 00:00:01', '2017-04-29 01:00:00', 'Terminated', 'stdout', ''),
(3, 3, '2017-04-29 00:00:01', '2017-04-29 01:00:00', 'Terminated', 'stdout', ''),
(4, 10, '2017-04-29 00:00:01', '2017-04-29 01:00:00', 'Terminated', 'stdout', '');
