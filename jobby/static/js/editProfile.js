(function($){
  "use strict";

   $(document).ready(function(){
     var toolbarOptions = [
   		['bold', 'italic', 'underline'],
   		[{'list': 'ordered'}, {'list': 'bullet'}]
   	];

     var quill = new Quill('#editor', {
       theme: 'snow',
   		modules: {
   			toolbar: toolbarOptions
   		}
     });

   	var quill2 = new Quill('#editor2', {
       theme: 'snow',
   		modules: {
   			toolbar: toolbarOptions
   		}
     });

   	var quill3 = new Quill('#editor3', {
       theme: 'snow',
   		modules: {
   			toolbar: toolbarOptions
   		}
     });

     $('.collapse').on('click', function(e){
       if($(this).next().css("display") == 'none'){
         $(this).next().show('slow');
       }
       else {
         $(this).next().hide('slow');
       }
     })

     //if a record exist then only show that otherwise show form
     var list_group = document.getElementsByClassName('list-group');
     for (ls of list_group){
       var li = ls.firstElementChild;
       if(li.style.display != 'none'){
         ls.parentNode.nextElementSibling.style.display = 'none';
       }
     }

     $('.saveSetting').on('click', function(e){
     	const xhr = new XMLHttpRequest();
     	var editProfileType = $(this).attr('data');
     	var csrf_token = document.getElementById('csrf_token').value;

     	if(editProfileType == "profile"){
     		var url = '/editProfile/profile';
        var editor = document.querySelector('#editor3');
     		var field_of_work = document.getElementById('field_of_work');
     		var tagline = document.getElementById('tagline');
     		var location = document.getElementById('location');
     		var introduction = document.querySelector('#profileQuill');
        introduction.value = editor.children[0].innerHTML;
     		var data = {'field_of_work': field_of_work.value, "tagline": tagline.value,
     		'location': location.value, "introduction": introduction.value};
     	}

     	else if(editProfileType == "skill"){
     		var url = '/editProfile/skill';
     		var skill = document.getElementById('skill').value;
     		var level = document.getElementById('level').value;
        if (parseInt(level) > 100 || parseInt(level) < 0 || !level) {
          alert("level should be a number between 0 and 100");
          return false;
        }

        if (!skill || skill.length > 50) {
          alert("skill length should be between 0 and 100");
          return false;
        }
     		var data = {'skill': skill, "level": level};
     	}

     	else if(editProfileType == "workExp"){
        var url = '/editProfile/workExp';
        var editor = document.querySelector('#editor2');
        var position = document.getElementById('position').value;
        var company = document.getElementById('company').value;
        var start_month_job = document.getElementById('start_month_job').value;
        var start_year_job = document.getElementById('start_year_job').value;
        var end_month_job = document.getElementById('end_month_job').value;
        var end_year_job = document.getElementById('end_year_job').value;
        var desc_work = document.querySelector('#desc_work');
        desc_work.value = editor.children[0].innerHTML;
        var data = {'position': position, "company": company, "start_month_job": start_month_job,
        "start_year_job": start_year_job, "end_month_job": end_month_job, "end_year_job": end_year_job,
        "desc_work": desc_work.value};
     	}

     	else if(editProfileType == "education"){
        var url = '/editProfile/education';
        var editor = document.querySelector('#editor');
        var field = document.getElementById('field').value;
        var school = document.getElementById('school').value;
        var start_month_edu = document.getElementById('start_month_edu').value;
        var start_year_edu = document.getElementById('start_year_edu').value;
        var end_month_edu = document.getElementById('end_month_edu').value;
        var end_year_edu = document.getElementById('end_year_edu').value;
        var desc_edu = document.querySelector('#desc_edu');
        desc_edu.value = editor.children[0].innerHTML;
        var data = {'field': field, "school": school, "start_month_edu": start_month_edu,
        "start_year_edu": start_year_edu, "end_month_edu": end_month_edu, "end_year_edu": end_year_edu,
        "desc_edu": desc_edu.value};
     	}

      else if (editProfileType == "social"){
     		var url = '/editProfile/social';
     		var facebook = document.getElementById('facebook').value;
     		var twitter = document.getElementById('twitter').value;
     		var youtube = document.getElementById('youtube').value;
        var github = document.getElementById('github').value;
     		var instagram = document.getElementById('instagram').value;
     		var linkedin = document.getElementById('linkedin').value;
     		var data = {'facebook': facebook, "twitter": twitter, "youtube": youtube,
          "github": github, "instagram": instagram, "linkedin": linkedin};
     	}

     	xhr.open('POST', url)
     	xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
     	xhr.setRequestHeader("X-CSRFToken", csrf_token);
     	xhr.onload = () =>{
     		if(xhr.status == 200){
     			const result = JSON.parse(xhr.responseText);
     			if(result.success){
            if(result.editProfileType == 's'){
              saveSkill(result.skill,result.level, result.skill_id);
            }
            else if(result.editProfileType == 'w'){
              saveWorkExp(result.workExp, result.company, result.workExp_id);
            }
            else if(result.editProfileType == 'so'){
              Swal.fire({
                icon: 'success',
                title: "Good job!",
                text: "Saved successfully!",
                type: "success",
                confirmButtonClass: 'btn btn-primary',
                buttonsStyling: false,
              });
            }
            else if(result.editProfileType == 'e'){
              saveEdu(result.field, result.school, result.edu_id);
            }
            else if(result.editProfileType == 'p'){
              Swal.fire({
                icon: 'success',
                title: "Good job!",
                text: "Saved successfully!",
                type: "success",
                confirmButtonClass: 'btn btn-primary',
                buttonsStyling: false,
              });
            }
     			}
     			else{
     				alert(result.msg);
     			}
     		}
     	}
     	xhr.send(JSON.stringify(data));
     	return false;
     })

     function saveSkill(skill, level, skill_id){
        var skill_table = document.getElementById('skill_table');
        var form_skill = document.getElementById('skillForm');
        if (skill_table.style.display == 'none'){
          skill_table.style.display = "";
        }

        var tbody = document.getElementById('tbody_skill');
        tbody.innerHTML += '<tr class="table-active" id=s_' + skill_id + '>' +
          '<td>' +
            '<span class="font-weight-bold">' + skill + '</span>' +
          '</td>' +
          '<td>' + level + '</td>' +
          '<td>' +
          '<button type="button" class="btn btn-danger deleteItem" data="s_' + skill_id + '"><i class="icon-feather-trash-2"></i></button>' +
          '</td>' +
        '</tr>';

        form_skill.style.display = 'none';
        return false;
      }

     function saveWorkExp(position, company, workExp_id){
       var workExp_table = document.getElementById('workExp_table');
       var form_workexp = document.getElementById('workExpForm');
       if (workExp_table.style.display == 'none'){
         workExp_table.style.display = "";
       }

       var tbody = document.getElementById('tbody_workExp');
       tbody.innerHTML += '<tr class="table-active" id=w_' + workExp_id + '>' +
         '<td>' +
           '<span class="font-weight-bold">' + position + '</span>' +
         '</td>' +
         '<td>' + company + '</td>' +
         '<td>' +
         '<button type="button" class="btn btn-danger deleteItem" data="w_' + workExp_id + '"><i class="icon-feather-trash-2"></i></button>' +
         '</td>' +
       '</tr>';

       form_workexp.style.display = 'none';
       return false;
     }

     function saveEdu(field, school, edu_id){
       var edu_table = document.getElementById('edu_table');
       var form_edu = document.getElementById('eduForm');
       if (edu_table.style.display == 'none'){
         edu_table.style.display = "";
       }

       var tbody = document.getElementById('tbody_edu');
       tbody.innerHTML += '<tr class="table-active" id=e_' + edu_id + '>' +
         '<td>' +
           '<span class="font-weight-bold">' + field + '</span>' +
         '</td>' +
         '<td>' + school + '</td>' +
         '<td>' +
         '<button type="button" class="btn btn-danger deleteItem" data="e_' + edu_id + '"><i class="icon-feather-trash-2"></i></button>' +
         '</td>' +
       '</tr>';

       form_edu.style.display = 'none';
       return false;
     }

    document.addEventListener('click', deleteItem);

    function deleteItem(e){
   		if (e.target.matches('.deleteItem')){
        const request = new XMLHttpRequest();
        var csrf_token = document.getElementById('csrf_token').value;
     		var type_id = $(e.target).attr('data');
        var data = {"type_id": type_id};
     		var url = '/deleteItem';

        request.open('POST', url);
        request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
       	request.setRequestHeader("X-CSRFToken", csrf_token);
    		request.onload = () =>{
    			if (request.status == 200){
    				const result = JSON.parse(request.responseText);
    				if(result.success){
              if (result.currentField == 's') {
                var tbody = document.getElementById('tbody_skill');
                var item = document.getElementById(type_id);
                item.parentNode.removeChild(item);
                if (tbody.childElementCount == 0){
                  var skill_table = document.getElementById('skill_table');
                  skill_table.style.display = "none";
                }
                e.preventDefault();
              }
              else if (result.currentField == 'w') {
                var tbody = document.getElementById('tbody_workExp');
                var item = document.getElementById(type_id);
                item.parentNode.removeChild(item);
                if (tbody.childElementCount == 0){
                  var workExp_table = document.getElementById('workExp_table');
                  workExp_table.style.display = "none";
                }
                e.preventDefault();
              }
              else if (result.currentField == 'e') {
                var tbody = document.getElementById('tbody_edu');
                var item = document.getElementById(type_id);
                item.parentNode.removeChild(item);
                if (tbody.childElementCount == 0){
                  var edu_table = document.getElementById('edu_table');
                  edu_table.style.display = "none";
                }
                e.preventDefault();
              }
    				}
    				else{
    					alert("Lutfen giriş yapınız");
    				}
    			}
    		}
    		request.send(JSON.stringify(data));
    		return false;
      }
    }

    var addButton = document.getElementsByName('addButton');
    addButton.forEach(function(btn){
      btn.onclick = () =>{
        var row = btn.previousElementSibling;
        if(row.style.display == 'none'){
          row.style.display = '';
        }
        else{
          alert("Please save the open form first!");
        }
      }
    })

   })
 })(this.jQuery);
