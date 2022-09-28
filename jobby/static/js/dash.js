(function($){
  "use strict";

  $(document).ready(function(){
    $('.viewButton').on('click', function(e){
      Chart.defaults.global.defaultFontFamily = "Nunito";
      Chart.defaults.global.defaultFontColor = '#888';
      Chart.defaults.global.defaultFontSize = '14';

      var ctx = document.getElementById('chart').getContext('2d');

      const xhr = new XMLHttpRequest();
      var task_id = parseInt($(this).attr('data'));
      var url = '/get-view-data/' + task_id;

      xhr.open('GET', url);

      xhr.onload = () =>{
        if (xhr.status == 200){
          const viewData = JSON.parse(xhr.responseText);
          if (viewData.success) {
            $('#chartTable').show('slow');
            $('#project_name').html('<i class="icon-feather-bar-chart-2"></i>' + viewData.project_name)
            var chart = new Chart(ctx, {
          		type: 'line',

          		// The data for our dataset
          		data: {
          			labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
          			// Information about the dataset
          	   		datasets: [{
          				label: "Views",
          				backgroundColor: 'rgba(42,65,232,0.08)',
          				borderColor: '#2a41e8',
          				borderWidth: "3",
          				data: [viewData.monday,viewData.tuesday,viewData.wednesday,viewData.thursday,viewData.friday,viewData.saturday,viewData.sunday],
          				pointRadius: 5,
          				pointHoverRadius:5,
          				pointHitRadius: 10,
          				pointBackgroundColor: "#fff",
          				pointHoverBackgroundColor: "#fff",
          				pointBorderWidth: "2",
          			}]
          		},

          		// Configuration options
          		options: {

          		    layout: {
          		      padding: 10,
          		  	},

          			legend: { display: false },
          			title:  { display: false },

          			scales: {
          				yAxes: [{
          					scaleLabel: {
          						display: false
          					},
          					gridLines: {
          						 borderDash: [6, 10],
          						 color: "#d8d8d8",
          						 lineWidth: 1,
          	            	},
          				}],
          				xAxes: [{
          					scaleLabel: { display: false },
          					gridLines:  { display: false },
          				}],
          			},

          		    tooltips: {
          		      backgroundColor: '#333',
          		      titleFontSize: 13,
          		      titleFontColor: '#fff',
          		      bodyFontColor: '#fff',
          		      bodyFontSize: 13,
          		      displayColors: false,
          		      xPadding: 10,
          		      yPadding: 10,
          		      intersect: false
          		    }
          		},

            });
          }
          else {
            alert(viewData.msg);
          }

        }
      }
      xhr.send();
    })

    $('.deleteNotif').on('click', function(e){
      const xhr = new XMLHttpRequest();
      var notif_id = $(this).attr('data');
      var url = '/delete-notif/' + notif_id;

      xhr.open('GET', url);
      xhr.onload = () => {
        if (xhr.status == 200){
          const result = JSON.parse(xhr.responseText);
          if (result.success) {
            if (result.all) {
              $('#notifList').hide('slow', function(){ $('#notifList').remove(); });
            }
            else {
              $('#'+notif_id).hide('slow', function(){ $('#'+notif_id).remove(); });
            }
          }
        }
      }
      xhr.send();
    })
  })

})(this.jQuery);
