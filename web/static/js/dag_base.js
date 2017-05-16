function getDags(user_id) {
   var postData = {
       "user_id": user_id 
   };
   $.ajax({
       type: "POST",
       url: "/dags/get_projects",
       contentType: "application/json; charset=utf-8",
       data: JSON.stringify(postData),
       dataType: "json",
       success: function(retJsonList){  
            var navSideDagDiv = document.getElementById("nav-side-dags");
            var innerHtml = '';
            for (var i = 0; i < retJsonList.length; i++) {
                var projectDict = retJsonList[i];
                var projectName = projectDict.project;
                var dagList = projectDict.dag_list;
                innerHtml += '<ul class="current"><li class="toctree-l1 current"><a class="current reference internal" href="#project='+projectName+'" onclick="showProject(' + projectName + ')"><span class="toctree-expand"></span>' + projectName + '</a><ul>';
                for (var j = 0; j < dagList.length; j++) {
                    var dagName = dagList[j];
                    innerHtml += '<li class="toctree-l2"><a class="reference internal" href="#dag='+dagName+'" onclick="showDag(' + dagName + ')">' + dagName + '</a></li>';
                }
                innerHtml += '</ul></ul>';
            } 
            navSideDagDiv.innerHTML = innerHtml;
       }
   });
}

function newProject() {
    BootstrapDialog.show({
        title: '新建项目',
        message: $(
            '<div><input id="new-project-name" type="text" class="form-control" placeholder="project name" required autofocus><br/><textarea id="new-project-desc" type="text" class="form-control" placeholder="project description" rows="3"></textarea></div>'
        ),
        buttons: [
            {
                label: 'Submit',
                cssClass: 'btn btn-success',
                hotkey: 13,
                action: function(dialogRef) {
                    var projectName = document.getElementById("new-project-name").value;
                    var projectDesc = document.getElementById("new-project-desc").value;
                    if (projectName.length <= 0) {
                        alert("项目名称不能为空");
                    }    
                    else {
                        addNewProject(dialogRef, projectName, projectDesc)
                    }
                }
            },
            {
                label: 'Cancel',
                cssClass: 'btn btn-warning',
                hotkey: 13,
                action: function(dialogRef) {
                    dialogRef.close();
                }
            }
        ]
    });
}

function addNewProject(dialogRef, projectName, projectDesc) {
    var postData = {
       "project_name": projectName,
       "project_desc": projectDesc
    };
    $.ajax({
       type: "POST",
       url: "/dags/new_project",
       contentType: "application/json; charset=utf-8",
       data: JSON.stringify(postData),
       dataType: "json",
       success: function(retJson){  
            console.log(retJson);
            var code = retJson.code; 
            var alertMessage = retJson.alert_message;
            alert(alertMessage);
            if (code == 0) {
                dialogRef.close();
            }
       }
   });
}

function showProject(projectName) {
}

function showDag(dagName) {
}
