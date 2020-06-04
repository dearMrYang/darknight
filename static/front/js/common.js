
// 信息提示
let bs4message = {
    _option: {
        position: 'topcenter',
    },
    _default: function (message) {
        bs4pop.notice(message, this._option)
    },
    dark: function (message) {
        this._option['type'] = 'dark'
        this._default(message)
    },
    light: function (message) {
        this._option['type'] = 'light'
        this._default(message)
    },
    warning: function (message) {
        this._option['type'] = 'warning'
        this._default(message)
    },
    success: function (message) {
        this._option['type'] = 'success'
        this._default(message)
    },
    info: function (message) {
        this._option['type'] = 'info'
        this._default(message)
    },
    primary: function (message) {
        this._option['type'] = 'primary'
        this._default(message)
    },
    secondary: function (message) {
        this._option['type'] = 'secondary'
        this._default(message)
    },
    danger: function (message) {
        this._option['type'] = 'danger'
        this._default(message)
    },
}


$(function () {
    // 底部定位
    computer()
    function computer() {
        if ($(window).height() > $(document.body).height()) {
            $('.footer').addClass('fixed-bottom')
        } else {
            $('.footer').removeClass('fixed-bottom')
        }
    }
    $(window).resize(computer)

    // toolbar
    toolbar()
    function toolbar() {
        if ($(window).scrollTop() > 100) {
            $('.toolbar .back-to-top').css({ display: 'block' })
        } else {
            $('.toolbar .back-to-top').css({ display: 'none' })
        }
    }
    $(window).scroll(toolbar)

    //当点击跳转链接后，回到页面顶部位置
    $(".toolbar .back-to-top").click(function () {
        $('body,html').animate({ scrollTop: 0 }, 500);
        return false;
    });


})