function getDags(user_id) {
   //console.log(user_id); 
   //ajax post get user id dags
   var post_data = {
       "user_id": user_id 
   };
   $.ajax({
       type: "POST",
       url: "/dags/get_projects",
       contentType: "application/json; charset=utf-8",
       data: JSON.stringify(post_data),
       dataType: "json",
       success: function(data){  
            //console.log(data);
            var nav_side_dag_div = document.getElementById("nav-side-dags");
            var inner_html = ''
            for (var i = 0; i < data.length; i++) {
                var project_dict = data[i];
                var project_name = project_dict.project;
                var dag_list = project_dict.dag_list;
                inner_html += '<ul class="current">'
                inner_html += '<li class="toctree-l1 current"><a class="current reference internal" href="#"><span class="toctree-expand"></span>' + project_name + '</a>'
                inner_html += '<ul>'
                for (var j = 0; j < dag_list.length; j++) {
                    var dag_name = dag_list[j]
                    inner_html += '<li class="toctree-l2"><a class="reference internal" href="#dags-view">'+ dag_name + '</a></li>'
                }
                inner_html += '</ul>'
                inner_html += '</ul>'
            }; 
            //console.log(inner_html)
            nav_side_dag_div.innerHTML = inner_html
       }
   });
}
