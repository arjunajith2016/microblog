var sidebar = document.querySelector('.sidebar');
var height = document.getElementById('navbar').offsetHeight;
var origOffsetY = sidebar.offsetTop-height;
var test = document.getElementById('sidebar');
var y=window.pageY;

function onScroll(e) {
  window.scrollY >= origOffsetY ? sidebar.classList.add('sticky') : sidebar.classList.remove('sticky');

  if(window.scrollY < origOffsetY)
  {
  	//test.style.position = 'fixed';
  	//test.style.posTop = MouseEvent.movementY  ;
  }

}

document.addEventListener('scroll', onScroll);
document.addEventListener('mousemove', onScroll);