#!/usr/bin/env python3
"""
A simple test file to verify the file watcher is working correctly.
"""


print("Hello, File Watcher!")
print("This file should trigger the file watcher's 'file created' event.")

if __name__ == "__main__":
    print("If you modify this file, it should trigger the 'file modified' event.")

