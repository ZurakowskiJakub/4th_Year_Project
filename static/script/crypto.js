function encrypt(plaintext, passphrase) {
    var encrypted = CryptoJS.AES.encrypt(plaintext, passphrase);

    return encrypted.toString();
}

function decrypt(encrypted_text, passphrase) {
    var decrypted = CryptoJS.AES.decrypt(encrypted_text, passphrase);

    return decrypted.toString(CryptoJS.enc.Utf8);
}


function generate_hash(plaintext, user_salt=null) {
    var plaintext = plaintext;
    var salt;
    if (user_salt === null) {
        //Generate salt based on current timestamp
        var now = new Date().getTime().toString();
        salt = CryptoJS.SHA256(now).toString();
    }
    else {
        //Use provided salt
        salt = user_salt;
    }

    var hash = CryptoJS.SHA256(salt+plaintext).toString();

    return {
        "salt": salt,
        "hash": hash
    };
}


function create_hash(plaintext) {
    var digest = null;
    
    try {
        digest = CryptoJS.SHA256(plaintext).toString();
    } catch (error) {
        console.log(error);
    }

    return digest;
}