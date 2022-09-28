var form = document.getElementById('leave-review-form');
var rate = document.getElementsByName('rate');
rate.forEach(function(r){
  r.onclick = () => {
    const request = new XMLHttpRequest();
    var review_id = parseInt(r.getAttribute('data'));
    form.setAttribute('data', review_id);
    var url = '/get-review/' + review_id;
    request.open('GET', url);

    request.onload = () =>{
      if (request.status == 200){
        const reviewData = JSON.parse(request.responseText);
        document.getElementById('rateWho').innerHTML = "<span>Rate <a href='#'>"  + reviewData.winner + " </a> for the project <a href='#'>" + reviewData.reviewed + "</a></span>";
      }
    }
    request.send();
  }
})


form.addEventListener('submit', () =>{
  var recommendation = document.getElementById('radio-1').checked;
  var RadioValues = document.getElementById('RadioValues');
  var intime = document.getElementById('radio-3').checked;
  var rating;
  var review_id = parseInt(form.getAttribute('data'));
  if(document.getElementById('rating-radio-5').checked){
    rating = 1;
  }
  else if(document.getElementById('rating-radio-4').checked){
    rating = 2;
  }
  else if(document.getElementById('rating-radio-3').checked){
    rating = 3;
  }
  else if(document.getElementById('rating-radio-2').checked){
    rating = 4;
  }
  else {
    rating = 5;
  }
  RadioValues.value = review_id + " " + recommendation + " " + intime + " " + rating;
})
//
// var reply = document.getElementsByName('reply');
// reply.forEach(function(r){
//   r.onclick = () =>{
//     const request = new XMLHttpRequest();
//     var review_id = parseInt(r.getAttribute('data'));
//     var url = '/reply-review/' + review_id;
//     var reply = r.previousElementSibling;
//     request.open('POST', url);
//
//     request.onload = () =>{
//       if (request.status == 200){
//         const result = JSON.parse(request.responseText);
//         if(result.success){
//           res = document.getElementById(review_id);
//           res.innerText = reply.value;
//           res.previousElementSibling.innerText = result.pro;
//           reply.remove();
//           r.remove();
//
//         }
//       }
//     }
//     request.send(JSON.stringify({"reply": reply.value}));
//     return false;
//   }
// })
