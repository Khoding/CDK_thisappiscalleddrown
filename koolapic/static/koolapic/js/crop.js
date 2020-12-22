import Cropper from '../../vendor/node_modules/cropperjs/dist/cropper.esm.js';

$(document).ready(function () {
    let x, y, width, height;
    let cropper;
    $("#id_profile_pic").change(function () {
        if (cropper) {
            cropper.destroy();
        }
        console.log(this)
        if (this.files && this.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                $("#imageCrop").attr('src', e.target.result);
                let image = document.getElementById('imageCrop');
                let modal = $("#modalCrop");
                modal.modal('show');
                cropper = new Cropper(image, {
                    viewMode: 2,
                    aspectRatio: 1 / 1,
                    minCropBoxWidth: 100,
                    minCropBoxHeight: 100,
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

    $("#id_image").change(function () {
        if (cropper) {
            cropper.destroy();
        }
        console.log(this)
        if (this.files && this.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                $("#imageCrop").attr('src', e.target.result);
                let image = document.getElementById('imageCrop');
                let modal = $("#modalCrop");
                modal.modal('show');
                cropper = new Cropper(image, {
                    viewMode: 2,
                    aspectRatio: 1072 / 272,
                    minCropBoxWidth: 100,
                    minCropBoxHeight: 100,
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

    $("#formUpload").click(function () {
        $("#id_x").val(x);
        $("#id_y").val(y);
        $("#id_width").val(width);
        $("#id_height").val(height);
    });
});