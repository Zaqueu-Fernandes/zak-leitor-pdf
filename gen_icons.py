#!/usr/bin/env python3
import base64, struct, zlib, os

def create_simple_png(size, bg_color, icon_color):
    """Create a minimal PNG with a PDF icon"""
    img = []
    for y in range(size):
        row = []
        for x in range(size):
            cx, cy = size//2, size//2
            r = size * 0.45
            in_circle = ((x-cx)**2 + (y-cy)**2) <= r**2
            margin = size * 0.08
            in_bg = (margin <= x < size-margin) and (margin <= y < size-margin)
            
            if in_bg:
                if in_circle:
                    row.extend(list(icon_color) + [255])
                else:
                    row.extend(list(bg_color) + [255])
            else:
                row.extend([0, 0, 0, 0])
        img.append(bytes(row))
    
    def make_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)
    raw = b''.join(b'\x00' + row for row in img)
    idat = zlib.compress(raw)
    
    png = b'\x89PNG\r\n\x1a\n'
    png += make_chunk(b'IHDR', ihdr)
    png += make_chunk(b'IDAT', idat)
    png += make_chunk(b'IEND', b'')
    return png

os.makedirs('icons', exist_ok=True)

bg = (15, 14, 23)
accent = (255, 140, 90)

for size in [192, 512]:
    png_data = create_simple_png(size, bg, accent)
    with open(f'icons/icon-{size}.png', 'wb') as f:
        f.write(png_data)
    print(f"Created icons/icon-{size}.png")
