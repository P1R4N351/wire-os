.PHONY: wirebluetoothd go_deps

GO_EXE ?= $(if $(wildcard /usr/local/go/.vicos-arm-time64-patched),/usr/local/go/bin/go,$(if $(wildcard $(HOME)/.anki/go/dist/1.26.11/go/bin/go),$(HOME)/.anki/go/dist/1.26.11/go/bin/go,$(if $(wildcard /usr/local/go/bin/go),/usr/local/go/bin/go,go)))
UPX_EXE ?= $(if $(wildcard $(HOME)/.anki/upx/dist/5.0.1/upx),$(HOME)/.anki/upx/dist/5.0.1/upx,$(if $(wildcard /usr/bin/upx),/usr/bin/upx,upx))

all: wirebluetoothd

go_deps:
	@echo "$$($(GO_EXE) version)" && $(GO_EXE) mod download

wirebluetoothd: go_deps
	mkdir -p build
	GOARCH=arm GOARM=7 $(GO_EXE) build -tags vicos -ldflags '-w -s' -o build/wirebluetoothd
	$(UPX_EXE) --best --lzma build/wirebluetoothd
