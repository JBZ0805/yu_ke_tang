$(function () {
    var tabsSwiper = new Swiper('.swiper-tabs1', {
        onSlideChangeStart: function() {
            $('.barmenu .on').removeClass('on');
            $('.barmenu a').eq(tabsSwiper.activeIndex).addClass('on');
        }
    });

    $('.barmenu a').on('touchstart mousedown', function() {
        var _ = $(this);
        _.addClass('on').siblings().removeClass('on');
        tabsSwiper.slideTo(_.index());
        return false;
    });
});
