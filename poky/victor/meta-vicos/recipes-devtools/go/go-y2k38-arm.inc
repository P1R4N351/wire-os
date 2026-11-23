FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append:arm = " file://0001-runtime-linux-arm-use-clock_gettime64-for-y2k38.patch"
