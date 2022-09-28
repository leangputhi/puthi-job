(function($){
  "use strict";

  $(document).ready(function(){
    var accept = document.getElementsByName('acceptBid');
    var BidData;
    accept.forEach(function(a){
      a.onclick = () => {
        const request = new XMLHttpRequest();
        var bid_id = parseInt(a.getAttribute('data'));
        var url = '/accept-bid/' + bid_id;
        request.open('GET', url);

        request.onload = () =>{
          if (request.status == 200){
            BidData = JSON.parse(request.responseText);
            document.getElementById('bid_amount').innerText = BidData.bid_amount + ' $';
            document.getElementById('bidder').innerText = "Accept bid from " + BidData.bidder;
          }
        }
        request.send();
      }
    })

    $('#acceptButton').on('click', function(e){
      const xhr = new XMLHttpRequest();
      var bid_id = BidData.bid_id;
      var url = '/accept-bid/' + BidData.bid_id;
      xhr.open('POST', url);
      xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");

      xhr.onload = () =>{
        if (xhr.status == 200){
          var result = JSON.parse(xhr.responseText);
          if(result.success){
            acceptButton.remove();
            document.getElementById('bid_amount').remove();
            msg = document.getElementById('bidder');
            msg.innerText = "Bid Accepted!";
            msg.style.color = 'green';
            deleteButtons(bid_id);
          }
        }
      }
      xhr.send(JSON.stringify({"bidder_id": BidData.bidder_id}));
      return false;
    })

    function deleteButtons(bid_id){
      accept.forEach(function(a){
        if(parseInt(a.getAttribute('data')) == bid_id){
          a.innerText = 'Won';
          a.style.background = 'green';
          a.parentNode.lastElementChild.remove();
        }
        else{
          a.style.display = 'none';
        }
      })
    }
  })
})(this.jQuery);
