## 1.user info
CREATE TABLE user_info (  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id   INT NOT NULL AUTO_INCREMENT,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user_name VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user_password_hash VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user_email VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;register_time datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id)  
);  
  
id: 主键id  
user_name: 用户名称  
user_password_hash: 用户密码加密  
user_email: 用户邮箱  
register_time: 注册时间  

## 2.project_info  
CREATE TABLE project_info (  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id   INT NOT NULL AUTO_INCREMENT,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;project_name VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;create_user_id INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;create_time  datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;project_desc VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;permission_users VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id)  
);  

id: 主键id  
project_name: 项目名称  
create_uesr_id: 创建用户id  
create_time: 创建时间  
project_desc: 项目描述  
permission_users: 有权限用户列表  

## 3.dag_info  
CREATE TABLE dag_info  (  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id   INT NOT NULL AUTO_INCREMENT,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dag_id  INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dag_name VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;valid INT NOT NULL default 0,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;project_name INT NOT NULL,   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;create_user_id INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;create_time datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;scheduler_interval  INT NOT NULL,    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;skip_failed INT NOT NULL default 0,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;modify_time datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dag_status VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;next_start_time datetime NOT NULL,   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dag_json VARCHAR(2048) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id)  
);  

id: 主键id  
dag_id: dag id，不重复，后台生成  
dag_name: dag 名称  
valid: 是否有效, 1表示有效，0表示无效  
project_name: 所属project名称
create_user_id: 创建用户id  
create_time: 创建时间  
scheduler_interval: 调度周期  
skip_failed: 是否跳过failed节点 定期调度  
modify_time: dag更新时间  
dag_status: dag状态  Not Running／Running／Failed／Terminted  
next_start_time: 下一次启动时间  
dag_json: dag json描述

## 4.task_info  
CREATE TABLE task_info (  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id   INT NOT NULL AUTO_INCREMENT,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dag_id INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;task_id INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;task_name VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;run_machine VARCHAR(255) NOT NULL,    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;run_user VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;run_dir VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;run_command  VARCHAR(2048) NOT NULL,   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;run_timeout  INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;retry_times INT NOT NULL default 1,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;task_status  VARCHAR(255) NOT NULL,   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;modify_time datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id)  
);  

id：task id，自增  
dag_id：所属dag id  
task_id:  task id, 不重复，后台自动生成  
task_name: task 名称  
run_machine: 运行机器  
run_user: 运行用户，root还是一般用户  
run_command: 运行命令  
run_timeout: 运行超时时间  
retry_times: 重试次数  
task_status: task 状态  Not Running／Running／Failed／Terminted
modiry_time: task 更新时间

## 5.machine_info  
CREATE TABLE machine_info (  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id   INT NOT NULL AUTO_INCREMENT,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;machine_name VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;machine_ip VARCHAR(255) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id)  
);  

id: 主键id  
machine_name: 机器名称  
machine_ip: 机器ip地址  

## 6.dag_run_history  
CREATE TABLE dag_run_history (  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id   INT NOT NULL AUTO_INCREMENT,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dag_id  VARCHAR(255) NOT NULL,      
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;start_time datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;end_time datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;status  VARCHAR(255) NOT NULL,     
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id)  
);  

id：主键id，自增  
dag_id：dag id  
start_time：dag 启动时间  
end_time：dag 结束时间  
status：dag 状态  Failed／Terminted  

## 7.task_run_history  
CREATE TABLE task_run_history (  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id   INT NOT NULL AUTO_INCREMENT,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;task_id INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;start_time datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;end_time datetime NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;status VARCHAR(255) NOT NULL,     
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY (id)  
);  

id：task id，自增  
task_id：task id  
start_time：启动时间  
end_time：结束时间  
status：task 状态, Failed／Terminted

## 8.task_pending_queue
CREATE TABLE task_pending_queue (  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;task_id INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;machine_ip VARCHAR(255) NOT NULL  
);  

id：task id，自增  
machine_ip: machine ip address  
