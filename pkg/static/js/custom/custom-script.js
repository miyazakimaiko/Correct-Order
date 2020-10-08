/*================================================================================
	Item Name: Materialize - Material Design Admin Template
	Version: 5.0
	Author: PIXINVENT
	Author URL: https://themeforest.net/user/pixinvent/portfolio
================================================================================

NOTE:
------
PLACE HERE YOUR OWN JS CODES AND IF NEEDED.
WE WILL RELEASE FUTURE UPDATES SO IN ORDER TO NOT OVERWRITE YOUR CUSTOM SCRIPT IT'S BETTER LIKE THIS. */

$(document).ready(function(){
    $('.reminder-input').keyup(function(){
        var name = $(this).attr('id');
        var currentNum = $(this).val();
        $('#output-'+name).text(currentNum);
    });
});


function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#user-avatar').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$("#picture").change(function() {
  readURL(this);
});

$("#oneday_shelf_life").click(function() {
  if ($(this).is(":checked")) {
    $("#extra").prop("disabled", true);
    $("#waste").prop("disabled", false);
    $("#extra").attr("value", 0);
  } else if ($(this).not(":checked")){
    $("#extra").prop("disabled", false);
    $("#waste").prop("disabled", true);
    $("#waste").attr("value", 0);
  }
});

var products = JSON.parse(document.getElementById('geocode').dataset.geocode);

$.each(products, function(i, ob) {
    $.each(ob, function (ind, obj) {
        $("#oneday_shelf_life-" + obj).click(function() {
            $("#extra-" + obj).prop("disabled", (i, v) => !v);
            $("#waste-" + obj).prop("disabled", (i, v) => !v);
        });
        if ($("#oneday_shelf_life-" + obj).is(":checked")) {
            $("#extra-" + obj).prop("disabled", true);
            $("#waste-" + obj).prop("disabled", false);
            $("#extra-" + obj).attr("value", 0);
        } else if ($(this).not(":checked")){
            $("#extra-" + obj).prop("disabled", false);
            $("#waste-" + obj).prop("disabled", true);
            $("#waste-" + obj).attr("value", 0);
        }
    });
});
