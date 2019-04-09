function deleteElementAfterTimeout(element, seconds) {
    setTimeout(function () {
        element.hide(500, function () {
            element.remove();
        });
    }, seconds*1000);
}


function createUserMessage(message, seconds=3, type="error") {
    if (type === "info") {
        var msg = $('<p class="alert alert-info">');
    }
    else {
        var msg = $('<p class="alert alert-danger">');
    }
    msg[0].innerText = message;
    msg.css('display', 'none');
    $("#" + type + "MessageContainer").append(msg);
    msg.show(500);
    deleteElementAfterTimeout(msg, seconds)
}