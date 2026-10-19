import struct


def finalize_round(orders, depot, stock, ledger, notify):
    if not depot.get("active"):
        raise ValueError("inactive depot")
    receipt_lines = ["Depot " + depot["name"]]
    total = 0
    packed = []
    for order in orders:
        if not order["customer"].strip():
            raise ValueError("missing customer")
        order_total = 0
        parcel = []
        for line in order["lines"]:
            sku = line["sku"]
            units = line["units"]
            if units <= 0:
                raise ValueError("invalid units")
            if stock.get(sku, 0) < units:
                raise ValueError("insufficient stock")
            stock[sku] -= units
            line_total = line["price"] * units
            order_total += line_total
            parcel.append((sku, units))
            receipt_lines.append(f"{sku} x {units} = {line_total:.2f}")
        if order.get("loyal") and order_total >= 80:
            order_total *= 0.9
        if order.get("remote"):
            order_total += depot["remote_fee"]
        order_total = round(order_total, 2)
        total += order_total
        ledger.append({"customer": order["customer"], "amount": order_total})
        receipt_lines.append(f"{order['customer']} owes {order_total:.2f}")
        notify(order["customer"], "Ready at " + depot["name"])
        packed.append({"customer": order["customer"], "parcel": parcel})
    total = round(total, 2)
    receipt_lines.append(f"ROUND TOTAL {total:.2f}")
    ledger.append({"depot": depot["name"], "total": total})
    receipt = "\n".join(receipt_lines)
    return {"total": total, "packed": packed, "receipt": receipt}


def decode_station_frame(packet):
    if len(packet) != 64:
        raise ValueError("frame must contain 64 bytes")
    magic = packet[0:4]
    if magic != b"RTE1":
        raise ValueError("bad frame magic")
    version = packet[4]
    if version != 1:
        raise ValueError("unsupported frame version")
    flags = packet[5]
    if flags & 0xF0:
        raise ValueError("reserved flags are set")
    channel_count = packet[6]
    if channel_count != 4:
        raise ValueError("invalid channel count")
    if packet[7] != 0:
        raise ValueError("reserved header byte is set")
    sequence = struct.unpack_from("<I", packet, 8)[0]
    timestamp_ms = struct.unpack_from("<Q", packet, 12)[0]
    source_bytes = packet[20:28]
    terminator = source_bytes.find(b"\0")
    if terminator >= 0:
        if any(source_bytes[terminator:]):
            raise ValueError("invalid source padding")
        source_bytes = source_bytes[:terminator]
    source = source_bytes.decode("ascii")
    if not source:
        raise ValueError("missing station source")
    latitude_raw = struct.unpack_from("<i", packet, 28)[0]
    longitude_raw = struct.unpack_from("<i", packet, 32)[0]
    if not -90000000 <= latitude_raw <= 90000000:
        raise ValueError("latitude outside range")
    if not -180000000 <= longitude_raw <= 180000000:
        raise ValueError("longitude outside range")
    temperature_raw = struct.unpack_from("<h", packet, 36)[0]
    battery_mv = struct.unpack_from("<H", packet, 38)[0]
    first = struct.unpack_from("<I", packet, 40)[0]
    second = struct.unpack_from("<I", packet, 44)[0]
    third = struct.unpack_from("<I", packet, 48)[0]
    fourth = struct.unpack_from("<I", packet, 52)[0]
    declared_checksum = struct.unpack_from("<I", packet, 56)[0]
    actual_checksum = sum(packet[:56]) & 0xFFFFFFFF
    if declared_checksum != actual_checksum:
        raise ValueError("frame checksum mismatch")
    if any(packet[60:64]):
        raise ValueError("reserved trailer is set")
    channels = (first, second, third, fourth)
    status = {
        "moving": bool(flags & 1),
        "charging": bool(flags & 2),
        "alarm": bool(flags & 4),
        "calibrated": bool(flags & 8),
    }
    return {
        "sequence": sequence,
        "timestamp_ms": timestamp_ms,
        "source": source,
        "latitude": latitude_raw / 1000000,
        "longitude": longitude_raw / 1000000,
        "temperature_c": temperature_raw / 100,
        "battery_v": battery_mv / 1000,
        "channels": channels,
        "status": status,
    }
