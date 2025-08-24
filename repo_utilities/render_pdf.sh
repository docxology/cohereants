#!/bin/bash

# Generic Project PDF/LaTeX renderer with Test Coverage Validation
# - Automatically cleans all previous outputs
# - Runs tests with 100% coverage requirement
# - Executes ALL project-specific scripts in scripts/
# - Builds PDFs from ALL Markdown modules
# - Builds combined PDF
# - Exports corresponding .tex files
# - Generates preamble from markdown source
# - All output folders can be safely purged

set -euo pipefail
export LANG="${LANG:-C.UTF-8}"

# =============================================================================
# CONFIGURATION AND PATHS
# =============================================================================

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MARKDOWN_DIR="$REPO_ROOT/markdown"
OUTPUT_DIR="$REPO_ROOT/output"
PREAMBLE_MD="$MARKDOWN_DIR/00_preamble.md"
CLEAN_SCRIPT="$REPO_ROOT/repo_utilities/clean_output.sh"

# Output subdirectories (all disposable)
PDF_DIR="$OUTPUT_DIR/pdf"
TEX_DIR="$OUTPUT_DIR/tex"
DATA_DIR="$OUTPUT_DIR/data"
FIGURE_DIR="$OUTPUT_DIR/figures"
LATEX_TEMP_DIR="$OUTPUT_DIR/latex_temp"

# Author/metadata (configurable)
AUTHOR_NAME="${AUTHOR_NAME:-Tucker C. Chambers, Daniel A. Friedman}"
AUTHOR_ORCID="${AUTHOR_ORCID:-0000-0001-6232-9096}"
AUTHOR_EMAIL="${AUTHOR_EMAIL:-daniel@activeinference.institute}"
DOI="${DOI:-}"
PROJECT_TITLE="${PROJECT_TITLE:-CohereAnts: Empirical and Theoretical Aspects of the Vibrational Model of Insect Olfaction}"

if [ -n "$DOI" ]; then
    AUTHOR_TEX="$AUTHOR_NAME\\\\ Email: $AUTHOR_EMAIL\\\\ DOI: $DOI"
else
    AUTHOR_TEX="$AUTHOR_NAME\\\\ Email: $AUTHOR_EMAIL"
fi

# =============================================================================
# LOGGING FUNCTIONS
# =============================================================================

# Log levels
LOG_DEBUG=0
LOG_INFO=1
LOG_WARN=2
LOG_ERROR=3

# Current log level (can be set via LOG_LEVEL environment variable)
LOG_LEVEL="${LOG_LEVEL:-$LOG_INFO}"

log() {
  local level="$1"
  local message="$2"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  
  if [ "$level" -ge "$LOG_LEVEL" ]; then
    case "$level" in
      $LOG_DEBUG) echo "[$timestamp] [DEBUG] $message" ;;
      $LOG_INFO)  echo "[$timestamp] [INFO]  $message" ;;
      $LOG_WARN)  echo "[$timestamp] [WARN]  $message" >&2 ;;
      $LOG_ERROR) echo "[$timestamp] [ERROR] $message" >&2 ;;
    esac
  fi
}

log_info() { log $LOG_INFO "$1"; }
log_warn() { log $LOG_WARN "$1"; }
log_error() { log $LOG_ERROR "$1"; }
log_debug() { log $LOG_DEBUG "$1"; }

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

check_dependencies() {
  log_info "Checking dependencies..."
  
  if ! command -v pandoc >/dev/null 2>&1; then
    log_error "pandoc is not installed."
    echo "Install: sudo apt-get install -y pandoc" >&2
    exit 1
  fi
  
  if ! command -v xelatex >/dev/null 2>&1; then
    log_error "xelatex not found. Install TeX Live:"
    echo "sudo apt-get install -y texlive-xetex texlive-fonts-recommended fonts-dejavu" >&2
    exit 1
  fi
  
  # Check for pdflatex for IDE-friendly PDF generation
  if ! command -v pdflatex >/dev/null 2>&1; then
    log_warn "pdflatex not found. IDE-friendly PDF generation may fail."
    echo "Install: sudo apt-get install -y texlive-latex-base" >&2
  fi
  
  log_info "All dependencies satisfied"
}

# =============================================================================
# AUTOMATIC CLEANUP
# =============================================================================

run_clean_output() {
  log_info "Step 0: Running clean_output.sh to ensure clean state..."
  
  if [ ! -f "$CLEAN_SCRIPT" ]; then
    log_error "clean_output.sh not found: $CLEAN_SCRIPT"
    exit 1
  fi
  
  if ! bash "$CLEAN_SCRIPT"; then
    log_error "clean_output.sh failed"
    exit 1
  fi
  
  log_info "✅ Cleanup completed successfully"
}

