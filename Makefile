PYC = python
LATEXC = pdflatex

BUILD_DIR = build
LATEX_O_DIR = $(BUILD_DIR)/latex
PDF_O_DIR = $(BUILD_DIR)/pdf

SRC_DIR = src

LANGUAGE = $(word 2, $(MAKECMDGOALS))
DIFF_FILE = $(word 3, $(MAKECMDGOALS))

build-$(LANGUAGE): 
	@mkdir -p $(LATEX_O_DIR) $(PDF_O_DIR)
	@echo "Building for language: $(LANGUAGE) with diff file: $(DIFF_FILE)"
	$(PYC) $(SRC_DIR)/diff2latex.py $(LANGUAGE) $(DIFF_FILE) > $(LATEX_O_DIR)/diff2latex.tex

build-pdf: build-$(LANGUAGE) $(LATEX_O_DIR)/diff2latex.tex
	@echo "Compiling LaTeX to PDF..."
	$(LATEXC) -output-directory=$(PDF_O_DIR) $(LATEX_O_DIR)/diff2latex.tex
	@echo "PDF generated at: $(PDF_O_DIR)/diff2latex.pdf"

clean:
	@echo "Cleaning build directories..."
	rm -rf $(BUILD_DIR)
	@echo "Build directories cleaned."

.PHONY: build-$(LANGUAGE) build-pdf clean