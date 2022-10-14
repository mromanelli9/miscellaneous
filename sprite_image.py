import glob

from PIL import Image, UnidentifiedImageError
from tqdm import tqdm


def load_images(files: list[str]) -> list[Image.Image]:
    images: list[Image.Image] = []
    for _, file in files:
        try:
            images.append(Image.open(file))
        except UnidentifiedImageError as err:
            print(f"! Image not loaded: {err}")
    return images


def create_sprite_image(
    images_folder="images/*",
    output_filename="sprite.png",
    sprite_image_size=52,
    num_images_w=10,
    background_color=(0, 0, 0, 0),  # RGBA
) -> None:
    files = glob.glob(images_folder)
    images = load_images(files)

    print(f"Loaded {len(images)} images.")
    if len(images) % num_images_w != 0:
        print("! Number of images should be divisible by num_images_w")

    num_images_h = int(len(images) // num_images_w)
    output_w = sprite_image_size * num_images_w
    output_h = sprite_image_size * num_images_h

    master = Image.new(mode="RGBA", size=(output_w, output_h), color=background_color)

    print("Creating images...")
    v_offset = 0
    for count, image in enumerate(tqdm(images)):
        h_offset = (count % num_images_w) * sprite_image_size
        v_offset = (count // num_images_w) * sprite_image_size

        image.thumbnail((sprite_image_size, sprite_image_size), Image.ANTIALIAS)
        master.paste(image, (h_offset, v_offset))

    print("Saving...")
    master.save(output_filename, background=background_color)
    print("Done.")


if __name__ == "__main__":
    create_sprite_image()
