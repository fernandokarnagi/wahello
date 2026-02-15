# Makefile for BFT Protocol Implementation

.PHONY: build test run clean

build:
	go build -o bft_protocol bft_protocol.go
	@echo "Built bft_protocol"

test:
	go test -v bft_protocol_test.go bft_protocol.go
	@echo "Tests completed"

run: build
	./bft_protocol

clean:
	rm -f bft_protocol
	@echo "Cleaned up"

install-deps:
	go get -u github.com/stretchr/testify
	@echo "Dependencies installed"

all: clean build test run

help:
	@echo "Available targets:"
	@echo "  build    - Build the BFT protocol"
	@echo "  test     - Run tests"
	@echo "  run      - Run the protocol simulation"
	@echo "  clean    - Clean build artifacts"
	@echo "  install-deps - Install dependencies"
	@echo "  all      - Clean, build, test, and run"

.DEFAULT_GOAL := help