# by Manuel Velarde
from typing import List, Tuple
from io import BytesIO
from PIL import Image
import openai as ai
import requests
import random
import re



STYLE = ""
COORDINATES = (
    #     X      Y
    (   512,  1024  ),
    (  1024,   512  ),
    (  1536,  1024  ),
    (  1024,  1536  ),
    (   512,   512  ),
    (   512,  1536  ),
    (  1536,  1536  ),
    (  1536,   512  ),
    (   512,     0  ),
    (  1536,     0  ),
    (     0,   512  ),
    (     0,  1536  ),
    (   512,  2048  ),
    (  1536,  2048  ),
    (  2048,   512  ),
    (  2048,  1536  ),
    (     0,     0  ),
    (     0,  2048  ),
    (  2048,     0  ),
    (  2048,  2048  ),
)



def openai_api_key() -> str:
    """
    Read the OpenAI API key from the .OPENAI_API_KEY file in the current directory.

    Returns:
        str: The OpenAI API key as a string.

    Raises:
        SystemExit: If the .OPENAI_API_KEY file cannot be found.
    """
    try:
        with open(".OPENAI_API_KEY", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: OpenAI API key not found.")
        raise SystemExit(1)



def image_description(theme: str) -> List[str]:
    """
    Generate a list of sentences describing different scenes based on a given theme using the GPT-4 model.

    This function takes a theme as input, and it creates a conversation with the GPT-4 model.
    The AI model is instructed to be very visual when describing things.

    Args:
        theme (str): The theme for the generated scene descriptions.

    Returns:
        List[str]: A list of generated scene descriptions as strings.
    """
    request = f"Write 21 sentences each describing a different scene about {theme}"
    response = ai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are very visual when describing things."
            },
            {
                "role": "user",
                "content": request
            }
        ]
    )
    text = response["choices"][0]["message"]["content"]
    return [
        re.sub(r'^\d+\)\s+', '', s)
        for s in re.split(r"(?<=[.!?])\s+", text.strip())
        if not re.match(r"^\d+\.$", s.strip())
    ]



def generate_anchor_url(description: str) -> str:
    """
    Generate an image from a given sentence using OpenAI's DALL-E API.

    Args:
        description (str): The textual description to generate an image from.

    Returns:
        str: The URL of the generated image.
    """
    response = ai.Image.create(
        prompt=description,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']



def download_image(url: str) -> Image.Image:
    """
    Download an image from a given URL and return it as a PIL Image object.

    Args:
        url (str): The URL of the image to download.

    Returns:
        PIL.Image.Image: The downloaded image as a PIL Image object.

    Raises:
        ValueError: If the URL is not valid or the content is not an image.
    """
    response = requests.get(url)
    if response.status_code == 200 and response.headers['Content-Type'].startswith('image/'):
        return Image.open(BytesIO(response.content))
    else:
        raise ValueError("Invalid URL or content is not an image")



def create_transparent_image(width: int, height: int) -> Image.Image:
    """
    Create a transparent PIL image with the specified width and height.

    Args:
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.

    Returns:
        PIL.Image.Image: The created transparent image.
    """
    return Image.new("RGBA", (width, height), (0, 0, 0, 0))



def create_base_image(anchor: Image.Image) -> Image.Image:
    base = create_transparent_image(3072, 3072)
    x = (base.width - anchor.width) // 2
    y = (base.height - anchor.height) // 2
    base.paste(
        anchor,
        (x, y)
    )
    return base



def update_base_image(base: Image.Image, x: int, y: int, description: str) -> Image.Image:
    cropped = base.crop((x, y, x + 1024, y + 1024))
    cropped.save(f"./img/tmp.png", format="PNG")
    with open(f"./img/tmp.png", "rb") as f:
        image = f.read()
        response = ai.Image.create_edit(
            image=image,
            mask=image,
            prompt=description,
            n=1,
            size="1024x1024"
        )
    replacement = download_image(response["data"][0]["url"])
    base.paste(
        replacement,
        (x, y)
    )
    return base



def main(theme: str, number: int) -> None:
    ai.api_key = openai_api_key()
    sentences = image_description(theme)
    try:
        anchor_image = download_image(
            generate_anchor_url(
                STYLE + sentences.pop(
                    random.randint(
                        0,
                        len(sentences) - 1
                    )
                )
            )
        )
    except ValueError:
        print(sentences)
        raise SystemExit(1)
    base_image = create_base_image(anchor_image)
    for x, y in COORDINATES:
        base_image = update_base_image(
            base_image,
            x,
            y,
            STYLE + sentences.pop(
                random.randint(
                    0,
                    len(sentences) - 1
                )
            )
        )
        base_image.save("./img/base.png", format="PNG")



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(
        description="This script uses the OpenAI API to generate images."
    )
    parser.add_argument(
        "-t",
        "--theme",
        dest="theme",
        type=str,
        required=True,
        help="Topic for the generated image"
    )
    parser.add_argument(
        "-n",
        "--number",
        dest="number",
        type=int,
        required=True,
        help="Number of hidden items in image"
    )
    args = parser.parse_args()

    main(
        theme=args.theme,
        number=args.number
    )
    