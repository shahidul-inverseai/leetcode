$(document).ready(function () {
  $("#add-contest-btn").click(() => {
    $("#add-contest-btn").hide();
    $("#update-form").show();
  });

  $("#update-btn").click(() => {
    $("#update-form").hide();
    $("#add-contest-btn").show();
  });

  $("#cancel-btn").click(() => {
    $("#update-form").hide();
    $("#add-contest-btn").show();
  });
});
