document.addEventListener('DOMContentLoaded', () => {

  $('.saveSetting').on('click', function(e){
   const xhr = new XMLHttpRequest();
   var settingType = $(this).attr('data');
   var csrf_token = document.getElementById('csrf_token').value;

   if (settingType == "security"){
     var url = '/setting/security';
     var password = document.getElementById('password');
     var new_password = document.getElementById('new_password');
     var confirm_password = document.getElementById('confirm_password');
     var data = {'password': password.value, "new_password": new_password.value, "confirm_password": confirm_password.value};
   }

   xhr.open('POST', url)
   xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
   xhr.setRequestHeader("X-CSRFToken", csrf_token);
   xhr.onload = () =>{
     if(xhr.status == 200){
       const result = JSON.parse(xhr.responseText);
       if(result.success){
         Swal.fire({
           icon: 'success',
           title: "Good job!",
           text: result.msg,
           type: "success",
           confirmButtonClass: 'btn btn-primary',
           buttonsStyling: false,
         });
       }
       else{
         Swal.fire({
           icon: 'error',
           title: "Oops..",
           text: result.msg,
           type: "error",
           confirmButtonClass: 'btn btn-primary',
           buttonsStyling: false,
         });
       }
     }
   }
   xhr.send(JSON.stringify(data));
   return false;
  })

})
