use test;

drop table if exists user_info;
CREATE TABLE user_info (
    id   INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

drop table if exists project_info;
CREATE TABLE project_info (
    id   INT NOT NULL AUTO_INCREMENT,
    project_id INT NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    create_user_id INT NOT NULL,
    create_time  datetime NOT NULL,
    permission_users VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

drop table if exists dag_info;
CREATE TABLE dag_info  (
    id   INT NOT NULL AUTO_INCREMENT,
    dag_id  INT NOT NULL,
    dag_name VARCHAR(255) NOT NULL,
    valid INT NOT NULL default 0,
    project_id INT NOT NULL, 
    create_user_id INT NOT NULL,
    create_time datetime NOT NULL,
    expire_time datetime NOT NULL,
    scheduler_interval  INT NOT NULL,  
    skip_failed  INT NOT NULL,  
    modify_time datetime NOT NULL,
    dag_status  INT NOT NULL,  
    next_start_time datetime NOT NULL, 
    head_tasks_list VARCHAR(2048) NOT NULL,
    PRIMARY KEY (id)
);

drop table if exists task_info;
CREATE TABLE task_info (
    id   INT NOT NULL AUTO_INCREMENT,
    dag_id INT NOT NULL,
    task_id INT NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    run_machine VARCHAR(255) NOT NULL,  
    run_user VARCHAR(255) NOT NULL,
    run_dir VARCHAR(255) NOT NULL,
    run_command  VARCHAR(2048) NOT NULL, 
    run_timeout  INT NOT NULL,   
    retry_times INT NOT NULL default 1,
    task_status  INT NOT NULL default 0,  
    modify_time datetime NOT NULL,
    pre_task_list  VARCHAR(2048) NOT NULL,
    next_task_list  VARCHAR(2048) NOT NULL,
    PRIMARY KEY (id)
);

drop table if exists machine_info;
CREATE TABLE machine_info (
    id   INT NOT NULL AUTO_INCREMENT,
    machine_name VARCHAR(255),
    machine_ip VARCHAR(255),
    PRIMARY KEY (id)
);

drop table if exists dag_run_history;
CREATE TABLE dag_run_history (
    id   INT NOT NULL AUTO_INCREMENT,
    dag_id  INT NOT NULL,         
    start_time datetime NOT NULL,
    end_time datetime NOT NULL,
    status  INT NOT NULL default 3,   
    PRIMARY KEY (id)
);

drop table if exists task_run_history;
CREATE TABLE task_run_history (
    id   INT NOT NULL AUTO_INCREMENT,
    task_id  INT NOT NULL,         
    start_time datetime NOT NULL,
    end_time datetime NOT NULL,
    status  INT NOT NULL default 3,   
    PRIMARY KEY (id)
);

drop table if exists task_pending_queue;
CREATE TABLE task_pending_queue (
    id   INT NOT NULL AUTO_INCREMENT,
    task_id INT NOT NULL, 
    machine_ip  VARCHAR(255)  NOT NULL,
    status VARCHAR(255) NOT NULL,   
    PRIMARY KEY (id)
);
