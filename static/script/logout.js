function deleteKey(){
    if($('#deleteKey:checked').length >= 1)
    {
        window.localStorage.removeItem("MediSecEncryptionKey");
    }
}

$(function () {
    /* Logout on-click cancel button */
    $("#logoutNavButton").click(function (e) { 
        e.preventDefault();
        $("#logoutCover").toggle();
    });

    $("#logoutCancel").click(function (e) { 
        e.preventDefault();
        $("#logoutCover").toggle();
    });
});