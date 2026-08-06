import re
import urllib.parse
from typing import Optional

from django.conf import settings


def _soundcloud_player_src(resource_url: str) -> Optional[str]:
    """resource_url can be a profile, single track, or playlist/set — SoundCloud decides the UI."""
    if not resource_url or not resource_url.strip():
        return None
    # visual=false = compact bar (short). visual=true = large artwork player (~450px tall).
    params = {
        "url": resource_url.strip(),
        "color": "#ff5500",
        "auto_play": "false",
        "hide_related": "false",
        "show_comments": "true",
        "show_user": "true",
        "show_reposts": "false",
        "show_teaser": "true",
        "visual": "false",
    }
    return "https://w.soundcloud.com/player/?" + urllib.parse.urlencode(params)


def _mixcloud_widget_src(profile_url: str) -> Optional[str]:
    if not profile_url or not profile_url.strip():
        return None
    parsed = urllib.parse.urlparse(profile_url.strip())
    slug = parsed.path.strip("/").split("/")[0]
    if not slug:
        return None
    feed_path = f"/{slug}/"
    # mini=1: compact bar. light=0: dark theme — light=1 leaves a big empty white block inside the iframe.
    params = {
        "feed": feed_path,
        "hide_cover": "1",
        "light": "0",
        "mini": "1",
    }
    return "https://www.mixcloud.com/widget/iframe/?" + urllib.parse.urlencode(params)


def _parse_youtube_start(t: str) -> Optional[int]:
    """Parse YouTube t= values like 1851, 1851s, or 30m51s into seconds."""
    t = (t or "").strip().lower()
    if not t:
        return None
    if t.isdigit():
        return int(t)
    if t.endswith("s") and t[:-1].isdigit():
        return int(t[:-1])
    match = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s?)?", t)
    if match:
        hours, minutes, seconds = match.groups()
        total = 0
        if hours:
            total += int(hours) * 3600
        if minutes:
            total += int(minutes) * 60
        if seconds:
            total += int(seconds)
        return total or None
    return None


def _youtube_embed_src(watch_url: str) -> Optional[str]:
    if not watch_url or not watch_url.strip():
        return None
    parsed = urllib.parse.urlparse(watch_url.strip())
    host = (parsed.hostname or "").lower()
    video_id = None
    start = None

    if host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0] or None
    elif "youtube.com" in host or "youtube-nocookie.com" in host:
        if parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/", 1)[1].split("/")[0]
        else:
            query = urllib.parse.parse_qs(parsed.query)
            video_id = (query.get("v") or [None])[0]
            start = (query.get("t") or query.get("start") or [None])[0]

    if not video_id:
        return None

    params = {"rel": "0", "modestbranding": "1"}
    start_seconds = _parse_youtube_start(start) if start else None
    if start_seconds:
        params["start"] = str(start_seconds)

    return f"https://www.youtube.com/embed/{video_id}?" + urllib.parse.urlencode(params)


def _footer_links():
    """SoundCloud + Mixcloud first, then env-based social links (footer + music page)."""
    out = []
    sc = (settings.SOUNDCLOUD_URL or "").strip()
    mc = (settings.MIXCLOUD_URL or "").strip()
    if sc:
        out.append({"label": "SoundCloud", "url": sc})
    if mc:
        out.append({"label": "Mixcloud", "url": mc})
    out.extend(settings.SOCIAL_LINKS)
    return out


def site_content(_request):
    sc = settings.SOUNDCLOUD_URL
    mc = settings.MIXCLOUD_URL
    embed_sc = (settings.SOUNDCLOUD_EMBED_URL or sc or "").strip()
    yt_set = (settings.YOUTUBE_SET_URL or "").strip()
    return {
        "project_name": settings.PROJECT_NAME,
        "landing_tagline": settings.LANDING_TAGLINE,
        "bio_text": settings.BIO_TEXT,
        "soundcloud_url": sc,
        "soundcloud_stream_url": embed_sc,
        "mixcloud_url": mc,
        "youtube_set_url": yt_set,
        "youtube_set_title": settings.YOUTUBE_SET_TITLE,
        "soundcloud_embed_src": _soundcloud_player_src(embed_sc),
        "mixcloud_embed_src": _mixcloud_widget_src(mc),
        "youtube_embed_src": _youtube_embed_src(yt_set),
        "social_links": settings.SOCIAL_LINKS,
        "footer_links": _footer_links(),
        "instagram_url": settings.INSTAGRAM_URL,
        "logo_mark": settings.LOGO_MARK,
        "logo_full": settings.LOGO_FULL,
        "logo_header": settings.LOGO_MARK,
        "logo_hero": settings.LOGO_FULL,
        "logo_footer": settings.LOGO_FOOTER,
    }
