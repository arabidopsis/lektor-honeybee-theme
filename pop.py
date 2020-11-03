import click
import os
import random
from lektor.databags import load_databag
import lorem
from datetime import datetime, timedelta
import re

R = {
    "date": lambda: (datetime.now() - timedelta(random.random() * 2000)).date(),
    "string": lambda: lorem.get_sentence(),
    "year": lambda: random.randint(1980, 2021),
    "journal": lambda: lorem.get_word().title(),
    "authors": lambda: ", ".join(
        lorem.get_word(3).title() for i in range(random.randint(1, 5))
    ),
}

S = re.compile(r"[.,:;@]+")


@click.command()
@click.argument("inifile")
def populate(inifile):
    db = load_databag(inifile)

    def gen():
        entry = {}
        for k, v in db["fields"].items():
            t = v["type"]
            if k in R:
                v = R[k]()
            else:
                v = R[t]()
            entry[k] = v
        title = entry["title"]
        title = S.sub("", title)
        id = "-".join(title.lower().split()).replace(".", "")
        t = "\n---\n".join(f"{k}: {str(v)}" for k, v in entry.items()) + "\n---\n"
        return id, t

    for _ in range(5):
        id, entry = gen()
        d = os.path.join("example-site", "content", "grassl-publications", id)
        os.makedirs(d)
        assert os.path.isdir(d), d
        with open(os.path.join(d, "contents.lr"), "w") as fp:
            fp.write(entry)


if __name__ == "__main__":
    populate()
