function generate_encrypted_fields() {
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
}