/*** ON PAGE READY ***/
$(function () {
    function footer_on_bottom() {
        var contentHeight = $(window).height();
        var footerHeight = $('footer').height();
        var footerTop = $('footer').position().top + footerHeight;
        if (footerTop < contentHeight) {
            $('footer').css('margin-top', (contentHeight - footerTop - 8) + 'px');
        }
    } footer_on_bottom();

    // LOGOUT LOGIC
    $("#logOutButton").click(function (e) { 
        e.preventDefault();
        window.localStorage.clear();
        window.location.replace("/logout");
    });
})

function checkPasswordPolicy(password) {
    var expression = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%&*()]).{8,}/;

    return expression.test(password);
}