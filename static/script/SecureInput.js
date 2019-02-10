function SecureInput(original_input = null, encrypted_input = null) {
    this.original_input = original_input;
    this.encrypted_input = encrypted_input;

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
}