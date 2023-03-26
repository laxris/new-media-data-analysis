# README.md

## New Media Data Analysis Tools

This repository contains a collection of tools for new media data analysis. The tools are organized into three folders, each focused on a specific task:

1. `news-articles`: Extracts text from news articles using the trafilatura library and stores the results in a CSV file.
2. `youtube-transcript`: Downloads transcripts from YouTube videos using yt-dlp and packages them into an XLS file using a Python notebook.
3. `zeroshot-classification`: Performs zero-shot classification on the downloaded texts using OpenAI's ChatGPT API.

These command line scripts read from input CSV/text files and produce output CSV files that can be loaded into Google Sheets or exported to Gephi for network analysis.

### Folder Structure
```
.
├── news-articles
│ └── tra.py
├── youtube-transcript
│ ├── yt-transcripts.py
│ └── vtt.txt\_to\_xls.ipynb
├── zeroshot-classification
└─ zeroshot.pyi
```

### Installation and Usage

1. Clone the repository:

`git clone https://github.com/username/new-media-data-analysis.git`

2. Navigate to the desired tool folder and install the required dependencies:

`pip install -r requirements.txt`


3. Run the script with the required input files:

Running each script without parameter will list the required inputs. The repository contains various example input files in each subfolder.

### License

GPLv3 or newer.
