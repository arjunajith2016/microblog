var sidebar = document.querySelector('.sidebar');
var height = document.getElementById('navbar').offsetHeight;
var origOffsetY = sidebar.offsetTop-height;
var test = document.getElementById('sidebar');
var y=window.pageY;

function onScroll(e) {
  window.scrollY >= origOffsetY ? sidebar.classList.add('sticky') : sidebar.classList.remove('sticky');

  /*if(window.scrollY < origOffsetY)
  {
  	test.style.position = 'fixed';
  	test.style.top = 'scrollY/2'  ;
  }*/

}

function like(id) {

  var xhttp = new XMLHttpRequest();
  var recv
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      recv = xhttp.responseText;
      document.getElementById("btn"+id).value = recv.slice(1)+' Likes';
      /*if(xhttp.responseText.charAt(0)=='y')
      {
      	document.getElementById("btn"+id).style.backgroundColor='rgba(0,170,100,0.8)';
      }
      else
      {
      	document.getElementById("btn"+id).style.backgroundColor='rgba(0,100,200,0)';
      }*/
    }
  };
  xhttp.open('PUT','like/'+id,true);
  xhttp.send();
}

document.addEventListener('scroll', onScroll);
document.addEventListener('mousemove', onScroll);