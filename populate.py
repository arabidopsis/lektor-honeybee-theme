import os
from os.path import join
import shutil
import sys
import shutil
import random
from datetime import datetime, timedelta
import re

import click
from lektor.databags import load_databag
from lektor.utils import slugify
import lorem
from lektor.imagetools import (
    ThumbnailMode,
    compute_dimensions,
    get_quality,
    get_image_info,
    portable_popen,
    find_imagemagick,
)


def multi_select(choices):
    n = random.randint(1, len(choices))
    return ", ".join(random.sample(choices, n))


R = {
    "date": lambda d: (datetime.now() - timedelta(random.random() * 2000)).date(),
    "string": lambda d: lorem.get_sentence(),
    "markdown": lambda d: lorem.get_paragraph(3),
    "year": lambda d: random.randint(1980, 2021),
    "journal": lambda d: lorem.get_word().title(),
    "twitter": lambda d: lorem.get_word().lower(),
    "sort_key": lambda d: random.randint(1, 200),
    "authors": lambda d: ", ".join(
        lorem.get_word(3).title() for i in range(random.randint(1, 5))
    ),
    "select": lambda d: random.choice([s.strip() for s in d["choices"].split(",")]),
    "checkboxes": lambda d: multi_select([s.strip() for s in d["choices"].split(",")]),
    "pubmed": lambda d: str(random.randint(1_000_000, 9_999_999)),
}


S = re.compile(r"\s+")

# see lektor/lektor/utils.py:is_valid_id
def to_valid_id(name):
    ret = S.sub("-", name.strip())
    if ret.startswith("."):
        ret = ret.rstrip(".")
    return ret


def find_images(todir):
    imgs = os.listdir(todir)
    for j in imgs:
        f = join(todir, j)
        if j.lower().endswith((".jpeg", ".jpg")) and "bite" not in j.lower():
            yield f
        if os.path.isdir(f):
            yield from find_images(f)


def image_getter(width):
    pics = "/home/ianc/Pictures"
    all_images = list(find_images(pics))

    def get_image(todir):
        c = random.choice(all_images)
        _, fname = os.path.split(c)
        # so lektor doesn't like spaces
        tgt = to_valid_id(fname)
        src, dst = join(pics, c), join(todir, tgt)
        process_image(src, dst, width=width)
        with open(join(todir, tgt + ".lr"), "w") as fp:
            print(f"description: {lorem.get_sentence()}", file=fp)

    return get_image


def load_full_model(inifile):

    db = load_databag(inifile)
    m = db["model"]
    if "inherits" in m:
        d = os.path.dirname(inifile)
        parent = load_full_model(join(d, m["inherits"] + ".ini"))
        if "fields" in db:
            db["fields"] = {**parent["fields"], **db["fields"]}
        else:
            db["fields"] = parent["fields"]
    return db


@click.group()
def cli():
    pass


@cli.command()
@click.option("-t", "--target", help="target subdirectory of content")
@click.option("-n", "--niter", default=5, help="number of entries")
@click.option("-w", "--width", default=400, help="max width of dst image")
@click.argument("model")
def populate(model, target, niter, width):
    """Create some random `contents.lr` files from a model file."""
    db = load_full_model(model)

    add_image = lambda d: None
    if target:
        add_image = image_getter(width)

    def gen():
        entry = {}
        for k, v in db["fields"].items():
            t = v["type"]
            if k in R:
                v = R[k](v)
            else:
                v = R[t](v)
            entry[k] = v
        for key in ["title", "description", "name"]:
            if key in entry:
                id = entry[key]
                break
        else:
            raise RuntimeError(f"no title/description in {model}: {entry.keys()}")
        id = slugify(id)
        t = "\n---\n".join(f"{k}: {str(v)}" for k, v in entry.items()) + "\n---\n"
        return id, t

    for _ in range(niter):
        id, entry = gen()
        if target:
            d = os.path.join("example-site", "content", target, id)
            os.makedirs(d, exist_ok=True)
            assert os.path.isdir(d), d
            with open(os.path.join(d, "contents.lr"), "w") as fp:
                fp.write(entry)
            if "attachments" in db:
                a = db["attachments"]
                if "model" in a and a["model"] == "image-attachment":
                    add_image(d)
        else:
            print("_id:", id, "\n---")
            print(entry)


def process_image(
    source_image,
    dst_filename,
    width=None,
    height=None,
    mode=ThumbnailMode.FIT,
    quality=None,
    upscale=False,
    quiet=False,
):
    """Build image from source image, optionally compressing and resizing.

    "source_image" is the absolute path of the source in the content directory,
    "dst_filename" is the absolute path of the target in the output directory.
    """

    im = find_imagemagick()

    with open(source_image, "rb") as f:
        format, source_width, source_height = get_image_info(f)
    if format is None:
        raise RuntimeError("Cannot process unknown images")

    if mode == ThumbnailMode.FIT:
        computed_width, computed_height = compute_dimensions(
            width, height, source_width, source_height
        )
    else:
        computed_width, computed_height = width, height
    if (
        not upscale
        and mode == ThumbnailMode.FIT
        and (
            (width is not None and width >= source_width)
            or (height is not None and height >= source_height)
        )
    ):
        if not quiet:
            click.secho(
                f"{source_image} smaller than {width or ''}x{height or ''} copying..",
                fg="blue",
            )
        shutil.copy(source_image, dst_filename)
        return computed_width, computed_height, source_width, source_height

    if quality is None:
        quality = get_quality(source_image)

    resize_key = ""
    if width is not None:
        resize_key += str(width)
    if height is not None:
        resize_key += "x" + str(height)

    if mode == ThumbnailMode.STRETCH:
        resize_key += "!"

    cmdline = [im, source_image, "-auto-orient"]
    if mode == ThumbnailMode.CROP:
        cmdline += [
            "-resize",
            resize_key + "^",
            "-gravity",
            "Center",
            "-extent",
            resize_key,
        ]
    else:
        cmdline += ["-resize", resize_key]

    cmdline += ["-strip", "-colorspace", "sRGB"]
    cmdline += ["-quality", str(quality), dst_filename]

    portable_popen(cmdline).wait()
    return computed_width, computed_height, source_width, source_height


@cli.command()
@click.option("-w", "--width", default=400, help="max width of dst image")
@click.option("-u", "--upscale", is_flag=True, help="upscale images")
@click.option("-q", "--quiet", is_flag=True, help="only log changes")
@click.argument("content")
def resize(width, content, upscale, quiet):
    """Resize all images in a content directory."""
    for directory, _, files in os.walk(content):
        for f in files:
            if not f.lower().endswith((".jpeg", ".jpg", ".png", ".gif")):
                continue
            b, e = os.path.splitext(f)
            dst = b + "-resized" + e
            dst = os.path.join(directory, dst)
            src = os.path.join(directory, f)
            # swap
            os.rename(src, dst)
            w, h, ow, oh = process_image(
                dst, src, width=width, upscale=upscale, quiet=quiet
            )
            os.unlink(dst)
            if not quiet or ow != w or oh != h:
                click.secho(f"{src}: {ow}x{oh} => {w}x{h}", fg="green")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
