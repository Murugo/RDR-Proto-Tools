"""Extracts files from SWAT.ZIP from the Red Dead Revolver prototype (PS2, Jan 15, 2002).

   Example usage:

   python extract-swat.py path/to/SWAT.ZIP
"""

import os
import struct
import sys
import zlib

# If set to True, the script will also write a manifest of all files to SWAT.csv.
WRITE_FILE_MANIFEST = True

BASE_OUT_DIR = 'SWAT\\'


def err(msg):
  print(f'Error: {msg}')
  sys.exit(1)


def print_usage_and_exit():
  print('Usage: python extract-swat.py path/to/SWAT.zip')
  sys.exit(0)


def getuint32(buf, offs):
  return struct.unpack('<I', buf[offs:offs + 4])[0]


def getnuint32(buf, offs, n):
  return struct.unpack('<' + 'I' * n, buf[offs:offs + 4 * n])


def getstring(buf, offs, max_len):
  end_offs = offs
  while buf[end_offs] != 0 and end_offs - offs < max_len:
    end_offs += 1
  return buf[offs:end_offs].decode('ascii')


def get_file_entries(buf):
  if (getstring(buf, 0x0, 4)) != 'DAVE':
    err('Expected magic DAVE at position 0')

  file_count = getuint32(buf, 0x4)
  # Allocated space for maximum # of directory entries
  central_dir_size = getuint32(buf, 0x8)
  string_heap_offs = 0x800 + central_dir_size
  # Allocated space for maximum # of filename strings
  # string_heap_size = getuint32(buf, 0xC)

  files = []
  for i in range(file_count):
    filename_offs, data_offs, uncompressed_size, compressed_size = getnuint32(
        buf, 0x800 + i * 0x10, 4)
    filename = getstring(buf, filename_offs + string_heap_offs, 0x100)
    files.append([
        filename, filename_offs, data_offs, uncompressed_size, compressed_size
    ])
  return files


def write_manifest(files):
  with open('SWAT.csv', 'w+') as f:
    f.write(
        'filename,filename_offs,file_offs,uncompressed_size,compressed_size\n')
    for filename, filename_offs, data_offs, uncompressed_size, compressed_size in files:
      f.write(','.join([
          filename,
          str(filename_offs),
          str(data_offs),
          str(uncompressed_size),
          str(compressed_size)
      ]) + '\n')


def extract_files(buf, files):
  for filename, _, data_offs, uncompressed_size, compressed_size in files:
    ext = ''.join(os.path.splitext(filename)[1:])
    # ext = '.'.join(os.path.basename(filename).split('.')[1:])
    outdir = os.path.join(BASE_OUT_DIR, ext)
    if not os.path.exists(outdir):
      os.makedirs(outdir)

    path = os.path.join(outdir, filename)
    print(f'Extracting: {path}')

    with open(path, 'wb+') as f:
      if uncompressed_size > compressed_size:
        f.write(
            zlib.decompress(
                buf[data_offs:data_offs + compressed_size],
                wbits=-15,  # Raw (no header or trailer)
                bufsize=uncompressed_size))
      else:
        f.write(buf[data_offs:data_offs + uncompressed_size])


def main():
  args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
  if len(args) != 1:
    print_usage_and_exit()

  try:
    with open(args[0], 'rb') as f:
      buf = f.read()
  except FileNotFoundError:
    err(f'Unable to open for reading: {args[0]}')

  files = get_file_entries(buf)
  if WRITE_FILE_MANIFEST:
    write_manifest(files)
  extract_files(buf, files)

  print(f'\nFinished extracting {len(files)} files.')


if __name__ == '__main__':
  main()
