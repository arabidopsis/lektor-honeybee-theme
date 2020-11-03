import os
from os.path import join
import random
from datetime import datetime, timedelta
import re
import click
from lektor.databags import load_databag
from lektor.utils import slugify
import lorem
import shutil


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
    "checkboxes": lambda d: random.choice([s.strip() for s in d["choices"].split(",")]),
}


def add_image(todir):
    pics = "/home/ianc/Pictures"
    jpg = [
        j
        for j in os.listdir(pics)
        if j.lower().endswith((".jpeg", ".jpg")) and "bite" not in j.lower()
    ]
    c = random.choice(jpg)
    shutil.copy(join(pics, c), join(todir, c))
    with open(join(todir, c + ".lr"), "w") as fp:
        print(f"description: {lorem.get_sentence()}", file=fp)


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


@click.command()
@click.option("-t", "--target", help="target directory")
@click.option("-n", "--niter", default=5, help="number of entries")
@click.argument("model")
def populate(model, target, niter):
    """Create some random `contents.lr` files from a model file."""
    db = load_full_model(model)

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


if __name__ == "__main__":
    populate()  # pylint: disable=no-value-for-parameter
