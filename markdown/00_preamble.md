```latex
% LaTeX Preamble for Insect Perception Research
\documentclass[13pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{booktabs}
% \usepackage{hyperref}  % Commented out to prevent unwanted metadata
\usepackage{color}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{fancyvrb}
\usepackage{setspace}
\usepackage{ragged2e}
\usepackage{etoolbox}

% Page geometry - more accessible margins
\geometry{margin=1in, top=1in, bottom=1in}

% Hyperref package removed to prevent unwanted metadata

% Custom colors
\definecolor{codebg}{RGB}{245, 245, 245}
\definecolor{codeborder}{RGB}{200, 200, 200}
\definecolor{codefg}{RGB}{50, 50, 50}

% Code listing setup
\lstset{
    backgroundcolor=\color{codebg},
    basicstyle=\normalsize\ttfamily\color{codefg},
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    frame=single,
    framerule=0.5pt,
    framesep=5pt,
    rulecolor=\color{codeborder},
    numbers=left,
    numbersep=5pt,
    numberstyle=\small\color{codefg}
}

% Font and spacing for accessibility
% Using standard LaTeX fonts for better compatibility
\renewcommand{\familydefault}{\rmdefault}
\renewcommand{\sfdefault}{\rmdefault}

% Single spacing for academic format
\setstretch{1.0}
\setlength{\parindent}{0.5in}
\setlength{\parskip}{0em}

% Left-justify the body text globally
\RaggedRight
\setlength{\RaggedRightParindent}{0.5in}

% Ensure body text is fully justified and consistent
\setlength{\parindent}{0.5in}

% Comprehensive numbering for figures, tables, and equations
\usepackage{chngcntr}
\counterwithout{figure}{section}
\counterwithout{table}{section}
\counterwithout{equation}{section}

% Figure and table caption formatting (left-justified)
\usepackage[font=small,labelfont=bf,textfont=it]{caption}
\captionsetup{justification=raggedright,singlelinecheck=false}
\captionsetup[figure]{position=bottom,skip=10pt}
\captionsetup[table]{position=top,skip=10pt}
% Left-align content inside all figure environments
\AtBeginEnvironment{figure}{\raggedright}

% Hyperlinks and smart cross-references
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}
\usepackage[nameinlink,capitalise]{cleveref}
% Configure cleveref names
\crefname{figure}{Figure}{Figures}
\crefname{table}{Table}{Tables}
\crefname{equation}{Equation}{Equations}

% Equation numbering and formatting
\usepackage{amsthm}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{remark}[theorem]{Remark}

% Section formatting - ensure proper academic style
\usepackage{titlesec}
\titlespacing{\section}{0pt}{12pt}{6pt}
\titlespacing{\subsection}{0pt}{10pt}{4pt}
\titlespacing{\subsubsection}{0pt}{8pt}{3pt}

% Ensure sections are left-aligned and properly formatted
\titleformat{\section}{\large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\normalsize\itshape}{\thesubsubsection}{1em}{}

% Title and author
\title{When do bugs see (infra)red? On the Visual and Infra-red in the Insect Perceptual Apparatus}
\author{Tucker Chambers \\
\small Email: tucker.chambers@example.com \\
\small ORCID: 0000-0000-0000-0000 \and 0000-0000-0000-0001 \\
Daniel A. Friedman \\
\small Email: daniel.friedman@example.com}
\date{\today}