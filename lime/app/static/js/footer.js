/* Make alerts dismissible */

$(function() {
  $(".close").each(function() {
    $(this).click(function() {
      $(this).parent().remove();
    });
  })
});