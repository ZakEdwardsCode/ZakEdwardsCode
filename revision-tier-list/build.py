# Builds tier-list.html: index.html with every photo inlined, so it opens as one file.
import base64, re, pathlib
here = pathlib.Path(__file__).parent
s = (here / "index.html").read_text()
s = re.sub(r'images/([\w-]+)\.jpg', lambda m: "data:image/jpeg;base64," + base64.b64encode((here / "images" / f"{m.group(1)}.jpg").read_bytes()).decode(), s)
(here / "tier-list.html").write_text(s)
print(len(s))
