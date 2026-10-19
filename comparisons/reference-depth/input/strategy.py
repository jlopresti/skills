def render_batch(items, style, emit):
    rendered = []
    for item in items:
        if style == "label":
            text = item["name"].strip().title() + " / " + item["sku"].upper()
        elif style == "slug":
            text = "-".join(item["name"].lower().split()) + ":" + item["sku"].lower()
        else:
            raise ValueError("unknown style")
        emit(text)
        rendered.append(text)
    return rendered
