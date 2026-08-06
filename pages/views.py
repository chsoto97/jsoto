import os

from django.conf import settings
from django.shortcuts import render

_GALLERY_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".avif",
    ".bmp",
    ".tif",
    ".tiff",
    ".heic",
    ".heif",
)


def _gallery_filenames():
    gallery_dir = settings.BASE_DIR / "static" / "gallery"
    if not gallery_dir.is_dir():
        return []
    names = []
    for name in sorted(os.listdir(gallery_dir)):
        if name.startswith(".") or ":" in name:
            continue
        lower = name.lower()
        if any(lower.endswith(ext) for ext in _GALLERY_EXTENSIONS):
            names.append(name)
    return names


def _home_only_casefolds():
    return {name.casefold() for name in settings.GALLERY_HOME_ONLY}


def _is_home_only_filename(name: str) -> bool:
    return name.casefold() in _home_only_casefolds()


def _split_landscape_portrait():
    """
    Landscape / square -> photos page; portrait (taller than wide) -> home only.
    Unreadable files default to landscape so they still appear somewhere.
    """
    gallery_dir = settings.BASE_DIR / "static" / "gallery"
    landscape = []
    portrait = []
    try:
        from PIL import Image
    except ImportError:
        all_names = _gallery_filenames()
        return all_names, []

    for name in _gallery_filenames():
        if _is_home_only_filename(name):
            continue
        path = gallery_dir / name
        try:
            with Image.open(path) as im:
                w, h = im.size
            if h > w:
                portrait.append(name)
            else:
                landscape.append(name)
        except Exception:
            landscape.append(name)
    return landscape, portrait


def _home_gallery_filenames(portrait):
    """Portrait-oriented shots plus any file forced to home-only (e.g. IMG_5590.JPG)."""
    all_files = _gallery_filenames()
    forced = [n for n in all_files if _is_home_only_filename(n)]
    merged = sorted(set(portrait) | set(forced))
    return merged


def home(request):
    landscape, portrait = _split_landscape_portrait()
    return render(
        request,
        "pages/home.html",
        {"gallery_preview": _home_gallery_filenames(portrait)},
    )


def bio(request):
    return render(request, "pages/bio.html")


def music(request):
    return render(request, "pages/music.html")


def photos(request):
    landscape, _portrait = _split_landscape_portrait()
    gallery_images = [n for n in landscape if not _is_home_only_filename(n)]
    return render(
        request,
        "pages/photos.html",
        {"gallery_images": gallery_images},
    )


def contact(request):
    return render(request, "pages/contact.html")

