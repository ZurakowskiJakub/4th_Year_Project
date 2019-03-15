function checkKey() {
    // Check if local storage is supported
    if(typeof(Storage) == "undefined"){
        window.location.replace("{{url_for(index)}}");
    }
    else {
        return true;
    }
}