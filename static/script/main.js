/*
function encrypt(object) {
    var encrypted = CryptoJS.AES.encrypt(object.value, "Secret Passphrase");
    var decrypted = CryptoJS.AES.decrypt(encrypted, "Secret Passphrase");
    console.log(encrypted.toString());
    console.log(decrypted.toString(CryptoJS.enc.Utf8));

    // $('#' + object.id + '_res')[0].value = decrypted.toString(CryptoJS.enc.Utf8);
    $('#' + object.id + '_res')[0].value = encrypted.toString();

    // Decode the base64 data so we can separate iv and crypt text.
    var rawData = atob(encrypted);
    var iv = rawData.substring(0,16);
    var crypttext = rawData.substring(16);

    // Decrypt...
    var plaintextArray = CryptoJS.AES.decrypt(
        { ciphertext: CryptoJS.enc.Latin1.parse(crypttext) },
        CryptoJS.enc.Hex.parse(key),
        { iv: CryptoJS.enc.Latin1.parse(iv) }
    );

    console.log(CryptoJS.enc.Latin1.stringify(plaintextArray));

}
*/

// On page.ready()
$(function () {
    // Generates encrypted fields on page load.
    generate_encrypted_fields();
})

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

// function derive_key_from_text(plaintext) {
//     // var salt = CryptoJS.lib.WordArray.random(128 / 8);
//     var salt = plaintext;
//     var key256Bits = CryptoJS.PBKDF2(plaintext, salt, { keySize: 256 / 32 });
//     return key256Bits.toString();
// }