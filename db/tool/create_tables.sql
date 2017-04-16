use test;

CREATE TABLE IF NOT EXISTS flow_user_info (
    id   INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS flow_dag  (
    id   INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    is_valid INT NOT NULL,
    project VARCHAR(255) NOT NULL,   
    owner  VARCHAR(255) NOT NULL,
    scheduler_interval  INT NOT NULL,  
    create_time datetime NOT NULL,
    expire_time datetime NOT NULL, 
    skip_failed  INT NOT NULL,  
    status  VARCHAR(255) NOT NULL,
    next_start_time datetime NOT NULL, 
    dag_json VARCHAR(2048) NOT NULL,
    last_modify_time datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS flow_task (
    id   INT NOT NULL AUTO_INCREMENT,
    dag_id INT NOT NULL,   
    name VARCHAR(255) NOT NULL,
    status  VARCHAR(255) NOT NULL,
    run_machine VARCHAR(255) NOT NULL,  
    run_user VARCHAR(255) NOT NULL,
    run_dir VARCHAR(255) NOT NULL,
    run_command  VARCHAR(2048) NOT NULL, 
    run_timeout  INT NOT NULL,   
    retry_times INT NOT NULL,     
    last_modify_time datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS flow_dag_history (
    id   INT NOT NULL AUTO_INCREMENT,
    dag_id INT NOT NULL,   
    start_time datetime NOT NULL,
    end_time datetime NOT NULL,
    status  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS flow_task_history (
    id   INT NOT NULL AUTO_INCREMENT,
    dag_id INT NOT NULL,   
    task_id INT NOT NULL,   
    start_time datetime NOT NULL,
    end_time datetime NOT NULL,
    status  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS flow_machine_group (
    id   INT NOT NULL AUTO_INCREMENT,
    group_name VARCHAR(255) NOT NULL,
    machine   VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
