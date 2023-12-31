import os
import glob
import json
import markdown
from html.parser import HTMLParser


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parse_title = False
        self.parse_summary = False
        self.title = ""
        self.summary = ""

    def handle_starttag(self, tag, attrs) -> None:
        # Fist headline
        if tag == "h1" and self.title == "":
            self.parse_title = True
        # Fisrt summary
        elif tag == "p" and self.summary == "":
            self.parse_summary = True
        else:
            self.parse_title = False
            self.parse_title = False

    def handle_data(self, data) -> None:
        if self.parse_title:
            self.title = data
        elif self.parse_summary:
            self.summary = data
        else:
            pass

    def handle_endtag(self, tag) -> None:
        if self.parse_title:
            self.parse_title = False
        if self.parse_summary:
            self.parse_summary = False


def form_data(id, title, summary, file_name):
    return {"id": id, "title": title, "summary": summary, "file_name": file_name}


def summarize():
    """Summarize and export json"""
    dir_path = "./contents/"
    markdowns = glob.glob(os.path.join(dir_path, "*.md"))
    json_data = []
    id = 0
    for md in reversed(markdowns):
        parser = Parser()
        with open(md) as f:
            parser.feed(markdown.markdown(f.read()))
        json_data.append(form_data(id, parser.title, parser.summary, md))
        id += 1
    data_size = len(json_data)
    with open("./contents/index.json", mode='w') as fout:
        fout.write("[")
        for i, data in enumerate(json_data):
            json.dump(data, fout, ensure_ascii=False)
            if i != data_size - 1:
                fout.write(",\n")
        fout.write("]")


if __name__ == "__main__":
    summarize()
