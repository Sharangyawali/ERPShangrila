$(document).ready(function () {
  toggleDateFields();
  console.log("Hello from jquery of leave duration");

  $('input[name="duration_type"]').change(function () {
    toggleDateFields();
  });
});

function toggleDateFields() {
  var fullDay = $("#full-day");
  var halfDay = $("#half-day");

  var moreDayField = $(".date-container-full-day");
  var halfDayContainer = $(".half-day-container");

  if (fullDay.is(":checked")) {
    moreDayField.show();
    halfDayContainer.hide();
  } else {
    moreDayField.hide();
    halfDayContainer.show();
  }
}
