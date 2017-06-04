/* Make alerts dismissible */

hljs.initHighlightingOnLoad();

$(function() {
  $(".close").each(function() {
    $(this).click(function() {
      $(this).parent().remove();
    });
  });

  $(".clickable").each(function() {
    $(this).click(function() {
      window.location = $(this).data("href");
    });
  });
});