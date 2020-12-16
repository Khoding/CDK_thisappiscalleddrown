import Cropper from '../../vendor/node_modules/cropperjs/dist/cropper.esm.js';

$(document).ready(function () {
    let x, y, width, height;
    let boolean = false;
    $("#id_profile_pic").change(function () {
        boolean = true;
        if (this.files && this.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                let image = document.getElementById("image");
                $("#modalCrop").modal('show');
                const cropper = new Cropper(image, {
                    aspectRatio: 1 / 1,
                    crop(event) {
                        x = event.detail.x;
                        y = event.detail.y
                        width = event.detail.width;
                        height = event.detail.height;
                    }
                });
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    $("#formUpload").click(function () {
        $("#id_x").val(x);
        $("#id_y").val(y);
        $("#id_width").val(width);
        $("#id_height").val(height);
    });
});