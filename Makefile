# ============================================================
# Tachistostory - Makefile
# Cross-platform build commands
# ============================================================

.PHONY: help install build-mac build-mac-onefile build-win clean test run

# Default target
help:
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║              Tachistostory - Build Commands                ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  make install           Install all dependencies"
	@echo "  make install-nuitka    Install Nuitka build dependencies"
	@echo ""
	@echo "  make build             Build standalone for current platform"
	@echo "  make build-onefile     Build single executable for current platform"
	@echo ""
	@echo "  make build-mac         Build macOS app bundle"
	@echo "  make build-mac-onefile Build macOS single executable"
	@echo "  make build-mac-dmg     Build macOS app bundle + DMG"
	@echo ""
	@echo "  make run               Run the application"
	@echo "  make test              Run tests"
	@echo "  make clean             Clean build artifacts"
	@echo ""

# Install dependencies
install:
	pip install -r requirements.txt

install-nuitka:
	pip install nuitka ordered-set zstandard

# Build commands
build:
	python build_nuitka.py

build-onefile:
	python build_nuitka.py --onefile

build-mac:
	python build_nuitka.py

build-mac-onefile:
	python build_nuitka.py --onefile

build-mac-dmg:
	./scripts/build_mac.sh

# Run application
run:
	python main.py

# Run tests
test:
	pytest

# Clean build artifacts
clean:
	rm -rf build_nuitka/
	rm -rf dist_nuitka/
	rm -rf main.build/
	rm -rf main.dist/
	rm -rf main.onefile-build/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
