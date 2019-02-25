function generate_encrypted_fields() {
    // Generates encrypted input fields
    var fields = $('.gen_enc_field');
    if (fields) {
        fields.each(function (i) {
            var name = null;
            if (this.name)
                name = this.name + "_encrypted";
            
            var id = null;
            if (this.id)
                id = this.id + "_encrypted";
            
            var HTML = $("<input/>", {
                "type": "hidden",
                "name": name,
                "id": id,
                "readonly": true,
                "required": true
            });
            HTML.insertAfter(this);
        })
    }

    //Generates password (salt+hash) fields
    var pass_fields = $('.gen_pass_field');
    if (pass_fields) {
        pass_fields.each(function (i) {
            var salt_name = null;
            var hash_name = null;
            if (this.name) {
                salt_name = this.name + "_salt";
                hash_name = this.name + "_hash";
            }
            
            var salt_id = null;
            var hash_id = null;
            if (this.id) {
                salt_id = this.id + "_salt";
                hash_id = this.id + "_hash";
            }
            
            var salt_field = $("<input/>", {
                "type": "hidden",
                "name": salt_name,
                "id": salt_id,
                "readonly": true,
                "required": true
            });
            var hash_field = $("<input/>", {
                "type": "hidden",
                "name": hash_name,
                "id": hash_id,
                "readonly": true,
                "required": true
            });
            hash_field.insertAfter(this);
            salt_field.insertAfter(this);
        })
    }

}