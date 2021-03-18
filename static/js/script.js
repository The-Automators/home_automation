$(document).ready(() => {
    $('[data-toggle="tooltip"]').tooltip();   
});
$(".input-field input").on("focus",function(){
    $(this).addClass("focus");
});
$(".input-field input").on("blur",function(){
    if($(this).val() == "")
    $(this).removeClass("focus");
});