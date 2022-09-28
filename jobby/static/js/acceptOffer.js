(function($){
  "use strict";

  $(document).ready(function(){
    var accept = document.getElementsByName('acceptOffer');
    var offerData;
    accept.forEach(function(a){
      a.onclick = () => {
        const request = new XMLHttpRequest();
        var offer_id = parseInt(a.getAttribute('data'));
        console.log(offer_id);
        var url = '/accept-offer/' + offer_id;
        request.open('GET', url);

        request.onload = () =>{
          if (request.status == 200){
            offerData = JSON.parse(request.responseText);
            document.getElementById('offer').innerText = "Accept offer from " + offerData.offers;
          }
        }
        request.send();
      }
    })

    var acceptButton = document.getElementById('acceptButton');
    var rejectButton = document.getElementById('rejectButton');

    acceptButton.onclick = () =>{
      const xhr = new XMLHttpRequest();
      var offer_id = offerData.offer_id;
      var url = '/accept-offer/' + offerData.offer_id;
      xhr.open('POST', url);
      xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");

      xhr.onload = () =>{
        if (xhr.status == 200){
          var result = JSON.parse(xhr.responseText);
          if(result.success){
            acceptButton.remove();
            rejectButton.remove();
            msg = document.getElementById('offer');
            msg.innerText = "Offer Accepted!";
            msg.style.color = 'green';

          }
        }
      }
      xhr.send(JSON.stringify({"offer_id": offerData.offer_id}));
      return false;
    }

  })

})(this.jQuery);
