#!/usr/bin/env python3

import livereload
import build

def rebuild():
    build.main()

rebuild()

server = livereload.Server()
server.setHeader("Cache-Control", "no-store")
server.watch("projects/**/*.md", rebuild)
server.watch("snippets/**/*.md", rebuild)
server.watch("snippets/*.md", rebuild)
server.watch("templates/*.html", rebuild)
server.watch("static/style.css", rebuild)
server.watch("srcs/**/*")
server.watch("docs/static/**/*.js")
server.watch("docs/static/**/*.css")
server.watch("docs/static/**/*.png")
server.watch("docs/static/**/*.jpg")
server.watch("docs/**/*.html")
server.serve(root="docs")
