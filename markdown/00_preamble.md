```latex
% Minimal LaTeX preamble fragment for Pandoc-built documents
% Avoid \documentclass or loading hyperref/cleveref here (they are managed by the build pipeline)
% Provide safe unicode declarations and small custom macros only
\DeclareUnicodeCharacter{03BC}{\(\mu\)}
\DeclareUnicodeCharacter{03BB}{\(\lambda\)}
\DeclareUnicodeCharacter{03BD}{\(\nu\)}
\DeclareUnicodeCharacter{03C0}{\(\pi\)}
\DeclareUnicodeCharacter{03B5}{\(\epsilon\)}
\DeclareUnicodeCharacter{03B4}{\(\delta\)}

% Map common Unicode subscripts and degree symbol to LaTeX-friendly macros
\DeclareUnicodeCharacter{2080}{\textsubscript{0}}
\DeclareUnicodeCharacter{2081}{\textsubscript{1}}
\DeclareUnicodeCharacter{2082}{\textsubscript{2}}
\DeclareUnicodeCharacter{2083}{\textsubscript{3}}
\DeclareUnicodeCharacter{2084}{\textsubscript{4}}
\DeclareUnicodeCharacter{2085}{\textsubscript{5}}
\DeclareUnicodeCharacter{2086}{\textsubscript{6}}
\DeclareUnicodeCharacter{2087}{\textsubscript{7}}
\DeclareUnicodeCharacter{2088}{\textsubscript{8}}
\DeclareUnicodeCharacter{2089}{\textsubscript{9}}
\DeclareUnicodeCharacter{00B0}{\textdegree}

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
\titlespacing{\section}{0pt}{12pt}{6pt}
\titlespacing{\subsection}{0pt}{10pt}{4pt}
\titlespacing{\subsubsection}{0pt}{8pt}{3pt}
\titleformat{\section}{\large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\normalsize\itshape}{\thesubsubsection}{1em}{}

% Ensure each top-level section starts on a new page
\let\oldsection\section
\renewcommand{\section}{\clearpage\oldsection}

% Graphics support for figures
\usepackage{graphicx}

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