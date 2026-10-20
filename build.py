#!/usr/bin/env python3
"""Sinh website tĩnh từ config.py + templates/ + static/ vào thư mục dist/.

Dùng:
    python build.py            # build ra dist/
    python build.py --serve    # build rồi chạy thử tại http://localhost:8000
    python build.py --check    # chỉ kiểm tra cấu hình, không ghi file
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import html
import http.server
import json
import os
import re
import shutil
import socketserver
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape

import config

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"

warnings: list[str] = []

# ---------------------------------------------------------------- icons
# Icon nét mảnh theo phong cách Lucide (ISC license).
ICONS: dict[str, str] = {
    "github": '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "youtube": '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/>',
    "arrow-up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "menu": '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "external": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
}


def icon(name: str, cls: str = "icon") -> str:
    """Trả về SVG inline (đã an toàn vì chỉ lấy từ bảng ICONS)."""
    body = ICONS.get(name, ICONS["link"])
    return (
        f'<svg class="{html.escape(cls)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
        f'focusable="false">{body}</svg>'
    )


# ---------------------------------------------------------------- helpers
def pick(value: Any, lang: str, fallback_lang: str) -> Any:
    """Chọn bản dịch theo ngôn ngữ; chuỗi thường được giữ nguyên."""
    if isinstance(value, dict) and ("vi" in value or "en" in value):
        return value.get(lang) or value.get(fallback_lang) or ""
    return value


def safe_url(url: str, *, allow_mailto: bool = False, label: str = "") -> str:
    """Chỉ chấp nhận http(s) (và mailto nếu cho phép). Trả về "" nếu không hợp lệ."""
    url = (url or "").strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return url
    if allow_mailto and parsed.scheme == "mailto" and parsed.path:
        return url
    warnings.append(f"URL không hợp lệ và đã bị bỏ qua ({label or 'không rõ'}): {url!r}")
    return ""


def safe_email(email: str) -> str:
    email = (email or "").strip()
    if not email:
        return ""
    if re.fullmatch(r"[^@\s<>\"',;]+@[^@\s<>\"',;]+\.[^@\s<>\"',;]+", email):
        return email
    warnings.append(f"Email không hợp lệ và đã bị bỏ qua: {email!r}")
    return ""


def safe_asset(path: str, label: str) -> str:
    """Đường dẫn tương đối tới file trong static/. Trả "" nếu thiếu file."""
    path = (path or "").strip()
    if not path:
        return ""
    if urlparse(path).scheme in ("http", "https"):
        return path
    clean = path.lstrip("/")
    if ".." in Path(clean).parts or not (STATIC / clean).is_file():
        warnings.append(f"Không tìm thấy file '{path}' trong static/ ({label}); đã bỏ qua.")
        return ""
    return clean


def site_url() -> str:
    raw = os.environ.get("SITE_URL") or config.SITE.get("url") or ""
    return safe_url(raw, label="SITE.url").rstrip("/")


def url_path_prefix(base_url: str) -> str:
    """Phần đường dẫn của site (vd /repo cho GitHub Pages project site)."""
    return urlparse(base_url).path.rstrip("/") if base_url else ""


def initials(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


# ---------------------------------------------------------------- context
def build_context(lang: str, base_url: str) -> dict[str, Any]:
    cfg = config
    default = cfg.SITE["default_lang"]
    langs: list[str] = list(cfg.SITE["languages"])
    t = functools.partial(pick, lang=lang, fallback_lang=default)
    ui = cfg.UI.get(lang) or cfg.UI[default]

    p = cfg.PROFILE
    email = safe_email(p.get("email", ""))
    resume_url = cfg.RESUME.get("url", "").strip()
    if resume_url and urlparse(resume_url).scheme in ("http", "https"):
        resume_href = safe_url(resume_url, label="RESUME.url")
        resume_external = bool(resume_href)
    else:
        resume_href = safe_asset(resume_url, "RESUME.url")
        resume_external = False

    avatar = safe_asset(p.get("avatar", ""), "PROFILE.avatar")

    # --- liên kết xã hội
    links = []
    for item in sorted(cfg.LINKS, key=lambda x: x.get("order", 0)):
        if not item.get("visible", True):
            continue
        url = safe_url(item.get("url", ""), allow_mailto=True, label=f"LINKS[{item.get('id')}]")
        if not url:
            continue
        links.append(
            {
                "id": item["id"],
                "platform": item["platform"],
                "label": item.get("custom_label") or item["platform"],
                "description": t(item.get("description", "")),
                "url": url,
                "icon": item.get("icon", "link"),
                "new_tab": bool(item.get("new_tab", True)) and not url.startswith("mailto:"),
            }
        )

    # --- dự án
    projects = []
    for item in sorted(cfg.PROJECTS, key=lambda x: x.get("order", 0)):
        cat = item.get("category", "")
        projects.append(
            {
                "id": item["id"],
                "name": t(item["name"]),
                "description": t(item.get("description", "")),
                "category": cat,
                "category_label": t(cfg.PROJECT_CATEGORIES.get(cat, cat)),
                "stack": item.get("stack", []),
                "cover": safe_asset(item.get("cover", ""), f"PROJECTS[{item['id']}].cover"),
                "repo_url": safe_url(item.get("repo_url", ""), label=f"PROJECTS[{item['id']}].repo_url"),
                "demo_url": safe_url(item.get("demo_url", ""), label=f"PROJECTS[{item['id']}].demo_url"),
                "status": item.get("status", ""),
                "role": t(item.get("role", "")),
                "features": [t(f) for f in item.get("features", [])],
                "example": bool(item.get("example")),
            }
        )
    used_cats = []
    for pr in projects:
        if pr["category"] and pr["category"] not in [c["key"] for c in used_cats]:
            used_cats.append({"key": pr["category"], "label": pr["category_label"]})

    # --- giới thiệu
    a = cfg.ABOUT
    about = {
        "summary": t(a.get("summary", "")),
        "education": [
            {k: t(v) for k, v in e.items()} for e in a.get("education", [])
        ],
        "interests": [t(i) for i in a.get("interests", [])],
        "goals": t(a.get("goals", "")),
        "philosophy": t(a.get("philosophy", "")),
        "languages": [{"name": t(x["name"]), "level": t(x.get("level", ""))} for x in a.get("languages", [])],
        "learning": [t(i) for i in a.get("learning", [])],
        "example": bool(a.get("example")),
    }

    skills = {
        "example": bool(cfg.SKILLS.get("example")),
        "groups": [
            {"name": t(g["name"]), "items": g.get("items", [])}
            for g in cfg.SKILLS.get("groups", [])
            if g.get("items")
        ],
    }

    experience = []
    for e in cfg.EXPERIENCE:
        experience.append(
            {
                "organization": t(e.get("organization", "")),
                "role": t(e.get("role", "")),
                "dates": e.get("dates", ""),
                "description": t(e.get("description", "")),
                "project_id": e.get("project_id", ""),
            }
        )

    # --- đường dẫn
    prefix = "" if lang == default else "../"
    page_path = "/" if lang == default else f"/{lang}/"
    canonical = f"{base_url}{page_path}" if base_url else ""
    alternates = []
    if base_url:
        for l in langs:
            alternates.append({"lang": l, "href": f"{base_url}{'/' if l == default else f'/{l}/'}"})
    other_langs = [l for l in langs if l != lang]
    switch = None
    if other_langs:
        target = other_langs[0]
        switch = {
            "lang": target,
            "href": "../" if target == default else (f"{target}/" if lang == default else f"../{target}/"),
            "label": cfg.UI[target]["lang_switch"],
            "aria": cfg.UI[lang]["lang_switch_label"],
        }

    og_image = f"{base_url}/assets/og-image.png" if base_url and (DIST / "assets" / "og-image.png").exists() else ""
    availability = p.get("availability", {}) or {}
    status = availability.get("status", "")

    analytics = cfg.SITE.get("analytics", {}) or {}
    plausible_domain = analytics.get("domain", "") if analytics.get("provider") == "plausible" else ""

    form_endpoint = safe_url(cfg.SITE.get("contact_form_endpoint", ""), label="SITE.contact_form_endpoint")
    if form_endpoint and not form_endpoint.startswith("https://"):
        warnings.append("contact_form_endpoint nên dùng https://")

    has_vcard = bool(cfg.SITE.get("enable_vcard") and email)

    description = t(p["intro"])
    return {
        "lang": lang,
        "ui": ui,
        "prefix": prefix,
        "site": {
            "accent": cfg.SITE["accent"],
            "default_theme": cfg.SITE["default_theme"],
            "base_url": base_url,
            "canonical": canonical,
            "alternates": alternates,
            "og_image": og_image,
            "plausible_domain": plausible_domain,
            "form_endpoint": form_endpoint,
            "has_vcard": has_vcard,
            "updated": dt.date.today().isoformat(),
            "year": dt.date.today().year,
        },
        "profile": {
            "full_name": p["full_name"],
            "display_name": p["display_name"],
            "title": p["title"],
            "avatar": avatar,
            "avatar_alt": t(p.get("avatar_alt", "")),
            "initials": initials(p["full_name"]),
            "email": email,
            "intro": description,
            "focus": [t(f) for f in p.get("focus", [])],
            "availability_status": status if status in ("open", "busy", "closed") else "",
            "availability_label": t(availability.get("label", "")),
            "example": bool(p.get("example")),
        },
        "about": about,
        "links": links,
        "projects": projects,
        "project_categories": used_cats,
        "skills": skills,
        "experience": experience,
        "resume": {
            "href": resume_href,
            "external": resume_external,
            "download_name": cfg.RESUME.get("download_name", "CV.pdf"),
        },
        "switch": switch,
        "meta_description": description[:200],
    }


# ---------------------------------------------------------------- outputs
def make_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "j2", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["icon"] = lambda name, cls="icon": __import__("markupsafe").Markup(icon(name, cls))
    return env


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        path.write_text(content, encoding="utf-8")
    else:
        path.write_bytes(content)


def make_og_image(out: Path) -> bool:
    """Ảnh chia sẻ 1200x630 tạo bằng Pillow (không dùng ảnh/số liệu bịa)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        warnings.append("Chưa cài Pillow nên không tạo được og-image.png (pip install pillow).")
        return False

    w, h = 1200, 630
    img = Image.new("RGB", (w, h), "#070b1a")
    draw = ImageDraw.Draw(img)
    # Quầng sáng nhẹ xanh/tím
    glow = Image.new("RGB", (w, h), "#070b1a")
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-200, -250, 700, 450), fill="#1b2a6b")
    gd.ellipse((600, 250, 1400, 900), fill="#3a1f77")
    from PIL import ImageFilter

    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.blend(img, glow, 0.85)
    draw = ImageDraw.Draw(img)

    def load_font(size: int, bold: bool = False):
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
        for c in candidates:
            if Path(c).exists():
                return ImageFont.truetype(c, size)
        return ImageFont.load_default()

    name = config.PROFILE["full_name"]
    title = config.PROFILE["title"]
    draw.rounded_rectangle((90, 90, 190, 190), radius=28, fill="#4f7cff")
    ini = initials(name)
    f_ini = load_font(44, True)
    bbox = draw.textbbox((0, 0), ini, font=f_ini)
    draw.text((140 - (bbox[2] - bbox[0]) / 2, 140 - (bbox[3] - bbox[1]) / 2 - bbox[1]), ini, font=f_ini, fill="white")
    draw.text((90, 270), name, font=load_font(76, True), fill="#eef1ff")
    draw.text((90, 380), title, font=load_font(36), fill="#a9b4dc")
    draw.rectangle((90, 470, 250, 476), fill="#8b6cf0")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return True


