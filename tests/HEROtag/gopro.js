function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
function getXhr(){
var xhr = null;
if(window.XMLHttpRequest) 
xhr = new XMLHttpRequest();
else if(window.ActiveXObject){ 
try {
xhr = new ActiveXObject("Msxml2.XMLHTTP");
} catch (e) {
xhr = new ActiveXObject("Microsoft.XMLHTTP");
}
}
else {
alert("Ooops, something went wrong");
xhr = false;
}
return xhr
}
function onLoad(){
command('setting','72','0');
sleep(500);
command('setting','54','1');
command('setting','55','2');
command('setting','56','0');
command('setting','8','1');
}
function command(option, type, command){
var xhr = getXhr()
xhr.onreadystatechange = function(){
if(xhr.readyState == 4 && xhr.status == 200){
alert(xhr.responseText);
}
}
xhr.open('GET','http://10.5.5.9/gp/gpControl/'+option+'/'+type+'/'+command);
xhr.send(null);
}
function commandTwo(option, type, number){
var xhr = getXhr()
xhr.onreadystatechange = function(){
if(xhr.readyState == 4 && xhr.status == 200){
alert(xhr.responseText);
}
}
xhr.open('GET','http://10.5.5.9/gp/gpControl/'+option+'/'+type+'?p='+number);
xhr.send(null);
}
function takepic() {
sleep (100)
commandTwo('command','shutter','0');
sleep(600)
commandTwo('command','mode','1');
sleep(1000);
commandTwo('command','shutter','1');
}
function offall(){
command('command','system','sleep');
sleep(1000);
command('setting','63','0');
}