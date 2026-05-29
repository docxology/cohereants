```latex
% Minimal LaTeX preamble fragment for Pandoc-built documents
% Avoid \documentclass or loading hyperref/cleveref here (they are managed by the build pipeline)
% Provide safe unicode declarations and small custom macros only

% Map common Unicode subscripts and degree symbol to LaTeX-friendly macros

% Page layout (project override; prevents Layer 1 default 0.75in injection)
\usepackage[margin=0.2in]{geometry}

% Counter behaviour
\usepackage{chngcntr}
\counterwithout{figure}{section}
\counterwithout{table}{section}
\counterwithout{equation}{section}

% Caption formatting
\usepackage[font=small,labelfont=bf,textfont=it]{caption}
\captionsetup{justification=raggedright,singlelinecheck=false}
\captionsetup[figure]{position=bottom,skip=10pt}
\captionsetup[table]{position=top,skip=10pt}
\AtBeginEnvironment{figure}{\raggedright}

% Titlesec formatting
\usepackage{titlesec}
\titlespacing{\section}{0pt}{8pt}{4pt}
\titlespacing{\subsection}{0pt}{6pt}{3pt}
\titlespacing{\subsubsection}{0pt}{5pt}{2pt}
\titleformat{\section}{\large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\normalsize\itshape}{\thesubsubsection}{1em}{}

% Ensure each top-level section starts on a new page
\let\oldsection\section
\renewcommand{\section}{\clearpage\oldsection}

% Graphics support for figures
\usepackage{graphicx}

% Cross-references (\Cref) — load after hyperref. The pipeline does NOT
% inject cleveref, so it must be declared here (matches template_code_project).
\usepackage[capitalise,noabbrev]{cleveref}

% Small visual tweaks
\usepackage{xcolor}
\definecolor{codebg}{RGB}{245,245,245}
\definecolor{codeborder}{RGB}{200,200,200}
\definecolor{codefg}{RGB}{50,50,50}

% Setup listings safely (don't override global styles)
\usepackage{listings}
\lstset{backgroundcolor=\color{codebg},basicstyle=\small\ttfamily\color{codefg},frame=single,framerule=0.5pt,framesep=5pt}

% Keep title metadata to be inserted by build system
% (title/author/date are managed by the build pipeline)
```
