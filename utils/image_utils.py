from PIL import Image

STILL_IMAGE_FORMATS = [
    'image/bmp',
    'image/jpeg',
    'image/png'
]

ANIMATED_IMAGE_FORMATS = [
    'image/gif',
    'image/apng',
    'image/webp'
]


def analyse_image(image):
    results = {
        'size': image.size,
        'mode': 'global'
    }

    try:
        for i in range(len(image.tile)):
            if image.tile:
                tile = image.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != image.size:
                    results['mode'] = 'partial'
                    break
        image.seek(image.tell() + 1)

        if 'duration' in image.info:
            results['duration'] = image.info['duration']
    except EOFError:
        pass
    return results


def crop_image(crop_dim, resize_dim, path):
    image = Image.open(path)

    if image.get_format_mimetype() in ANIMATED_IMAGE_FORMATS:
        crop_animated_image(crop_dim, resize_dim, path, image)
    elif image.get_format_mimetype() in STILL_IMAGE_FORMATS:
        crop_still_image(crop_dim, resize_dim, path, image)
    else:
        pass

    image.close()


def crop_still_image(crop_dim, resize_dim, path, image):
    crop_dim = (crop_dim[0], crop_dim[1], crop_dim[2] + crop_dim[0], crop_dim[3] + crop_dim[1])
    image = image.crop(crop_dim)
    image = image.resize(resize_dim, Image.ANTIALIAS)
    image.save(path, optimize=True)


def crop_animated_image(crop_dim, resize_dim, path, image):
    # (x, y, width, height)
    crop_dim = (crop_dim[0], crop_dim[1], crop_dim[2] + crop_dim[0], crop_dim[3] + crop_dim[1])
    image_data = analyse_image(image)

    all_frames = extract_and_resize_frames(crop_dim, resize_dim, image_data, image)
    if image.get_format_mimetype() == "image/webp":
        all_frames[0].save(path, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)
    elif image.get_format_mimetype() == "image/gif" or image.get_format_mimetype() == "image/apng":
        if len(all_frames) == 1:
            all_frames[0].save(path, optimize=True)
        else:
            all_frames[0].save(path, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000, duration=image_data['duration'])


def extract_and_resize_frames(crop_dim, resize_dim, image_data, image):
    """
    Iterate the GIF, extracting each frame and resizing them


    Returns:
        An array of all frames
    """
    mode = image_data['mode']

    i = 0
    palette = image.getpalette()
    last_frame = image.convert('RGBA')

    all_frames = []

    try:
        while True:

            '''
            Si le GIF utilise une palette locale, chaque frame aura sa propre palette.
            Sinon, il appliquera une palette globale pour chaque nouvelle frame.
            '''
            if not image.getpalette():
                image.putpalette(palette)

            new_frame = Image.new('RGBA', image.size)

            '''
            
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(image, (0, 0), image.convert('RGBA'))

            new_frame = new_frame.crop(crop_dim)
            new_frame = new_frame.resize(resize_dim, Image.ANTIALIAS)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            image.seek(image.tell() + 1)
    except EOFError:
        pass
    return all_frames
