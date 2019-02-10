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

function fill_encrypted(object) {
    $('#' + object.id + '_encrypted')[0].value = encrypt(object.value);
}

function encrypt(plaintext, passphrase="Secret Passphrase") {
    // TODO remove the randomness factor.
    var encrypted = CryptoJS.AES.encrypt(plaintext, passphrase);

    return encrypted.toString();
}

function decrypt(encrypted_text, passphrase) {
    var decrypted = CryptoJS.AES.decrypt(encrypted_text, passphrase);

    return decrypted.toString(CryptoJS.enc.Utf8);
}

function derive_key_from_text(plaintext) {
    // var salt = CryptoJS.lib.WordArray.random(128 / 8);
    var salt = plaintext;
    var key256Bits = CryptoJS.PBKDF2(plaintext, salt, { keySize: 256 / 32 });
    return key256Bits.toString();
}