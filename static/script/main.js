/*** RAN AT START-UP ***/
// checkKey();


/*** ON PAGE READY ***/
$(function () {
    // Generates encrypted fields on page load.
    generate_encrypted_fields();
})


/*** PRIVATE FUNCTIONS ***/
function fill_encrypted(object, encryption_key) {
// function fill_encrypted(object, encrypt_with_itself = false) {

    // var password;
    // if (encrypt_with_itself) {
    //     password = object.value;
    // }
    // else {
    //     // TODO password that is retrieved.
    //     // getCookie('encryption_key);
    //     //// setCookie('encryption_key', this.value);
    // }
    $('#' + object.id + '_encrypted')[0].value = encrypt(object.value, encryption_key);
}

function fill_password(object, salt = null) {
    if (salt === null) {
        var hash = generate_hash(object.value);
        $('#' + object.id + '_salt')[0].value = hash["salt"];
        $('#' + object.id + '_hash')[0].value = hash["hash"];
    }
    else {
        var hash = generate_hash(object.value, salt);
        $('#' + object.id + '_salt')[0].value = hash["salt"];
        $('#' + object.id + '_hash')[0].value = hash["hash"];
    }
}

function encrypt(plaintext, passphrase) {
    // TODO remove the randomness factor.
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


function PBKDF2(salt, password) {
    var user_salt = salt;
    var user_password = password;
    var iterations = 2500;
    var digest = CryptoJS.PBKDF2(
        user_password,
        user_salt,
        {
            keySize: 512 / 32,
            iterations: iterations
        }
    );
    return digest.toString();
}


function checkPasswordPolicy(password) {
    var expression = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%&*()]).{8,}/;

    return expression.test(password);
}


function deleteElementAfterTimeout(element, seconds) {
    setTimeout(function () {
        element.hide(750, function () {
            element.remove();
        });
    }, seconds*1000);
}


function createUserMessage(message, seconds=3, type="error") {
    var msg = $('<p>');
    msg[0].innerText = message;
    $("#"+type+"MessageContainer").append(msg);
    deleteElementAfterTimeout(msg, seconds)
}