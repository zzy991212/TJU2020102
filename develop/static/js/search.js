
function jmp_to_search(){
//  self.location='./component/search-result.html';
  var u = document.forms[0].elements["val"].value;
  document.forms[0].action = '/search_result' + '?value=' + u;
  document.forms[0].submit();
}

function jmp_toto_search(){
//  self.location='../component/search-result.html';
  var u = document.forms[0].elements["val"].value;
  document.forms[0].action = '/search_result' + '?value=' + u;
  document.forms[0].submit();
}

function entersearch(){
    if(event.keyCode==13){
        var u = document.forms[0].elements["val"].value;
        document.forms[0].action = '/search_result' + '?value=' + u;
        document.forms[0].submit();
    }
}

function jmp_to_page(pagenum){
    window.location.href="/word-cloud?pagenum=" + pagenum;
//    var u = document.getElementByid();
}

function jmp_to_pre_page(pagenum){
    window.location.href="/word-cloud?pagenum=" + (Number(pagenum) - 1).toString();
}
function jmp_to_next_page(pagenum){
    window.location.href="/word-cloud?pagenum=" + (Number(pagenum) + 1).toString();
}