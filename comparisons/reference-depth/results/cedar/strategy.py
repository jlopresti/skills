def _render_label(item):
    return item["name"].strip().title() + " / " + item["sku"].upper()


def _render_slug(item):
    return "-".join(item["name"].lower().split()) + ":" + item["sku"].lower()


def _renderer_for(style):
    if style == "label":
        return _render_label
    if style == "slug":
        return _render_slug
    raise ValueError("unknown style")


def render_batch(items, style, emit):
    rendered = []
    renderer = None
    for item in items:
        if renderer is None:
            renderer = _renderer_for(style)
        text = renderer(item)
        emit(text)
        rendered.append(text)
    return rendered
