def _render_label(item):
    return item["name"].strip().title() + " / " + item["sku"].upper()


def _render_slug(item):
    return "-".join(item["name"].lower().split()) + ":" + item["sku"].lower()


def render_batch(items, style, emit):
    rendered = []
    renderer = None
    for item in items:
        if renderer is None:
            if style == "label":
                renderer = _render_label
            elif style == "slug":
                renderer = _render_slug
            else:
                raise ValueError("unknown style")
        text = renderer(item)
        emit(text)
        rendered.append(text)
    return rendered
