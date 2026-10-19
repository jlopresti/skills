def _label(item):
    return item["name"].strip().title() + " / " + item["sku"].upper()


def _slug(item):
    return "-".join(item["name"].lower().split()) + ":" + item["sku"].lower()


def _render_item(item, style):
    if style == "label":
        return _label(item)
    elif style == "slug":
        return _slug(item)
    else:
        raise ValueError("unknown style")


def render_batch(items, style, emit):
    rendered = []
    for item in items:
        text = _render_item(item, style)
        emit(text)
        rendered.append(text)
    return rendered
