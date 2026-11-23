#!/usr/bin/env python3
"""Verify ARM32 ELF binaries avoid legacy 32-bit time/stat GLIBC symbols."""

import argparse
import re
import subprocess
import sys

BAD_TIME32_NAMES = frozenset({
    "clock_getres", "clock_gettime", "clock_nanosleep", "clock_settime",
    "fstat", "fstat64", "futimens", "gettimeofday", "ioctl", "lstat",
    "lstat64", "nanosleep", "ppoll", "pselect", "pthread_cond_timedwait",
    "pthread_mutex_timedlock", "pthread_rwlock_timedrdlock",
    "pthread_rwlock_timedwrlock", "recvmmsg", "recvmsg", "select",
    "semtimedop", "sendmsg", "settimeofday", "stat", "stat64", "time",
    "timer_gettime", "timer_settime", "timerfd_gettime", "timerfd_settime",
    "utimensat",
})
SYM_RE = re.compile(r"\sUND\s+([^\s@]+)(?:@([A-Z0-9_.]+))?")


def readelf_check(tool: str, path: str) -> list[str]:
    """Return list of offending 32-bit time symbol strings for one ELF path."""
    hdr = subprocess.run([tool, "-h", path], capture_output=True, text=True, check=False)
    if hdr.returncode != 0 or "ELF32" not in hdr.stdout:
        return [f"{path}: not a valid ELF32 binary"]
    syms = subprocess.run([tool, "-Ws", "--wide", path], capture_output=True, text=True, check=False)
    if syms.returncode != 0:
        return [f"{path}: readelf -Ws failed ({syms.returncode})"]
    bad: list[str] = []
    for line in syms.stdout.splitlines():
        if " UND " not in line:
            continue
        m = SYM_RE.search(line)
        if m and m.group(1) in BAD_TIME32_NAMES:
            ver = m.group(2) or "UNVERSIONED"
            bad.append(f"{path}: legacy 32-bit symbol {m.group(1)}@{ver}")
    return bad


def main() -> int:
    """CLI entrypoint checking 1+ ARM32 ELFs for legacy 32-bit time symbols."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readelf", default="arm-linux-gnueabihf-readelf", help="readelf binary")
    parser.add_argument("elfs", nargs="+", help="ARM32 ELF files to inspect")
    args = parser.parse_args()
    failures: list[str] = []
    for path in args.elfs:
        failures.extend(readelf_check(args.readelf, path))
    if failures:
        for item in failures:
            print(f"FAIL: {item}", file=sys.stderr)
        return 1
    print(f"TIME64_ABI_PASS: checked {len(args.elfs)} ELF32 binaries (0 legacy 32-bit time symbols)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
