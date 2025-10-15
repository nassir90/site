import struct
import json

# Example data
with open("pointcloud_capture.json") as original:
    points = json.load(original)

# Flatten into sequence of floats (x, y, z, x, y, z, ...)
flat = [coord for p in points for coord in (p["x"], p["y"], p["z"])]

# Pack as little-endian 32-bit floats
blob = struct.pack("<" + "f" * len(flat), *flat)

# Write to file
with open("points.bin", "wb") as f:
    f.write(blob)

print(f"Wrote {len(points)} points ({len(blob)} bytes)")

