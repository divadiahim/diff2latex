include .env

PYC = python
LATEXC = lualatex

LANGUAGE ?= python
DIFF_FILE ?= your_diff_file.diff

BUILD_DIR = build-$(LANGUAGE)
LATEX_O_DIR = $(BUILD_DIR)/latex
PDF_O_DIR = $(BUILD_DIR)/pdf

SRC_DIR = src

build:
	@mkdir -p $(LATEX_O_DIR) $(PDF_O_DIR)
	@echo "Building for language: $(LANGUAGE) with diff file: $(DIFF_FILE)"
	$(PYC) $(SRC_DIR)/diff2latex.py $(LANGUAGE) $(DIFF_FILE) > $(LATEX_O_DIR)/diff2latex.tex

build2:
	@mkdir -p $(LATEX_O_DIR) $(PDF_O_DIR)
	@echo "Building for language: $(LANGUAGE) with diff file: $(DIFF_FILE)"
	$(PYC) $(SRC_DIR)/diff2latex2.py $(LANGUAGE) $(DIFF_FILE) > $(LATEX_O_DIR)/diff2latex.tex

build-pdf:
	@echo "Compiling LaTeX to PDF..."
	$(LATEXC) -shell-escape -output-directory=$(PDF_O_DIR) $(LATEX_O_DIR)/diff2latex.tex
	@echo "PDF generated at: $(PDF_O_DIR)/diff2latex.pdf"

clean:
	@echo "Cleaning build directories..."
	rm -rf $(BUILD_DIR)
	@echo "Build directories cleaned."

.PHONY: build build-pdf clean