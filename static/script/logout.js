function deleteKey(){
    if($('#deleteKey:checked').length >= 1)
    {
        window.localStorage.removeItem("MediSecEncryptionKey");
    }
}

$(function () {

    var LOGOUTANIMATIONTIME = 400;
    /* Logout on-click cancel button */
    $("#logoutNavButton").click(function (e) { 
        e.preventDefault();
        $("#logoutCover").toggle(0, function () {
            $("#logoutBox").toggle(LOGOUTANIMATIONTIME);
        });
    });

    $("#logoutCancel").click(function (e) { 
        e.preventDefault();
        $("#logoutBox").toggle(LOGOUTANIMATIONTIME, function () {
            $("#logoutCover").toggle(0);
        });
    });
});