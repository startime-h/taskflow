## Running Docker
  测试环境为了使用mysql我们可以用docker mysql镜像来使用mysql
  1. build: 基于mysql镜像构建新的镜像
            [mysql](https://github.com/chenguolin/docker/tree/master/mysql)
  2. 为了方便测试, 我们启动mysql容器的时候设置--net=container 模式
  3. run: docker run -d --net=container:xxx --name mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:v1 
  4. mysql 默认的port=3306, user=root
  5. execute sql: [run_sql.sh](https://github.com/chenguolin/nbflow/blob/master/db/tool/run_sql.sh)
  
  注意：docker容器默认情况下网络模式为bridge，IP地址会动态变化。但是有些时候希望绑定固定的IP地址给docker容器，可以通过[set_docker_ip](https://github.com/chenguolin/docker/blob/master/set_docker_ip.sh)
