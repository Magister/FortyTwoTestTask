$(document).ready(function() {
    $(".image-picker").change(function() {
        var file_input = this;
        if (file_input.files && file_input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var img_id = '#img_' + file_input.id;
                $(img_id).attr('src', e.target.result);
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
});
