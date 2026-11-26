FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# 32-bit ARM kernels built without CONFIG_COMPAT_32BIT_TIME return -ENOSYS for
# futex (240), timer_settime (258), clock_gettime (263) and nanosleep (162).
# 0001-0006 backport the upstream Go 1.26 fix (golang/go#75133): futex_time64
# and timer_settime64, selected from uname on Linux 5.1 or later. 0007 adapts
# it to go1.25. 0008 moves clock_gettime and usleep to their 64-bit variants
# under the same check (golang/go#83314). Older kernels keep the 32-bit calls.
SRC_URI:append:arm = " \
    file://0001-runtime-use-futexes-with-64-bit-time-on-Linux.patch \
    file://0002-runtime-clean-dead-architectures-from-go-build-const.patch \
    file://0003-runtime-use-timer_settime64-on-32-bit-Linux.patch \
    file://0004-runtime-merge-all-the-linux-32-and-64-bits-files-int.patch \
    file://0005-runtime-use-uname-version-check-for-64-bit-time.patch \
    file://0006-runtime-tolerate-vendor-suffixes-in-kernel-release.patch \
    file://0007-runtime-adapt-the-64-bit-time-backport-to-go1.25.patch \
    file://0008-runtime-use-64-bit-time-for-clock_gettime-and-usleep.patch \
"
