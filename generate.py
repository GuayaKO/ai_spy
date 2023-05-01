# by Manuel Velarde


from typing import List
import openai as ai
import re


def openai_api_key() -> str:
    with open(".OPENAI_API_KEY", "r") as file:
        return file.read().strip()


ai.api_key = openai_api_key()


def image_description(theme: str) -> List[str]:
    request = f"Write 10 sentences each describing a different scene about {theme}"
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


def main(theme: str, number: int) -> None:
    # sentences = image_description(theme)
    # sentences = [
    #     'Sunlight pours through a delicate lace curtain, casting an intricate, dappled pattern upon the pale blue walls of the cozy kitchen, illuminating the gleaming marble countertops and highlighting the array of copper pots and pans hanging artfully from a wrought iron rack.',
    #     'In the homey, rustic kitchen, a large, scarred wooden table stands proudly in the middle of the space, its well-worn surface scattered with vintage enamel mixing bowls, a colorful selection of sun-ripened vegetables and a majestic, chipped ceramic jug brimming with fragrant wildflowers.',
    #     'Shadows dance across the sleek, modern kitchen as the soft glow of under-cabinet lighting gently illuminates the streamlined stainless-steel appliances and gleaming glass tile backsplash, reflecting brilliantly off the pristine black granite countertops.',
    #     'A riot of warm, vibrant colors burst forth from the bohemian-inspired kitchen, as eclectic, mismatched dishes fill the open shelves, a beautifully chaotic collection of ingredients and trinkets adorning every available surface, and lush, green potted plants adding a wild and vivacious touch.',
    #     'The comforting scent of freshly baked bread and brewing coffee fills the quaint, cottage-style kitchen, with its cheerful, pastel-painted cabinets, delicately patterned floral wallpaper, and gold-framed, botanical prints adorning the walls, evoking a sense of timeless charm and serenity.',
    #     'An air of sumptuous luxury inhabits the vast, opulent kitchen, boasting stunning, veined marble flooring, a breathtaking, crystal chandelier descending from the ornate, coffered ceiling, and an impressive, gilded mirror mounted above an intricately carved fireplace mantle.',
    #     'Echoing the simplicity and tranquility of nature, the minimalist, Scandinavian-style kitchen exudes an effortless, airy elegance, with its clean lines, crisp, white cabinetry, and carefully curated selection of functional and aesthetically pleasing wooden utensils and cookware.',
    #     'A sense of nostalgia imbues the retro-themed kitchen, with its shiny, checkerboard linoleum floor, vibrant, cherry-red appliances, and chrome-edged, Formica-topped dining table, surrounded by a row of plush, swivel-seated barstools, ready to welcome an impromptu gathering of friends and family.',
    #     "Industrial elements intermingle with vintage charm in the urban loft's kitchen, as exposed brick walls, raw concrete floors, and metal piping shelves create a gritty, yet inviting backdrop for an eclectic assortment of salvaged, cast iron cookware and well-loved, copper-bottomed pots.",
    #     'A profusion of bold, geometric shapes in contrasting black and white dominate the visually striking, Art Deco-inspired kitchen, capturing the eye with a dazzling, herringbone-tiled floor, dramatic, chevron-patterned backsplash, and a series of statement-making, hexagonal sconces casting intriguing shadows against the walls.'
    # ]
    sentences = [
        'The soft glow of the morning sunlight bathed the kitchen in a warm, comforting embrace, accentuating the honey-toned wooden cabinets, pristine white countertops, and the delicate dance of steam rising from the freshly brewed coffee.',
        'A chaotic symphony of sizzling, bubbling, and clanking emanated from the bustling kitchen, where the chefs gracefully navigated the tight space, their crisp white uniforms contrasting against the gleaming stainless steel appliances and surfaces.',
        'The rustic charm of the farmhouse kitchen inspired feelings of nostalgia, with its weathered wooden table inviting one to share a meal, surrounded by the chalky pastel tones of shabby-chic furniture and delicate floral patterns adorning the walls and dishes.',
        'Familiar and intoxicating aromas wafted through the cozy, dimly-lit kitchen, where a simmering pot of homemade tomato sauce drew attention to the well-worn stovetop, surrounded by the whimsical disorder of scattered utensils and ingredients to be used next.',
        'The sleek lines and minimalist elegance of the modern kitchen invited organization and efficiency among gleaming glass surfaces, polished metal fixtures, and the silent hum of hidden, state-of-the-art appliances waiting to bring their culinary magic to life.',
        'A riotous celebration of color permeated the eclectic bohemian kitchen, where vibrant textiles adorned the walls, mismatched chairs gathered around the table, and pots filled with a verdant jungle of herbs created a lush oasis that blurred the line between the indoors and out.',
        'The enchanting open-air kitchen perfectly blended the lush natural surroundings and ocean views with its subtle, earth-toned design elements, creating an idyllic space where one could imagine whipping up a delicious, alfresco meal on balmy summer evenings.',
        'The grand, gourmet kitchen brimmed with opulence, from luxurious marble countertops and intricately carved cabinetry, to the chandelier that dangles magnificently above the massive island, showcasing a fine collection of crystal stemware and silver-plated accessories.',
        'Following the nostalgic scent of freshly baked cookies, one is greeted by a quaint cottage-style kitchen, where flour-dusted countertops, antique enamel canisters, and the windowsill lined with plump, sunbathing houseplants evoke memories of cherished times spent with loved ones.',
        "Late-night serenity cloaked the once-busy kitchen, now illuminated only by the soft, lunar glow of the moon shining through the window, casting long, intriguing shadows upon the walls and floor, highlighting a scene that, in just a few hours, would spring back to life with a new day's activities."
    ]
    print(sentences, len(sentences))



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(
        description="This script uses the OpenAI API to generate images."
    )
    parser.add_argument(
        "-t",
        type=str,
        required=True,
        help="Topic for the generated image"
    )
    parser.add_argument(
        "-n",
        type=int,
        required=True,
        help="Number of hidden items in image"
    )
    args = parser.parse_args()

    main(
        theme=args.t,
        number=args.n
    )
    
