$(document).ready(function () {
  const contestUrl =
    "https://leetcode.com/contest/api/info/weekly-contest-267/";
  const proxy = "https://cors-anywhere.herokuapp.com/";

  $.ajax({
    url: contestUrl,
    complete: function (data) {
      console.log(data);
    },
  });
});
