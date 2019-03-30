// function deleteKey(){
//     // if($('#deleteKey:checked').length >= 1)
//     // {
//         window.localStorage.removeItem("MediSecEncKey");
//     // }
// }

$(function () {

    // $("#logoutBox form").submit(function (e) { 
    //     window.localStorage.clear();
    //     return true;
    // });

    $("#logOutButton").click(function (e) { 
        e.preventDefault();
        window.localStorage.clear();
        window.location.replace("/logout");
    });

    // Old animation code for the logout pop-up.
    // var LOGOUTANIMATIONTIME = 300;
    // /* Logout on-click cancel button */
    // $("#logoutNavButton").click(function (e) { 
    //     $("#logoutCover").toggle(0, function () {
    //         $("#logoutBox").toggle(LOGOUTANIMATIONTIME);
    //     });
    //     e.preventDefault();
    // });

    // $("#logoutCancel").click(function (e) { 
    //     $("#logoutBox").toggle(LOGOUTANIMATIONTIME, function () {
    //         $("#logoutCover").toggle(0);
    //     });
    //     e.preventDefault();
    // });
});