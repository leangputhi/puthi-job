document.addEventListener('DOMContentLoaded', () =>{
  $('#bookmark').on('click', function(e){
    const request = new XMLHttpRequest();
    var bookmark_id = parseInt($(this).attr('data'));
    var bookmarkType = parseInt($(this).data('type'));
    if($(this).hasClass('bookmarked')){
      var url = '/unmark/' + bookmark_id;
    }
    else{
      var url = '/bookmark/' + bookmark_id;
    }

    request.open('POST', url);
    request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    request.onload = () =>{
      if (request.status == 200){
        const result = JSON.parse(request.responseText);
        if(result.success){
          if(result.bookmark){
            $(this).addClass('bookmarked');
            $(this).html('<i class="uil uil-check"></i> Bookmarked');
            e.preventDefault();
          }
          else {
            $(this).removeClass('bookmarked');
            $(this).html('<i class="uil uil-bookmark"></i> Bookmark');
            e.preventDefault();
          }
        }
        else{
          alert(result.msg);
        }
      }
    }
    request.send(JSON.stringify({"bookmarkType": bookmarkType}));
    return false;
  });

  if (document.getElementById('submitBidButton')) {
    var submitBidButton = document.getElementById('submitBidButton');
    submitBidButton.addEventListener('click', () =>{
      var bid_amount = document.getElementById('bid_amount').value;
      var qtyInput = document.getElementById('qtyInput').value;
      var qtyOption = document.getElementById('qtyOption').value;
      var bidMessage = document.getElementById('bidMessage').value;

      var form_data = new FormData();
      const xhr = new XMLHttpRequest();
      var url = window.location.pathname;
      var csrf_token = document.getElementById('csrf_token').value;

      form_data.append("bid_amount", bid_amount);
      form_data.append("qtyInput", qtyInput);
      form_data.append("qtyOption", qtyOption);
      form_data.append("bidMessage", bidMessage);

      xhr.open('POST', url)
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
      xhr.onload = () =>{
        if(xhr.status == 200){
          const result = JSON.parse(xhr.responseText);
          if(result.success){
            window.location.href = result.msg;
          }
        }
      }
      xhr.send(form_data);
      return false;
    })
  }

  if (document.getElementById('offerForm')) {
    var offerForm = document.getElementById('offerForm');
    offerForm.addEventListener('submit', (e) =>{
      var subject = document.getElementById('subject').value;
      var offerMessage = document.getElementById('offerMessage').value;
      var offeredTask = document.getElementById('offeredTask').value;
      var ins = document.getElementById('formFile').files.length;
      var ext = ['pdf', 'doc', 'docx'];

      if(subject.length < 5 || subject.length > 100){
        alert("subject length should be between 5 and 100.");
        e.preventDefault();
      }

      if(offerMessage.length < 15 || offerMessage.length > 500){
        alert("message length should be between 15 and 500.");
        e.preventDefault();
      }

      if(!offeredTask){
        alert("You have to choose a project!");
        e.preventDefault();
      }

      if(ins > 0) {
        var size = document.getElementById('formFile').files[0].size;
      }

      if(size > 2*1024*1024) {
        alert("file size is too big!At most 2Mb.")
        e.preventDefault();
      }

      if (document.getElementById('formFile').value) {
        if ( !ext.includes(document.getElementById('formFile').value.split('.').pop()) ) {
          alert('Invalid file type! Only pdf, doc, docx are allowed');
          e.preventDefault();
        }
      }
    })
  }

})
