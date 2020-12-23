import Cropper from '../../vendor/node_modules/cropperjs/dist/cropper.esm.js';

$(document).ready(function () {
    let x, y, width, height;
    let cropper;

    $('#id_profile_pic').change(function () {
        cropLoadedImage(this, 1, 1);
    });

    $('#id_image').change(function () {
        cropLoadedImage(this, 1072, 272);
    });

    function cropLoadedImage(input, widthRatio, heightRatio) {
        if (input.files && input.files[0]) {
            if (cropper) {
                cropper.destroy();
            }
            let reader = new FileReader();
            reader.onload = function (e) {
                $('#imageCrop').attr('src', e.target.result);
                let image = document.getElementById('imageCrop');
                let modal = $('#modalCrop');
                modal.modal('show');
                cropper = new Cropper(image, {
                    viewMode: 2,
                    aspectRatio: widthRatio / heightRatio,
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
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('#formUpload').click(function () {
        $('#id_x').val(x);
        $('#id_y').val(y);
        $('#id_width').val(width);
        $('#id_height').val(height);
    });
});