import Cropper from '../../vendor/node_modules/cropperjs/dist/cropper.esm.js';

$(document).ready(function () {
    let x, y, width, height;
    let cropper;
    $("#id_profile_pic").change(function () {
        if (this.files && this.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                $("#imageCrop").attr("src", e.target.result);
                let image = document.getElementById("imageCrop");
                $("#modalCrop").modal('show');
                cropper = new Cropper(image, {
                    aspectRatio: 1 / 1,
                    crop(event) {
                        x = event.detail.x;
                        y = event.detail.y
                        width = event.detail.width;
                        height = event.detail.height;
                    },
                });
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    $("#saveImageCropped").click(function () {
        cropper.destroy();
    });

    $("#formUpload").click(function () {
        $("#id_x").val(x);
        $("#id_y").val(y);
        $("#id_width").val(width);
        $("#id_height").val(height);
    });
});