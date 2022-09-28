document.addEventListener('DOMContentLoaded', () => {
  badge = document.getElementsByName('badge');
  badge.forEach(function(b){
    if (parseInt(b.innerText) == 0){
      b.style.visibility = 'hidden';
    }
    else{
      b.style.visibility = 'visible';
    }
  })
})
