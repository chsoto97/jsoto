"""
Django settings for the musical project site.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-not-for-production-change-me",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if o.strip()
]

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    if ".run.app" not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(".run.app")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pages.context_processors.site_content",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email (contact form). In development, messages print to the console.
EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "web@localhost")
CONTACT_EMAIL_TO = os.environ.get("DJANGO_CONTACT_EMAIL_TO", "your@email.com")

# Site-specific content (override via environment or edit here)
# Main profile (footer, “Open on SoundCloud”). The embed uses SOUNDCLOUD_EMBED_URL when set.
SOUNDCLOUD_URL = os.environ.get(
    "SOUNDCLOUD_URL",
    "https://soundcloud.com/chui-soto",
)
# Playlist/set URL for the on-site player only. Empty = embed uses SOUNDCLOUD_URL.
SOUNDCLOUD_EMBED_URL = os.environ.get(
    "SOUNDCLOUD_EMBED_URL",
    "https://soundcloud.com/chui-soto/j-soto-demo-set",
).strip()
MIXCLOUD_URL = os.environ.get(
    "MIXCLOUD_URL",
    "https://www.mixcloud.com/chsoto97/",
)
# Featured DJ set on the Music page (watch URL; start time from &t= is preserved in the embed).
YOUTUBE_SET_URL = os.environ.get(
    "YOUTUBE_SET_URL",
    "https://www.youtube.com/watch?v=rXXeHMnII9g&t=1851s",
).strip()
YOUTUBE_SET_TITLE = os.environ.get("YOUTUBE_SET_TITLE", "Latest set").strip()

# List of {"label": str, "url": str}. Override with SOCIAL_* env vars; defaults below.
def _social_links():
    items = [
        ("Instagram", "SOCIAL_INSTAGRAM", "https://www.instagram.com/jsoto.music"),
        ("YouTube", "SOCIAL_YOUTUBE", "https://www.youtube.com/@ChuiSoto"),
        ("Bandcamp", "SOCIAL_BANDCAMP", ""),
        ("X / Twitter", "SOCIAL_TWITTER", ""),
    ]
    out = []
    for label, env_key, default in items:
        url = os.environ.get(env_key, default).strip()
        if url:
            out.append({"label": label, "url": url})
    return out


SOCIAL_LINKS = _social_links()

INSTAGRAM_URL = os.environ.get(
    "SOCIAL_INSTAGRAM",
    "https://www.instagram.com/jsoto.music",
).strip()

# Bio: HTML allowed (headings, paragraphs, blockquote). Override with BIO_TEXT in .env or edit here.
_DEFAULT_BIO = """
<h2 class="bio-heading">A Collector of Rhythms</h2>
<p>J Soto doesn’t just play sets; he documents a feeling.</p>
<p>Born from a deep curiosity for his own origins and a love for the &ldquo;warmth&rdquo; of the past, J’s sound is a bridge between generations. His studio isn’t a factory—it’s a laboratory for musical experiments. It’s where melodies from his heritage meet the crisp, driving pulse of modern electronic music.</p>
<p>This is his personal archive. From late-night studio sketches to the high-vibration energy of the dance floor, everything shared here is an extension of a simple belief: Music is the most honest form of love.</p>
<h2 class="bio-heading">The Sound &amp; The Soul</h2>
<p>For J, the booth is a space for vitality. He remixes the songs that made him, not just to keep the past alive, but to give it a new body to dance in.</p>
<p>What you hear is a curated collection of ideas. No fillers, no generic loops—just a &ldquo;Studio-to-You&rdquo; pipeline of soundscapes designed to make the body move and the soul feel seen.</p>
<h2 class="bio-heading">The Mission</h2>
<blockquote class="bio-quote"><p>I’m not interested in just filling a room with sound. I’m interested in sharing the tracks that help us reconnect—to our roots, to our health, and to each other. This site is my diary; consider the music my open letter to you.</p></blockquote>
""".strip()

BIO_TEXT = os.environ.get("BIO_TEXT", _DEFAULT_BIO).replace("\\n", "\n")

PROJECT_NAME = os.environ.get("SITE_PROJECT_NAME", "J SOTO")

# One line under the name on the home page only.
LANDING_TAGLINE = os.environ.get(
    "LANDING_TAGLINE",
    "From my studio to you: A collection of rhythms and melodies.",
)

# Logo assets (static/logos/SVG/) — blanco variants on dark UI
_LOGO_DIR = "logos/SVG"
# Playermark — header + browser tab
LOGO_MARK = f"{_LOGO_DIR}/Logo J SOTO 3_blanco.svg"
# Full wordmark — home hero
LOGO_FULL = f"{_LOGO_DIR}/Logo J SOTO 1_blanco.svg"
LOGO_FOOTER = f"{_LOGO_DIR}/Logo J SOTO 2_blanco.svg"

# Filenames in static/gallery/ that appear only on the home page (comma-separated), never on /photos/
GALLERY_HOME_ONLY = frozenset(
    n.strip()
    for n in os.environ.get("GALLERY_HOME_ONLY", "IMG_5590.JPG").split(",")
    if n.strip()
)
