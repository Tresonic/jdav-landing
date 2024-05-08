import pathlib
from typing import Sequence
import shutil

import markdown
import markdown.extensions.fenced_code
import markdown_link_attr_modifier
import pymdownx.magiclink
import frontmatter
import jinja2

import highlighting
#import witchhazel

OUTPUT_DIR = 'docs'
PROJECTS_DIR = 'projects'
SNIPPETS_DIR = 'snippets'


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
)

markdown_ = markdown.Markdown(
    extensions=[
        "toc",
        "admonition",
        "tables",
        "abbr",
        "attr_list",
        "footnotes",
        "pymdownx.smartsymbols",
        "pymdownx.tilde",
        "pymdownx.caret",
        markdown.extensions.fenced_code.FencedCodeExtension(lang_prefix="language-"),
        pymdownx.magiclink.MagiclinkExtension(
            hide_protocol=False,
        ),
        markdown_link_attr_modifier.LinkAttrModifierExtension(
            new_tab="external_only", custom_attrs=dict(referrerpolicy="origin")
        ),
    ]
)


def copy_static():
    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        pathlib.Path("./static"), pathlib.Path(f"./{OUTPUT_DIR}/static"), dirs_exist_ok=True
    )


def get_sources(prefix: str):
    yield from pathlib.Path(".").glob(f"{prefix}/*.md")
    yield from pathlib.Path(".").glob(f"{prefix}/*/index.md")


def parse_source(source: pathlib.Path) -> frontmatter.Post:
    post = frontmatter.load(str(source))
    return post


def fixup_styles(content: str) -> str:
    content = content.replace("<table>", '<table class="table">')
    return content


def render_markdown(content: str) -> str:
    markdown_.reset()
    content = markdown_.convert(content)
    content = highlighting.highlight(content)
    content = fixup_styles(content)
    return content


def write_post(post: frontmatter.Post, content: str):
    dst = pathlib.Path(f"./{OUTPUT_DIR}/{post['stem']}")
    dst.mkdir(parents=True, exist_ok=True)

    index = dst / "index.html"

    template = jinja_env.get_template("post.html")
    rendered = template.render(post=post, content=content)

    index.write_text(rendered)


def copy_post_resources(post: frontmatter.Post):
    src = post["source"].parent
    dst = pathlib.Path(f"./{OUTPUT_DIR}/{post['stem']}")
    dst.mkdir(parents=True, exist_ok=True)

    shutil.copytree(src, dst, dirs_exist_ok=True)


def write_projects_snippets() -> (Sequence[frontmatter.Post], Sequence[frontmatter.Post]):
    projects = []
    sources = get_sources(PROJECTS_DIR)

    for source in sources:
        post = parse_source(source)
        content = render_markdown(post.content)

        post["source"] = source
        if source.match("*/index.md"):
            post["stem"] = source.parent.name
            copy_post_resources(post)
        else:
            post["stem"] = source.stem

        write_post(post, content)

        projects.append(post)

    snippets = []
    sources = get_sources(SNIPPETS_DIR)

    for source in sources:
        post = parse_source(source)
        content = render_markdown(post.content)

        post["source"] = source
        if source.match("*/index.md"):
            post["stem"] = source.parent.name
            copy_post_resources(post)
        else:
            post["stem"] = source.stem

        write_post(post, content)

        snippets.append(post)

    return projects, snippets


def write_pygments_style_sheet():
    css = highlighting.get_style_css()
    pathlib.Path(f"./{OUTPUT_DIR}/static/pygments.css").write_text(css)


def write_index(projects: Sequence[frontmatter.Post], snippets: Sequence[frontmatter.Post]):
    projects = sorted(projects, key=lambda post: post["date"], reverse=True)
    snippets = sorted(snippets, key=lambda post: post["date"], reverse=True)
    path = pathlib.Path(f"./{OUTPUT_DIR}/index.html")
    template = jinja_env.get_template("index.html")
    rendered = template.render(projects=projects, snippets=snippets)
    path.write_text(rendered)


def write_rss(posts: Sequence[frontmatter.Post]):
    posts = sorted(posts, key=lambda post: post["date"], reverse=True)
    path = pathlib.Path(f"./{OUTPUT_DIR}/feed.xml")
    template = jinja_env.get_template("rss.xml")
    rendered = template.render(posts=posts, root="lubla.de")
    path.write_text(rendered)


def write_cname():
    pathlib.Path(f"./{OUTPUT_DIR}/CNAME").write_text("lubla.de")


def main():
    copy_static()
    write_pygments_style_sheet()
    projects, snippets = write_projects_snippets()
    write_index(projects, snippets)
    write_rss(projects)
    write_cname()


if __name__ == "__main__":
    main()