def make_vcard() -> str:
    p = config.PROFILE
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{p['full_name']}",
        f"N:;{p['full_name']};;;",
        f"TITLE:{p['title']}",
        f"EMAIL:{safe_email(p.get('email', ''))}",
    ]
    for item in config.LINKS:
        url = safe_url(item.get("url", ""), label="vcard")
        if item.get("visible", True) and url:
            lines.append(f"URL:{url}")
    lines.append("END:VCARD")
    return "\r\n".join(lines) + "\r\n"


def build() -> int:
    base_url = site_url()
    if not base_url:
        warnings.append("Chưa đặt SITE.url / SITE_URL: bỏ qua canonical, og:url, sitemap, og-image tuyệt đối.")

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)

    env = make_env()
    default = config.SITE["default_lang"]
    langs = list(config.SITE["languages"])
    if default not in langs:
        print(f"LỖI: default_lang '{default}' không nằm trong languages {langs}", file=sys.stderr)
        return 1

    make_og_image(DIST / "assets" / "og-image.png")

    index_tpl = env.get_template("index.html.j2")
    for lang in langs:
        ctx = build_context(lang, base_url)
        out = DIST / "index.html" if lang == default else DIST / lang / "index.html"
        write(out, index_tpl.render(**ctx))

    # 404: dùng đường dẫn tuyệt đối theo phần path của site (hợp với GitHub Pages project site)
    ctx404 = build_context(default, base_url)
    ctx404["root"] = (url_path_prefix(base_url) or "") + "/"
    write(DIST / "404.html", env.get_template("404.html.j2").render(**ctx404))

    # robots + sitemap
    robots = ["User-agent: *", "Allow: /"]
    if base_url:
        robots.append(f"Sitemap: {base_url}/sitemap.xml")
        urls = [f"{base_url}/"] + [f"{base_url}/{l}/" for l in langs if l != default]
        today = dt.date.today().isoformat()
        sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        sm += [f"  <url><loc>{html.escape(u)}</loc><lastmod>{today}</lastmod></url>" for u in urls]
        sm.append("</urlset>")
        write(DIST / "sitemap.xml", "\n".join(sm) + "\n")
    write(DIST / "robots.txt", "\n".join(robots) + "\n")

    # manifest
    manifest = {
        "name": config.PROFILE["full_name"],
        "short_name": config.PROFILE["display_name"],
        "start_url": "./",
        "display": "standalone",
        "background_color": "#070b1a",
        "theme_color": config.SITE["accent"],
        "icons": [{"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}],
    }
    write(DIST / "manifest.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    if config.SITE.get("enable_vcard") and safe_email(config.PROFILE.get("email", "")):
        write(DIST / "assets" / "contact.vcf", make_vcard())

    # GitHub Pages: tắt Jekyll
    write(DIST / ".nojekyll", "")
    return 0


def serve(port: int = 8000) -> None:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Xem thử tại http://localhost:{port}  (Ctrl+C để dừng)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--serve", action="store_true", help="build rồi chạy server thử")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--check", action="store_true", help="chỉ kiểm tra cấu hình")
    args = ap.parse_args()

    if args.check:
        for lang in config.SITE["languages"]:
            build_context(lang, site_url())
    else:
        code = build()
        if code:
            return code
        print(f"Đã build xong -> {DIST}")

    if warnings:
        print("\nCẢNH BÁO:")
        for w in dict.fromkeys(warnings):
            print(f"  - {w}")
    if args.serve and not args.check:
        serve(args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
