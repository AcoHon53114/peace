(function ($) {
  "use strict";
  $(function () {
    setTimeout(function () { $("#message").fadeOut("slow"); }, 2000);
    if ($.fn.appear && $.fn.countTo) {
      $('.counter-thumb').appear(function () {
        $(this).find('.counter-number').countTo();
      });
    }
    $('.smoothscroll').on('click', function (event) {
      var href = this.getAttribute('href');
      if (!href || href.charAt(0) !== '#' || href.length < 2) return;
      var element = document.getElementById(href.slice(1));
      if (!element) return;
      event.preventDefault();
      var top = $(element).offset().top - ($('.navbar').outerHeight() || 0);
      $('body,html').animate({scrollTop: top}, 300);
    });
  });
})(window.jQuery);