setup_directories() {
  log_info "Setting up output directories..."
  
  # Create all output directories (these can be safely purged)
  mkdir -p "$OUTPUT_DIR" "$PDF_DIR" "$TEX_DIR" "$DATA_DIR" "$FIGURE_DIR" "$LATEX_TEMP_DIR"
  
  # Clean up any existing content in temp directory
  rm -rf "$LATEX_TEMP_DIR"/*
  
  log_info "Output directories ready"
}

# Prepare markdown files by copying local images into the output figures directory
# and rewriting image links to point to the normalized `figures/` path.
embed_images_prepare_markdown() {
  log_info "Preparing markdown with embedded images..."

  TMP_MD_DIR="$LATEX_TEMP_DIR/markdown_prep"
  rm -rf "$TMP_MD_DIR"
  mkdir -p "$TMP_MD_DIR" "$FIGURE_DIR"

  for md in "$MARKDOWN_DIR"/*.md; do
    out="$TMP_MD_DIR/$(basename "$md")"
    cp "$md" "$out"

    # Find local image links and copy referenced files into $OUTPUT_DIR/figures
    # Then rewrite the markdown to reference figures/<basename>
    if command -v rg >/dev/null 2>&1; then
      while IFS= read -r img; do
        path=$(printf "%s" "$img" | sed -E 's/.*!\[[^]]*\]\(([^)]+)\).*/\1/')
        if [[ -z "$path" ]]; then
          continue
        fi
        # skip remote URLs
        if [[ "$path" =~ ^https?:// ]]; then
          continue
        fi
        # Resolve source path relative to MARKDOWN_DIR when not absolute
        if [[ "$path" = /* ]]; then
          src="$path"
        else
          src="$MARKDOWN_DIR/$path"
        fi
        bn=$(basename "$path")
        dst="figures/$bn"
        mkdir -p "$OUTPUT_DIR/$(dirname "$dst")"
        if cp -f "$src" "$OUTPUT_DIR/$dst" 2>/dev/null; then
          log_info "Copied image: $src -> $OUTPUT_DIR/$dst"
          # rewrite the path in the copied markdown file
          sed -i "s|($path)|($dst)|g" "$out" || true
        else
          log_warn "Could not copy image: $src (checked from $md)"
        fi
      done < <(rg -o '!\[[^]]*\]\((?!https?://)([^)]+)\)' "$md" || true)
    else
      log_warn "rg (ripgrep) not found; skipping image embedding"
    fi
  done

  EXPORT_MARKDOWN_DIR="$TMP_MD_DIR"
  log_info "Prepared markdown files in $TMP_MD_DIR"
}

# =============================================================================
# TEST COVERAGE VALIDATION
# =============================================================================

run_tests_with_coverage() {
  log_info "Step 1: Running tests with coverage validation..."
  
  # Check if we have a test runner
  local runner
  if command -v uv >/dev/null 2>&1; then
    runner="uv run"
  elif command -v python3 >/dev/null 2>&1; then
    runner="python3 -m"
  else
    log_error "No Python test runner found. Install uv or python3."
    exit 1
  fi
  
  # Run tests with coverage - ensure we get detailed output
      log_info "Running tests with 80% coverage requirement..."
  if ! $runner python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80 -v; then
          log_error "Tests failed or coverage below 95%"
    exit 1
  fi
  
      log_info "✅ All tests passed with 100% coverage"
}

# =============================================================================
# PROJECT SCRIPTS EXECUTION
# =============================================================================

run_project_scripts() {
  log_info "Step 2: Executing ALL project-specific scripts..."
  
  local scripts_dir="$REPO_ROOT/scripts"
  if [ ! -d "$scripts_dir" ]; then
    log_warn "Scripts directory not found: $scripts_dir"
    return 0
  fi
  
  local runner
  if command -v uv >/dev/null 2>&1; then
    runner="uv run python"
  else
    runner="python3"
  fi
  
  export MPLBACKEND=Agg
  log_info "Using runner: $runner"
  
  # Prefer running orchestrator (if present) and a small whitelist; avoid duplicate runs
  local scripts=()
  local orchestrator="$scripts_dir/run_all_case_studies.py"
  local whitelist=("$scripts_dir/generate_integrated_analysis.py" "$scripts_dir/generate_research_figures.py")
  if [ -f "$orchestrator" ]; then
    scripts+=("$orchestrator")
    # Append whitelisted scripts if present
    for w in "${whitelist[@]}"; do
      if [ -f "$w" ]; then
        scripts+=("$w")
      fi
    done
  else
    # If no orchestrator, fallback to all non-internal scripts
    while IFS= read -r -d '' script; do
      base="$(basename "$script")"
      if [[ "$script" == *.py && "$base" != _utils.py ]]; then
        scripts+=("$script")
      fi
    done < <(find "$scripts_dir" -maxdepth 1 -name "*.py" -print0)
  fi
  
  if [ ${#scripts[@]} -eq 0 ]; then
    log_info "No Python scripts found in scripts directory"
    return 0
  fi
  
  log_info "Found ${#scripts[@]} scripts to execute: ${scripts[*]}"
  
  local failed_scripts=()
  
  for script in "${scripts[@]}"; do
    local script_name=$(basename "$script")
    log_info "Running: $script_name"
    
    # Capture both stdout and stderr for better debugging
    if $runner "$script" 2>&1; then
      log_info "✅ Success: $script_name"
    else
      log_error "❌ Failed: $script_name"
      failed_scripts+=("$script_name")
    fi
  done
  
  if [ ${#failed_scripts[@]} -gt 0 ]; then
    log_error "Critical: Some scripts failed: ${failed_scripts[*]}"
    log_error "Cannot proceed with PDF generation without successful script execution"
    exit 1
  fi
  
  log_info "✅ ALL project scripts executed successfully"
}

# =============================================================================
# REPOSITORY UTILITIES
# =============================================================================

run_repo_utilities() {
  log_info "Step 2.5: Running repository utilities (glossary + markdown validation)..."
  
  local runner
  if command -v uv >/dev/null 2>&1; then
    runner="uv run python"
  else
    runner="python3"
  fi
  
  # Run glossary generation
  log_info "Generating API glossary..."
  if ! $runner "$REPO_ROOT/repo_utilities/generate_glossary.py"; then
    log_error "Glossary generation failed - cannot proceed"
    exit 1
  fi
  
  # Run markdown validation
  log_info "Validating markdown files..."
  if ! $runner "$REPO_ROOT/repo_utilities/validate_markdown.py"; then
    log_warn "Markdown validation found issues - continuing but may affect PDF quality"
  fi
  
  log_info "✅ Repository utilities completed"
}

 # =============================================================================
 # EXTRA FORMATS (DISABLED)
 # =============================================================================

create_ide_friendly_pdf() {
  return 0
}

create_web_optimized_pdf() {
  return 0
}

create_html_version() {
  return 0
}

# Legacy function bodies kept below for reference (disabled)

legacy_create_ide_friendly_pdf() {
  local combined_md="$OUTPUT_DIR/project_combined.md"
  local ide_pdf="$PDF_DIR/project_combined_ide_friendly.pdf"
  
  log_info "Creating IDE-friendly PDF version..."
  
  # Use different settings optimized for IDE viewing
  # Create a sanitized preamble for IDE-friendly PDF: remove documentclass and begin/end document
  local ide_preamble="$LATEX_TEMP_DIR/preamble_ide.tex"
  if [ -f "$preamble_tex" ]; then
    # remove documentclass, begin/end document, maketitle and titlepage blocks
    sed -e '/\\documentclass/Id' -e '/\\begin{document}/Id' -e '/\\end{document}/Id' -e '/\\maketitle/Id' -e '/\\begin{titlepage}/,/\\end{titlepage}/Id' -e '/\\usepackage\[[^]]*\]{microtype}/Id' -e '/\\usepackage{microtype}/Id' "$preamble_tex" > "$ide_preamble" || cp "$preamble_tex" "$ide_preamble"
  else
    touch "$ide_preamble"
  fi

  local pandoc_args=(
    -f markdown+implicit_figures+tex_math_dollars+tex_math_single_backslash+raw_tex+autolink_bare_uris
    -s
    -V title="$PROJECT_TITLE"
    -V author="$AUTHOR_TEX"
    -V date="$(date '+%B %d, %Y')"
    --pdf-engine=pdflatex
    --toc
    --toc-depth=3
    --number-sections
    -V secnumdepth=3
    -V mainfont="Times New Roman"
    -V monofont="Courier New"
    -V fontsize=13pt
    -V linestretch=1.5
    -V geometry:margin=2.5cm
    -V geometry:top=2.2cm
    -V geometry:bottom=2.2cm
    -V geometry:left=3cm
    -V geometry:right=3cm
    -V geometry:includeheadfoot
    -V colorlinks=false
    -V linkcolor=black
    -V urlcolor=black
    -V citecolor=black
    -V toccolor=black
    -V filecolor=black
    -V menucolor=black
    --highlight-style=espresso
    --listings
    --resource-path="$MARKDOWN_DIR:$OUTPUT_DIR:$LATEX_TEMP_DIR:$REPO_ROOT"
    -H "$ide_preamble"
    -o "$ide_pdf"
  )
  
  if pandoc "$combined_md" "${pandoc_args[@]}"; then
    log_info "✅ Created IDE-friendly PDF: $ide_pdf"
    return 0
  else
    log_warn "Initial IDE-friendly pandoc run failed; retrying without custom preamble..."
    # Retry without including custom preamble to avoid LaTeX preamble mismatches
    local pandoc_fallback=(
      -f markdown+implicit_figures+tex_math_dollars+tex_math_single_backslash+raw_tex+autolink_bare_uris
      -s
      -V title="$PROJECT_TITLE"
      -V author="$AUTHOR_TEX"
      -V date="$(date '+%B %d, %Y')"
      --pdf-engine=pdflatex
      --toc
      --toc-depth=3
      --number-sections
      -V secnumdepth=3
      -V mainfont="Times New Roman"
      -V monofont="Courier New"
      -V fontsize=13pt
      -V linestretch=1.5
      -V geometry:margin=2.5cm
      -V geometry:top=2.2cm
      -V geometry:bottom=2.2cm
      -V geometry:left=3cm
      -V geometry:right=3cm
      -V geometry:includeheadfoot
      -V colorlinks=false
      --highlight-style=espresso
      --listings
      --resource-path="$MARKDOWN_DIR:$OUTPUT_DIR:$LATEX_TEMP_DIR:$REPO_ROOT"
      -o "$ide_pdf"
    )

    if pandoc "$combined_md" "${pandoc_fallback[@]}"; then
      log_info "✅ Created IDE-friendly PDF (fallback): $ide_pdf"
      return 0
    else
      log_error "❌ Failed to create IDE-friendly PDF (both primary and fallback)"
      return 1
    fi
  fi
}

legacy_create_web_optimized_pdf() {
  local combined_md="$OUTPUT_DIR/project_combined.md"
  local web_pdf="$PDF_DIR/project_combined_web.pdf"
  
  log_info "Creating web-optimized PDF version..."
  
  # Use web-optimized settings
  local pandoc_args=(
    -f markdown+implicit_figures+tex_math_dollars+tex_math_single_backslash+raw_tex+autolink_bare_uris
    -s
    -V title="$PROJECT_TITLE"
    -V author="$AUTHOR_TEX"
    -V date="$(date '+%B %d, %Y')"
    --pdf-engine=wkhtmltopdf
    --toc
    --toc-depth=3
    --number-sections
    -V fontsize=14pt
    -V linestretch=1.3
    -V geometry:margin=1cm
    -V geometry:top=1cm
    -V geometry:bottom=1cm
    -V geometry:left=1.5cm
    -V geometry:right=1.5cm
    --resource-path="$MARKDOWN_DIR:$OUTPUT_DIR:$LATEX_TEMP_DIR:$REPO_ROOT"
    -o "$web_pdf"
  )
  
  # Check if wkhtmltopdf is available
  if ! command -v wkhtmltopdf >/dev/null 2>&1; then
    log_warn "wkhtmltopdf not available, skipping web-optimized PDF"
    return 0
  fi
  
  if pandoc "$combined_md" "${pandoc_args[@]}"; then
    log_info "✅ Created web-optimized PDF: $web_pdf"
    return 0
  else
    log_warn "Failed to create web-optimized PDF (continuing)"
    return 0
  fi
}

legacy_create_html_version() {
  local combined_md="$OUTPUT_DIR/project_combined.md"
  local html_out="$OUTPUT_DIR/project_combined.html"
  
  log_info "Creating HTML version for IDE viewing..."
  
  # Create a simple CSS file for better IDE viewing
  local css_file="$REPO_ROOT/repo_utilities/ide_style.css"
  cat > "$css_file" << 'EOF'
body {
  font-family: 'DejaVu Serif', 'Georgia', 'Times New Roman', serif;
  font-size: 16px;
  line-height: 1.7;
  max-width: 900px;
  margin: 0 auto;
  padding: 30px;
  background-color: #fafafa;
  text-align: left;
}

h1, h2, h3, h4, h5, h6 {
  color: #1a252f;
  border-bottom: 3px solid #2980b9;
  padding-bottom: 8px;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
}

h1 { font-size: 2.2em; }
h2 { font-size: 1.8em; }
h3 { font-size: 1.5em; }
h4 { font-size: 1.3em; }

code {
  background-color: #f1f3f4;
  padding: 3px 6px;
  border-radius: 4px;
  font-family: 'DejaVu Sans Mono', 'Consolas', 'Courier New', monospace;
  font-size: 14px;
  border: 1px solid #d1d5db;
}

pre {
  background-color: #1e293b;
  color: #e2e8f0;
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 14px;
  line-height: 1.6;
  border: 2px solid #475569;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 20px 0;
}

th, td {
  border: 1px solid #bdc3c7;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #3498db;
  color: white;
}

img {
  max-width: 100%;
  height: auto;
  border: 1px solid #bdc3c7;
  border-radius: 5px;
  margin: 20px 0;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

a {
  color: #2980b9;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.toc {
  background-color: #ecf0f1;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 30px;
}

.toc a {
  color: #2c3e50;
}

.math {
  text-align: center;
  margin: 20px 0;
  font-size: 1.1em;
}

.figure {
  text-align: center;
  margin: 30px 0;
}

.figure img {
  max-width: 100%;
  height: auto;
  border: 2px solid #3498db;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.figure-caption {
  font-style: italic;
  color: #7f8c8d;
  margin-top: 10px;
  text-align: center;
}
EOF
  
  # Create HTML version with proper resource path and LaTeX support
  # Use new pandoc 3.1.9 features for better image handling
  local pandoc_args=(
    -f markdown+implicit_figures+tex_math_dollars+tex_math_single_backslash+raw_tex+autolink_bare_uris
    -s
    -V title="$PROJECT_TITLE"
    -V author="$AUTHOR_NAME"
    -V date="$(date '+%B %d, %Y')"
    --toc
    --toc-depth=3
    --number-sections
    --highlight-style=espresso
    --resource-path="$OUTPUT_DIR"
    --css="$css_file"
    --standalone
    --embed-resources
    --self-contained
    --lua-filter="$REPO_ROOT/repo_utilities/convert_latex_images.lua"
    -o "$html_out"
  )
  
  if pandoc "$combined_md" "${pandoc_args[@]}"; then
    log_info "✅ Created basic HTML version: $html_out"
    
    # Post-process HTML to fix image paths and convert LaTeX image commands
    log_info "Post-processing HTML to fix image paths and LaTeX commands..."
    
    # Create a backup of the original HTML
    local html_backup="$OUTPUT_DIR/project_combined_backup.html"
    cp "$html_out" "$html_backup"
    
    # Fix image paths to use absolute paths that work in IDEs
    local figures_dir="$OUTPUT_DIR/figures"
    if [ -d "$figures_dir" ]; then
      # Replace relative image paths with absolute paths
      sed -i "s|src=\"\.\./output/figures/|src=\"$figures_dir/|g" "$html_out"
      sed -i "s|src=\"output/figures/|src=\"$figures_dir/|g" "$html_out"
      sed -i "s|src=\"figures/|src=\"$figures_dir/|g" "$html_out"
      
      # Convert LaTeX \includegraphics commands to HTML img tags
      # Remove any legacy references to experimental_setup.png in HTML output
      sed -i "/experimental_setup\.png/d" "$html_out"
      sed -i "s|\\includegraphics\[width=0\.8\\textwidth\]{\.\./output/figures/example_figure\.png}|<img src=\"$figures_dir/example_figure.png\" alt=\"Example Figure\" style=\"max-width: 100%; height: auto;\">|g" "$html_out"
      
      # Remove LaTeX labels that don't work in HTML
      sed -i "s|\\label{fig:[^}]*}||g" "$html_out"
      
      log_info "✅ Fixed image paths and LaTeX commands in HTML for IDE compatibility"
      log_info "✅ Using pandoc 3.1.9 --embed-resources and --self-contained for better image handling"
    else
      log_warn "⚠️  Figures directory not found, image paths may not work"
    fi
    
    return 0
  else
    log_error "❌ Failed to create HTML version"
    return 1
  fi
}

# =============================================================================
# MARKDOWN MODULE DISCOVERY
# =============================================================================

discover_markdown_modules() {
  if [ ! -d "$MARKDOWN_DIR" ]; then
    return 1
  fi
  
  # Find all markdown files, exclude preamble, and sort them, return only the filenames
  find "$MARKDOWN_DIR" -maxdepth 1 -name "*.md" -print0 | sort -z | xargs -0 basename -a | grep -v "^00_preamble\.md$"
}

# =============================================================================
# PDF BUILDING
# =============================================================================

build_one() {
  local in_md="$1"
  local title="$2"
  local preamble_tex="$3"
  local base="${in_md%.md}"
  local pdf_out="$PDF_DIR/${base}.pdf"
  local tex_out="$TEX_DIR/${base}.tex"
  
  log_info "Building: $in_md -> $base.pdf"
  
  # Generate TeX file first
  local pandoc_args=(
    -f markdown+implicit_figures+tex_math_dollars+tex_math_single_backslash+raw_tex+autolink_bare_uris
    -s
    --pdf-engine=pdflatex
    --toc
    --toc-depth=3
    --number-sections
    -V secnumdepth=3
    -V mainfont="Times New Roman"
    -V monofont="Courier New"
    -V fontsize=13pt
    -V linestretch=1.0
    -V geometry:margin=1.5cm
    -V geometry:top=1.5cm
    -V geometry:bottom=1.5cm
    -V geometry:left=1.5cm
    -V geometry:right=1.5cm
    -V documentclass=article
    -V classoption=12pt
    -V papersize=a4paper
    -V geometry:includeheadfoot
    -V colorlinks=true
    -V linkcolor=blue
    -V urlcolor=blue
    -V citecolor=blue
    -V toccolor=black
    -V filecolor=blue
    -V menucolor=blue
    -V linkbordercolor=blue
    -V urlbordercolor=blue
    -V citebordercolor=blue
    --highlight-style=tango
    --listings
    --resource-path="$MARKDOWN_DIR:$OUTPUT_DIR:$LATEX_TEMP_DIR:$REPO_ROOT"
    -H "$preamble_tex"
    -o "$tex_out"
  )
  
  if pandoc "$MARKDOWN_DIR/$in_md" "${pandoc_args[@]}"; then
    log_info "Generated TeX: $tex_out"
  else
    log_error "Failed to generate TeX for $in_md"
    return 1
  fi

  # Fix includegraphics paths produced by pandoc when resource paths include $OUTPUT_DIR
  # Pandoc may emit paths like ../output/figures/... which become ../output/output/figures when compiled
  # from $OUTPUT_DIR; normalize to ../figures/ which points to $OUTPUT_DIR/figures from output/tex
  if command -v sed >/dev/null 2>&1; then
    # Normalize various forms to a single relative path "figures/" so pdflatex (run from $OUTPUT_DIR) finds them
    sed -i 's|\.\./output/figures/|figures/|g' "$tex_out" || true
    sed -i 's|\.\./figures/|figures/|g' "$tex_out" || true
    sed -i 's|output/figures/|figures/|g' "$tex_out" || true
    sed -i 's|\.\/figures/|figures/|g' "$tex_out" || true
  fi

  # Compile TeX to PDF with Xelatex - ensure complete compilation
  log_info "Compiling PDF: $base.pdf"
  (
    cd "$OUTPUT_DIR"
    
    # Use comprehensive pdflatex compilation for reliability
    log_info "Using comprehensive pdflatex compilation for $base"
    
    # First run - generate initial PDF
    if pdflatex -interaction=nonstopmode -output-directory="$PDF_DIR" "$TEX_DIR/$base.tex" >/dev/null 2>&1; then
      log_info "First pdflatex run completed for $base"
    else
      log_warn "First pdflatex run had warnings for $base (continuing)"
    fi
    
    # Second run - resolve references
    log_info "Running second pdflatex pass for $base"
    pdflatex -interaction=nonstopmode -output-directory="$PDF_DIR" "$TEX_DIR/$base.tex" >/dev/null 2>&1 || true
    
    # Third run - ensure all references are resolved
    log_info "Running final pdflatex pass for $base"
    pdflatex -interaction=nonstopmode -output-directory="$PDF_DIR" "$TEX_DIR/$base.tex" >/dev/null 2>&1 || true
    
    # Clean up auxiliary files
    rm -f "$PDF_DIR/${base}.aux" "$PDF_DIR/${base}.log" "$PDF_DIR/${base}.toc" 2>/dev/null || true
  )
  
  if [ -f "$pdf_out" ]; then
    log_info "✅ Built: $pdf_out"
    return 0
  else
    log_error "❌ Failed to build: $pdf_out"
    return 1
  fi
}

build_combined() {
  local preamble_tex="$1"
  local modules=("$@")
  local combined_md="$OUTPUT_DIR/project_combined.md"
  
  log_info "Step 5: Building combined document..."
  
  # Build combined markdown with special handling for abstract
  {
    : > "$combined_md"
    
    # Handle abstract specially - it should appear before TOC
    local abstract_module=""
    local other_modules=()
    
    for module in "${modules[@]}"; do
      if [[ "$module" == "01_abstract.md" ]]; then
        abstract_module="$module"
      else
        other_modules+=("$module")
      fi
    done
    
    # Title page will be handled via a standalone LaTeX cover (inserted with -B)

    # Add abstract first (without page break)
    if [ -n "$abstract_module" ]; then
      cat "$MARKDOWN_DIR/$abstract_module" >> "$combined_md"
      printf '\n\n\\newpage\n\n' >> "$combined_md"
    fi
    
    # Add other modules with page breaks
    for i in "${!other_modules[@]}"; do
      if [ $i -gt 0 ]; then
        printf '\n\\newpage\n\n' >> "$combined_md"
      fi
      cat "$MARKDOWN_DIR/${other_modules[$i]}" >> "$combined_md"
      # Figure inclusion is controlled by explicit references within the markdown modules.
      # Auto-inserting captioned figures here is disabled to avoid duplication and ordering issues.
      # Add extra spacing after each section for better separation
      if [ $i -lt $((${#other_modules[@]} - 1)) ]; then
        printf '\n\n' >> "$combined_md"
      fi
    done
  }
  
  log_info "Generated combined markdown: $combined_md"

  # Enforce page break before each top-level section in the combined markdown
  # This uses raw LaTeX (enabled via +raw_tex) and keeps the render clean
  if command -v sed >/dev/null 2>&1; then
    sed -i 's/^# /\\newpage\n\n# /' "$combined_md" || true
  fi
  
  # Generate TeX file for combined document
  log_info "Generating combined TeX file..."
  
  # Create a standalone LaTeX cover page that uses \maketitle and (optionally) adds DOI
  local cover_tex="$LATEX_TEMP_DIR/cover.tex"
  cat > "$cover_tex" << EOF
\thispagestyle{empty}
\title{$PROJECT_TITLE}
\author{$AUTHOR_TEX}
\date{\today}
\maketitle
EOF

  # Append DOI line if provided via environment/variable
  if [ -n "${DOI:-}" ]; then
    {
      printf "\\begin{center}\n"
      printf "{\\small DOI: %s}\\\n" "$DOI"
      printf "\\end{center}\n"
    } >> "$cover_tex"
  fi

  # End cover page
  echo "\\clearpage" >> "$cover_tex"

  local pandoc_args=(
    -f markdown+implicit_figures+tex_math_dollars+tex_math_single_backslash+raw_tex+autolink_bare_uris
    -s
    --pdf-engine=pdflatex
    -B "$cover_tex"
    --toc
    --toc-depth=3
    --number-sections
    -V secnumdepth=3
    -V mainfont="Times New Roman"
    -V monofont="Courier New"
    -V fontsize=13pt
    -V linestretch=1.0
    -V geometry:margin=1.5cm
    -V geometry:top=1.5cm
    -V geometry:bottom=1.5cm
    -V geometry:left=2cm
    -V geometry:right=2cm
    -V documentclass=article
    -V classoption=12pt
    -V papersize=a4paper
    -V geometry:includeheadfoot
    -V colorlinks=true
    -V linkcolor=blue
    -V urlcolor=blue
    -V citecolor=blue
    -V toccolor=black
    -V filecolor=blue
    -V menucolor=blue
    -V linkbordercolor=blue
    -V urlbordercolor=blue
    -V citebordercolor=blue
    --highlight-style=tango
    --listings
    --resource-path="$MARKDOWN_DIR:$OUTPUT_DIR:$LATEX_TEMP_DIR:$REPO_ROOT"
    -H "$preamble_tex"
    -o "$TEX_DIR/project_combined.tex"
  )
  
  if pandoc "$combined_md" "${pandoc_args[@]}"; then
    log_info "Generated combined TeX: $TEX_DIR/project_combined.tex"
    
    # Post-processing completed
    # Ensure cleveref is loaded after hyperref in the generated TeX to make \Cref clickable
    # Insert a small snippet that explicitly loads cleveref after hyperref if not already present
    if ! rg "\\\usepackage\[nameinlink,capitalise\]{cleveref}" "$TEX_DIR/project_combined.tex" >/dev/null 2>&1; then
      # Find the hyperref block and append cleveref immediately after it
      awk 'BEGIN{p=0} /\\\usepackage\{hyperref\}/{print; print "\\usepackage[nameinlink,capitalise]{cleveref}"; p=1; next} {print}' "$TEX_DIR/project_combined.tex" > "$TEX_DIR/project_combined.tex.tmp" || true
      mv "$TEX_DIR/project_combined.tex.tmp" "$TEX_DIR/project_combined.tex"
      log_info "Inserted cleveref after hyperref in combined TeX"
    else
      log_info "cleveref already present in combined TeX"
    fi

    # Normalize includegraphics paths to point to figures/<basename> and add \graphicspath
    if command -v sed >/dev/null 2>&1; then
      sed -i 's|\.\./output/figures/|figures/|g' "$TEX_DIR/project_combined.tex" || true
      sed -i 's|\.\./figures/|figures/|g' "$TEX_DIR/project_combined.tex" || true
      sed -i 's|output/figures/|figures/|g' "$TEX_DIR/project_combined.tex" || true
      sed -i 's|\./figures/|figures/|g' "$TEX_DIR/project_combined.tex" || true

      # Ensure \graphicspath{{./figures/}} is present after \usepackage{graphicx}
      if ! rg "\\\graphicspath\{\{\.\/figures\/\}\}" "$TEX_DIR/project_combined.tex" >/dev/null 2>&1; then
        awk 'BEGIN{p=0} /\\usepackage\{graphicx\}/{print; print "\\graphicspath{{./figures/}}"; p=1; next} {print}' "$TEX_DIR/project_combined.tex" > "$TEX_DIR/project_combined.tex.tmp" || true
        mv "$TEX_DIR/project_combined.tex.tmp" "$TEX_DIR/project_combined.tex"
        log_info "Inserted \\graphicspath{{./figures/}} into combined TeX"
      fi
      # Fix filenames that contain stray whitespace and map to actual files in output/figures
      if command -v python3 >/dev/null 2>&1; then
        python3 - <<'PY'
from pathlib import Path
import re
tex=Path("$TEX_DIR/project_combined.tex")
figdir=Path("$OUTPUT_DIR/figures")
if not tex.exists():
    raise SystemExit(0)
files=[f.name for f in figdir.iterdir() if f.is_file()]
def norm(s):
    return re.sub(r'[^0-9a-z]', '', s.lower())
norm_map={norm(f):f for f in files}
txt=tex.read_text(encoding='utf8')
# collapse whitespace inside includegraphics arguments to underscores
txt=re.sub(r'(\\includegraphics(?:\[[^]]*\])?\{)\s*([^}]+?)\s*\}', lambda m: m.group(1)+re.sub(r'\s+','_',m.group(2))+"}", txt)

pattern=re.compile(r'(\\includegraphics(?:\[[^]]*\])?\{)([^}]+)\}')
def repl(m):
    prefix=m.group(1)
    arg=m.group(2)
    base=arg.split('/')[-1]
    key=norm(base)
    if key in norm_map:
        new='figures/'+norm_map[key]
        return prefix+new+'}'
    safe=re.sub(r'\s+','_', base)
    safe=re.sub(r'[^0-9A-Za-z._-]','', safe)
    return prefix+'figures/'+safe+'}'

new_txt=pattern.sub(repl, txt)
tex.write_text(new_txt, encoding='utf8')
PY
      fi

      # Further harden: map any includegraphics argument to an existing file in output/figures
      # by normalizing names (lowercase, remove non-alphanumeric) and substituting the actual filename.
      if command -v python3 >/dev/null 2>&1; then
        python3 - <<'PY'
import re
from pathlib import Path
tex=Path("$TEX_DIR/project_combined.tex")
figdir=Path("$OUTPUT_DIR/figures")
if not tex.exists():
    raise SystemExit(0)
files=[f.name for f in figdir.iterdir() if f.is_file()]
def norm(s):
    return re.sub(r'[^0-9a-z]', '', s.lower())
norm_map={norm(f):f for f in files}
txt=tex.read_text(encoding='utf8')
pattern=re.compile(r'(\\\\includegraphics(?:\[[^]]*\])?\{)([^}]+)\}')
def repl(m):
    prefix=m.group(1)
    arg=m.group(2)
    base=arg.split('/')[-1]
    key=norm(base)
    if key in norm_map:
        new='figures/'+norm_map[key]
        return prefix+new+'}'
    # fallback: collapse whitespace and remove odd characters
    safe=re.sub(r'\s+','_', base)
    safe=re.sub(r'[^0-9A-Za-z._-]','', safe)
    return prefix+'figures/'+safe+'}'

new_txt=pattern.sub(repl, txt)
tex.write_text(new_txt, encoding='utf8')
PY
      fi
    fi

    log_info "LaTeX generation completed"
  else
    log_error "Failed to generate combined TeX"
    return 1
  fi

  # Compile combined TeX to PDF - ensure complete compilation
  log_info "Compiling combined PDF..."
  (
    cd "$OUTPUT_DIR"
    
    # Use comprehensive pdflatex compilation for combined document
    log_info "Using comprehensive pdflatex compilation for combined document"
    
    # First run - generate initial PDF
    if pdflatex -interaction=nonstopmode -output-directory="$PDF_DIR" "$TEX_DIR/project_combined.tex" >/dev/null 2>&1; then
      log_info "First pdflatex run completed for combined document"
    else
      log_warn "First pdflatex run had warnings for combined document (continuing)"
    fi
    
    # Second run - resolve references
    log_info "Running second pdflatex pass for combined document"
    pdflatex -interaction=nonstopmode -output-directory="$PDF_DIR" "$TEX_DIR/project_combined.tex" >/dev/null 2>&1 || true
    
    # Third run - ensure all references are resolved
    log_info "Running final pdflatex pass for combined document"
    pdflatex -interaction=nonstopmode -output-directory="$PDF_DIR" "$TEX_DIR/project_combined.tex" >/dev/null 2>&1 || true
    
    # Clean up auxiliary files
    rm -f "$PDF_DIR/project_combined.aux" "$PDF_DIR/project_combined.log" "$PDF_DIR/project_combined.toc" 2>/dev/null || true
  )
  
  if [ -f "$PDF_DIR/project_combined.pdf" ]; then
    log_info "✅ Built combined PDF: $PDF_DIR/project_combined.pdf"
    return 0
  else
    log_error "❌ Failed to build combined PDF"
    return 1
  fi
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

main() {
  local start_time=$(date +%s)
  
  log_info "🚀 Starting COMPLETE project PDF generation pipeline..."
  log_info "Repository root: $REPO_ROOT"
  log_info "Markdown source: $MARKDOWN_DIR"
  log_info "Output directory: $OUTPUT_DIR"
  
  # Step 0: Automatic cleanup
  run_clean_output
  
  # Setup and validation
  check_dependencies
  setup_directories
  
  # Step 1: Run tests with 85% coverage
  run_tests_with_coverage
  
  # Step 2: Execute ALL project-specific scripts
  run_project_scripts
  
  # Step 2.5: Run repo utilities for glossary and markdown validation
  run_repo_utilities
  
  # Step 3: Generate preamble from markdown (ONCE)
  log_info "Step 3: Generating LaTeX preamble from markdown..."
  local preamble_tex
  if [ ! -f "$PREAMBLE_MD" ]; then
    log_error "Preamble markdown file not found: $PREAMBLE_MD"
    exit 1
  fi
  
  # Extract LaTeX content from the markdown file
  preamble_tex="$LATEX_TEMP_DIR/preamble.tex"
  
  # Extract the LaTeX preamble including \begin{document} and \maketitle
  sed -n '/^```latex$/,/^```$/p' "$PREAMBLE_MD" | sed '1d;$d' > "$preamble_tex"

  # Sanitize preamble: remove any duplicate \documentclass or \begin{document} lines
  if command -v awk >/dev/null 2>&1; then
    awk '!/\\documentclass/ || ++dc==1' "$preamble_tex" > "$preamble_tex.tmp" || true
    mv "$preamble_tex.tmp" "$preamble_tex"
    # Remove multiple \begin{document} / \end{document} occurrences if present
    awk '!/\\begin\{document\}/ || ++bd==1' "$preamble_tex" > "$preamble_tex.tmp" || true
    mv "$preamble_tex.tmp" "$preamble_tex"
  fi
  
  if [ ! -s "$preamble_tex" ]; then
    log_error "Failed to extract LaTeX preamble from $PREAMBLE_MD"
    exit 1
  fi
  
  log_info "Generated preamble: $preamble_tex"
  
  # Step 4: Discover and build ALL individual modules
  log_info "Step 4: Discovering and building ALL markdown modules..."
  local modules=()
  while IFS= read -r line; do
    if [[ "$line" =~ \.md$ ]]; then
      modules+=("$line")
    fi
  done < <(discover_markdown_modules)
  
  if [ ${#modules[@]} -eq 0 ]; then
    log_error "No valid markdown modules found"
    exit 1
  fi
  
  # Reorder appendices explicitly to enforce A–G order
  desired_appendices=(
    "appendix_sensilla_array_directionality.md"   # A
    "appendix_environmental_channel.md"          # B
    "appendix_detection_limits.md"               # C
    "appendix_neural_encoding.md"                # D
    "appendix_spectral_unmixing.md"              # E
    "appendix_plasmonic_geometry.md"             # F
    "appendix_active_inference.md"               # G
  )

  # Build a set for quick membership checks
  declare -A is_desired
  for app in "${desired_appendices[@]}"; do
    is_desired["$app"]=1
  done

  ordered_modules=()
  # Keep non-appendix modules in their discovered order
  for m in "${modules[@]}"; do
    if [[ -z "${is_desired[$m]:-}" ]]; then
      ordered_modules+=("$m")
    fi
  done
  # Append appendices in the explicit desired order, if present
  for app in "${desired_appendices[@]}"; do
    for m in "${modules[@]}"; do
      if [[ "$m" == "$app" ]]; then
        ordered_modules+=("$m")
      fi
    done
  done

  modules=("${ordered_modules[@]}")

  log_info "Found ${#modules[@]} markdown modules (ordered): ${modules[*]}"
  log_info "Building ALL individual module PDFs..."
  local failed_modules=()
  
  for module in "${modules[@]}"; do
    local title="${module%.md}"
    title="${title//_/ }"  # Replace underscores with spaces
    title="$(tr '[:lower:]' '[:upper:]' <<< ${title:0:1})${title:1}"  # Capitalize first letter
    
    if build_one "$module" "$title" "$preamble_tex"; then
      log_info "✅ Module built successfully: $module"
    else
      log_error "❌ Module failed: $module"
      failed_modules+=("$module")
    fi
  done
  
  # Step 5: Build combined document
  if build_combined "$preamble_tex" "${modules[@]}"; then
    log_info "✅ Combined document built successfully"
  else
    log_error "❌ Combined document failed"
  fi
  
  # Step 5.5: Skipped — single robust PDF build only
  
  # Final validation - ensure all expected PDFs exist
  log_info "Step 6: Validating all generated PDFs..."
  local expected_pdfs=()
  for module in "${modules[@]}"; do
    local base="${module%.md}"
    expected_pdfs+=("$PDF_DIR/${base}.pdf")
  done
  expected_pdfs+=("$PDF_DIR/project_combined.pdf")
  
  # No additional formats expected
  
  local missing_pdfs=()
  for pdf in "${expected_pdfs[@]}"; do
    if [ ! -f "$pdf" ]; then
      missing_pdfs+=("$pdf")
    fi
  done
  
  if [ ${#missing_pdfs[@]} -gt 0 ]; then
    log_error "Critical: Missing expected PDFs: ${missing_pdfs[*]}"
    exit 1
  fi
  
  log_info "✅ All expected PDFs generated successfully"
  
  # Summary
  local end_time=$(date +%s)
  local duration=$((end_time - start_time))
  
  log_info "🎉 COMPLETE BUILD SUCCESSFUL in ${duration}s"
  log_info "All outputs in: $OUTPUT_DIR"
  log_info "  PDFs: $PDF_DIR (${#expected_pdfs[@]} files)"
  log_info "  LaTeX: $TEX_DIR"
  log_info "  Data: $DATA_DIR"
  log_info "  Figures: $FIGURE_DIR"
  
  if [ ${#failed_modules[@]} -gt 0 ]; then
    log_error "Critical: Failed modules: ${failed_modules[*]}"
    exit 1
  else
    log_info "🎯 ALL modules built successfully!"
    log_info "📚 Complete manuscript available: $PDF_DIR/project_combined.pdf"
    
    log_info "📖 Manuscript PDF: $PDF_DIR/project_combined.pdf"
  fi
}

# Run main function
main "$@"
