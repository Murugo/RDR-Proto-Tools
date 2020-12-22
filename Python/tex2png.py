"""Converts a .TEX image to .PNG. Some image types may be unsupported.

   Example usage:

   python tex2png.py path/to/image.tex

   Optionally, you can provide the output path for the .PNG file:

   python tex2png.py path/to/image.text path/to/output.png
"""

import os
import png
import struct
import sys


def err(msg):
  print(f'Error: {msg}')
  sys.exit(1)


def print_usage_and_exit():
  print('Usage: python tex2png.py path/to/image.tex [path/to/output.png]')
  sys.exit(0)


def getuint16(buf, offs):
  return struct.unpack('<H', buf[offs:offs + 2])[0]


def getnuint8(buf, offs, n):
  return buf[offs:offs + n]


def from_8_bit_indexed(buf, width, height):
  rows = []
  # Each clut entry is in BGRA.
  clut = [
      list(getnuint8(buf, i * 0x4 + 0xE, 3)[::-1]) + [buf[i * 0x4 + 0x11]]
      for i in range(0x100)
  ]
  data_offs = 0x40E
  for _ in range(height):
    row = []
    for _ in range(width):
      c = clut[buf[data_offs]]
      data_offs += 1
      row.extend(c)
    rows = [row] + rows
  return rows


def from_4_bit_indexed(buf, width, height):
  rows = []
  # Each clut entry is in BGRA.
  clut = [
      list(getnuint8(buf, i * 0x4 + 0xE, 3)[::-1]) + [buf[i * 0x4 + 0x11]]
      for i in range(0x10)
  ]
  data_offs = 0x4E
  for _ in range(height):
    row = []
    for _ in range(width // 2):
      p = buf[data_offs]
      c1 = clut[p & 0xF]
      c2 = clut[(p >> 4) & 0xF]
      data_offs += 1
      row.extend(c1)
      row.extend(c2)
    rows = [row] + rows
  return rows


def from_rgb888(buf, width, height):
  rows = []
  data_offs = 0xE
  for _ in range(height):
    row = []
    for _ in range(width):
      c = getnuint8(buf, data_offs, 3)
      row.extend(c)
      row.append(0xFF)
      data_offs += 3
    rows = [row] + rows
  return rows


def from_rgba8888(buf, width, height):
  rows = []
  data_offs = 0xE
  for _ in range(height):
    row = []
    for _ in range(width):
      c = getnuint8(buf, data_offs, 4)
      row.extend(c)
      data_offs += 4
    rows = [row] + rows
  return rows


def from_rgba4444(buf, width, height):
  rows = []
  data_offs = 0xE
  for _ in range(height):
    row = []
    for _ in range(width):
      p = getuint16(buf, data_offs)
      r = p & 0xF
      g = (p >> 4) & 0xF
      b = (p >> 8) & 0xF
      a = (p >> 12) & 0xF
      row.extend([r, g, b, a])
      data_offs += 2
    rows = [row] + rows
  return rows


def main():
  args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
  if len(args) not in (1, 2):
    print_usage_and_exit()

  input_path = args[0]
  output_path = args[1] if len(args) > 1 else '{}.png'.format(
      os.path.splitext(input_path)[0])

  try:
    with open(input_path, 'rb') as f:
      buf = f.read()
  except FileNotFoundError:
    err(f'Unable to open for reading: {input_path}')

  width = getuint16(buf, 0x0)
  height = getuint16(buf, 0x2)
  tex_type = getuint16(buf, 0x4)

  if tex_type in (0x1, 0xE):
    rows = from_8_bit_indexed(buf, width, height)
  elif tex_type in (0xF, 0x10):
    rows = from_4_bit_indexed(buf, width, height)
  elif tex_type == 0x11:
    rows = from_rgb888(buf, width, height)
  elif tex_type == 0x12:
    rows = from_rgba8888(buf, width, height)
  elif tex_type == 0x6:
    rows = from_rgba4444(buf, width, height)
  else:
    err(f'Unhandled image type {tex_type}')

  with open(output_path, 'wb+') as f:
    w = png.Writer(width=width, height=height, greyscale=False, alpha=True)
    w.write(f, rows)


if __name__ == '__main__':
  main()
