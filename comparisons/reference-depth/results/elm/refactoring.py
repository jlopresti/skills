def _prepare_settlement(rows, fee, events):
    total = fee
    accepted = []
    for row in rows:
        events.append(("item", row["sku"]))
        if row["enabled"]:
            total += row["price"] * row["units"]
            accepted.append(row)
    return total, accepted


def settle(rows, fee, events):
    events.append("start")
    total, accepted = _prepare_settlement(rows, fee, events)
    events.append(("total", total))
    for row in accepted:
        row["charged"] = True
    return total, accepted
