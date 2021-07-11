#!/usr/bin/python
# -*- coding: utf8 -*-
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import platform
import sys
import marshal
import types
if (sys.version_info.major != 2 or sys.version_info.minor != 7):
  sys.exit("This application requires Python 2.7.")
if len(sys.argv) != 2:
  sys.exit("usage: main.py <flag>")
flag = sys.argv[1]
if len(flag) >= 32:
  sys.exit("Meh.")
alphabet = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}-_")
for ch in flag:
  if ch not in alphabet:
    sys.exit("No.")
loader = '\x78\x9c\xe5\x56\x4b\x6f\x1c\x45\x10\xee\x9d\xdd\x38\x71\x30\x89\xc3\x2b\xe1\x12\xae\x3e\x85\x7e\x3f\x24\x84\x40\x40\x24\x2e\x11\xb2\x85\x84\x10\x44\xea\xee\xaa\xb6\x1d\x2f\x10\xb2\xc3\x53\xce\x29\xfc\x6f\xf8\xba\x37\x16\x56\x24\x40\x3e\x33\xeb\x1e\xd7\xf4\xd4\xf7\x55\x75\xd5\x37\x3d\x53\xc5\xcb\x63\xc2\xf8\x08\x63\xf3\x2e\x4e\x84\xbf\x85\x58\x0b\xf1\x35\x8c\x49\xfc\x01\x63\xd1\x67\x8e\x0e\x96\xb8\x7b\xfa\x27\x8e\x47\x75\x01\xf3\x1a\xc6\x0e\xc6\x27\x1d\xf9\x8b\x18\x30\x78\x3f\x5f\x88\xf3\x85\x78\x01\x63\x12\xb3\x10\xe7\x93\x78\xb1\x18\x86\xe8\xc6\xd9\x52\x3c\x7b\x20\x66\xd0\xcd\x93\x38\x16\x62\x5e\xf6\x1b\xdd\x69\x12\x9f\x7e\xfb\xbe\xf8\x66\x12\xcf\x97\xe2\xf9\x4a\xcc\x2b\xf1\xe4\x5a\x4f\xe0\x7c\x29\xee\x12\x06\xc0\x4f\x76\x3a\xef\xf9\x4a\x9c\x4d\xe2\xf1\x24\x7e\xfc\xb8\x33\x1e\x1d\xac\x10\xfb\x51\xed\x0b\x59\xbc\x1c\x47\x3d\xa5\xfd\xbf\x53\xda\x46\xc7\xfc\xc1\xf4\xbf\xf0\xed\xc7\xfd\x0b\xdf\xc7\x5b\x5f\x94\x12\x65\xa4\x95\x20\x94\x75\x47\xd0\x75\x41\x37\x04\xed\x0a\xba\x39\xee\xbe\x36\xe6\xf7\x04\xbd\x3e\x8c\x5b\x63\xf2\xf6\x30\x5e\x71\xbb\x35\xe0\xfb\xc3\xbe\x23\x8e\xef\x23\xf2\x1b\x3d\xf2\xdc\x25\x54\xab\xd6\xce\x2a\x65\x48\xe7\x16\x64\xd2\xd2\x64\x93\x5c\x28\xc6\xe6\x14\xb9\x31\xb1\x73\x64\x4d\x8b\x35\x6b\x5b\x24\xd7\xec\x43\xa6\x66\x93\x32\x85\x93\x1a\x24\xc6\x1a\x27\x8d\x2c\xde\xb2\xd4\xd1\x72\x05\xb0\xf8\xa8\x55\x6a\xc4\x29\x91\x27\x6f\x6d\xc8\x9c\x83\x36\x35\xd4\xc2\xde\x81\x24\x84\xd8\x1a\x58\x02\x0f\x92\x90\x10\x8b\x55\x8b\x60\x56\x4e\x07\x63\xa8\x84\xe6\x9a\x95\x81\x12\x85\x16\x90\x5f\x2a\xd5\x29\x50\xa8\x6a\x73\xf1\xce\x44\x9b\xb2\x53\xae\xca\xe2\xe4\x20\xc9\x29\x98\x6c\xbd\x09\x88\xda\x1c\x6b\x23\xb5\xd2\xc5\xb1\x29\x91\x8d\x76\x3a\xb5\xec\x73\xe2\x12\x8d\xd5\x70\xa9\x41\xe7\xea\x70\x4e\xaa\x79\x25\x4d\xdd\x92\x54\x4b\x8a\x1a\x99\x92\x1d\x56\x9f\x4a\xc8\x4a\x69\xe5\x48\x7a\x04\xad\xac\x9c\x2b\xb1\xe8\xa2\x92\x62\x89\x25\x91\x73\x32\x71\x36\x5a\x23\xf3\x5a\xfd\x20\x71\xdc\x4c\xd3\x39\xb3\xb2\x4e\x79\x5f\x0b\x92\x0c\x26\xe6\x96\x8b\x6e\x91\x92\xac\x48\xa0\xaf\xd8\x71\xb1\xd2\x29\x25\x03\xea\x8e\x44\x33\xb2\xcf\xf1\x25\x89\x4c\x26\x48\x2d\x93\x25\x5b\x01\x2b\x41\x57\x53\x8c\x46\x03\x10\xaf\x56\xe5\x24\x7b\xdf\x48\xb5\xca\x14\x4c\x73\xc5\x67\x25\x0b\x4a\x28\xa9\x18\x13\x06\x09\xd9\xa4\xbd\xb4\x35\x5a\x4f\xc9\x83\x4b\x53\x2a\xae\x7a\x36\x92\x5b\xee\x39\x4b\xa7\x0d\xa3\x92\x8c\x0a\x49\x2e\x5c\xaa\x22\xd7\x6a\xd2\x8d\x2a\x99\x6d\x8b\x61\xda\xd4\x6c\xe6\x56\x65\xf4\x2e\xc6\xda\x82\xd3\x88\x14\x62\xb6\xe8\xbf\xca\x11\x1a\x30\xec\x6b\xe0\xc4\x36\x1b\x84\xe7\xa0\x7c\xaf\x82\x56\x6d\xbb\x1c\x72\x25\x84\x22\x09\xb9\xfa\x00\xcb\x69\xdd\xaa\x82\xdc\x34\xbb\x1c\x14\xd9\x52\x74\xaa\x8d\x5a\x88\x09\x7a\x68\x35\x1b\xaa\x39\x1a\xaf\x0a\xe5\x60\x07\x49\xcc\x05\x1d\x84\x54\xa1\x07\x55\xa0\x5b\x32\x11\xed\x67\x49\xc8\xdc\x42\xcd\x06\x4d\xf1\xcd\x75\x95\x66\xa8\xae\xa7\x02\x5d\x43\x6a\x81\x8b\x0e\xb4\x25\xb1\xb5\x40\x69\x4e\x67\x09\x87\xe8\x8a\x41\x67\xd9\x95\xe4\x35\x14\x41\xae\x5a\x46\x41\x12\xfa\x80\x18\xbe\x5a\x1f\x0b\xb4\x5d\x7d\x92\x9e\x63\xe3\x6d\x77\x94\x44\x11\x0a\xf4\x61\x08\x19\xe5\x10\xbd\x54\x45\xa1\xac\x54\x95\x0e\x09\xb1\x8d\x47\x00\x76\x4d\xe2\x69\x72\x14\x64\x94\xd1\xd9\x60\x73\x86\xd4\xca\xf6\xd9\x91\x3a\x07\x69\xa8\x29\x97\x7a\xcd\x51\x4c\x50\x04\xb4\xc3\x11\x74\x21\x8b\xf2\x15\xad\xa6\x96\x52\x8b\xcc\x9e\x75\x32\xd5\x21\x69\x89\x1f\x1e\x85\xad\xec\xa9\xf5\x7a\x25\x66\xe4\x28\x1d\x13\x0a\xe0\xa4\x6c\x3e\xf9\x4a\x35\x15\x5b\xbd\x44\x09\x3d\x24\x51\x72\x44\xba\xa8\x88\x47\x94\x48\x1e\x94\x21\x6d\x6b\xa2\x39\x06\x8b\x26\x96\xac\x08\x3d\xc6\x05\x11\xe1\xa9\x41\xcf\x35\x18\xa5\xb2\x29\x54\xed\x5b\x33\x39\x70\xb5\x1a\xd5\xca\x2a\x2b\x93\x0a\x1a\x11\x38\x0e\x12\x14\x2a\x3a\x85\x4d\xc0\x43\xf7\x92\x22\xea\x0a\x08\x74\x9e\x82\x74\x81\x62\xc0\xe3\x83\xe6\x52\x94\xb9\x46\xa9\x20\x38\xa8\x2f\x61\x3b\x40\x1f\x0b\x96\x70\xd0\xb7\xc2\x57\x4e\x9b\x9b\x7d\xa3\x3a\xe1\x7a\xc6\xcf\x1e\x3c\xfd\x6d\xee\xef\xb5\x63\x9e\xfb\xcb\x6f\x33\x8d\xad\x76\xeb\xdb\x77\xdb\xc3\x3b\xff\x06\x1d\x77\xef\xf5\xf9\xd5\xc0\xed\x4e\x57\x42\xde\xbd\x84\x5c\x5d\x09\xf9\xce\x25\xe4\xce\x95\x90\x6f\x5f\x42\xde\xb8\x12\xf2\xad\x4b\xc8\x9b\x57\x42\xbe\x79\x09\xb9\x37\xf7\x6f\x86\xa3\x2f\x1f\x3e\xfc\xfc\xab\x61\x7e\x71\xf8\x19\xcc\x83\xeb\x62\x7c\x0c\x08\xb1\xe6\xef\xe7\xfe\x69\xf1\x30\xaf\x37\x3c\x66\xf2\x7a\x3d\xfe\xff\x7e\xfa\x74\xee\x6e\x27\x79\x73\xb2\x3e\x2d\x03\xbd\x39\xc9\xda\xf9\x79\xb7\x4f\xf3\xaf\x74\x7a\xcc\x9b\xf9\xa0\xc3\xe7\x9e\xdb\x66\x84\x1f\xe6\xcf\xf3\x34\x12\x1b\x4c\x33\x9c\xfe\x51\x0e\xd7\x2e\x2e\xfb\x5b\x6d\x73\x6b\x9b\xf6\xed\xdd\xc5\xbd\xc5\x6a\x5a\x2e\x96\x8b\xf1\x9e\x3d\xec\x5d\x3f\x7c\xef\xbf\xc5\x75\x03\x97\x1f\x7c\xf7\x03\xfd\xb4\xe6\x0f\xf7\x2f\x14\xb6\x37\xfd\x05\x7e\x67\xdb\x30'.decode('zlib')
loader = types.FunctionType(marshal.loads(loader), globals())
loader()
if check(flag):
  print "Well done!"
  sys.exit(0)
else:
  sys.exit("Nope.")