from datetime import datetime


def prettydate(d: datetime) -> str:
    diff = datetime.now() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return d.strftime("%d %b %y")
    elif diff.days == 1:
        return "1 day ago"
    elif diff.days > 1:
        return f"{diff.days} days ago"
    elif s <= 1:
        return "just now"
    elif s < 60:
        return f"{s} seconds ago"
    elif s < 120:
        return "1 minute ago"
    elif s < 3600:
        return f"{s / 60:.1f} minutes ago"
    elif s < 7200:
        return "1 hour ago"
    else:
        return f"{s / 3600:.1f} hours ago"
