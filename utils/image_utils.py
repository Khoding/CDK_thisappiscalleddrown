"""
Fichier contenant des fonctions utilitaires pour la gestion des images.
"""

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


def crop_redim_image(crop_dim, resize_dim, path):
    """
    Rogne et redimensionne une image aux dimensions données.

    Arguments nommés :
    crop_dim -- dimensions de rognage de l'image
    resize_dim -- dimensions de redimensionnement de l'image
    path -- chemin du fichier image
    """
    image = Image.open(path)

    if image.get_format_mimetype() in ANIMATED_IMAGE_FORMATS:
        crop_and_resize_animated_image(crop_dim, resize_dim, path, image)
    elif image.get_format_mimetype() in STILL_IMAGE_FORMATS:
        crop_still_image(crop_dim, resize_dim, path, image)
    else:
        pass

    image.close()


def crop_still_image(crop_dim, resize_dim, path, image):
    """
    Rogne une image statique.

    Arguments nommés :
    crop_dim -- dimensions de rognage de l'image
    resize_dim -- dimensions de redimensionnement de l'image
    path -- chemin du fichier image
    image -- image
    """
    crop_dim = (crop_dim[0], crop_dim[1], crop_dim[2] + crop_dim[0], crop_dim[3] + crop_dim[1])
    image = image.crop(crop_dim)
    image = image.resize(resize_dim, Image.ANTIALIAS)
    image.save(path, optimize=True)


def crop_and_resize_animated_image(crop_dim, resize_dim, path, image):
    """
    Rogne une image animée.

    Arguments nommés :
    crop_dim -- dimensions de rognage de l'image
    resize_dim -- dimensions de redimensionnement de l'image
    path -- chemin du fichier image
    image -- image

    NOTE : des bugs avec la bibliothèque PIL sont fréquents.
    """

    # Format : (x, y, width, height)
    crop_dim = (crop_dim[0], crop_dim[1], crop_dim[2] + crop_dim[0], crop_dim[3] + crop_dim[1])

    frames = crop_and_resize_frames(crop_dim, resize_dim, image)

    if image.get_format_mimetype() == "image/webp":
        frames[0].save(path, save_all=True, append_images=frames[1:], loop=0)
    elif image.get_format_mimetype() == "image/gif" or image.get_format_mimetype() == "image/apng":
        if len(list(frames)) == 1:
            frames[0].save(path)
        else:
            frames[0].save(path, save_all=True, append_images=frames[1:], loop=0, duration=image.info['duration'])


def crop_and_resize_frames(crop_dim, resize_dim, image):
    """
    Rogneet redimensionne les frames des images animées.

    Arguments nommés :
    crop_dim -- dimensions de rognage de l'image
    resize_dim -- dimensions de redimensionnement de l'image
    image -- image

    NOTE : des bugs avec la bibliothèque PIL sont fréquents.
    """

    frames = []
    last_frame = image.convert('RGBA')
    palette = image.getpalette()
    try:
        while True:
            if not image.getpalette():
                image.putpalette(palette)

            new_frame = Image.new('RGBA', image.size)
            new_frame.paste(last_frame)
            new_frame.paste(image, (0, 0), image.convert('RGBA'))

            resized_frame = new_frame.crop(crop_dim)
            resized_frame = resized_frame.resize(resize_dim, Image.ANTIALIAS)

            frames.append(resized_frame)
            last_frame = new_frame
            image.seek(image.tell() + 1)

    except EOFError:
        pass
    return frames
