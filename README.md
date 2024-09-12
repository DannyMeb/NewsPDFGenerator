# NewsPDFGenerator

## Project Goal

The goal of NewsPDFGenerator is to facilitate developers in collecting news articles to create a knowledge graph. This project fetches the latest news articles from various sources, saves them as PDF files categorized by topic, and merges the PDFs by category. It utilizes the News API to gather articles and generates PDF documents with the article content.

![Application](images\RAG.png)

## Directory Structure

- **Examples/**: Contains example PDFs showcasing the generated results.
- **source/**: Contains `fetch_and_save.py` and `merge.py` scripts.
- **setup.py**: Script to check for and install required dependencies.
- **run_experiment.sh**: Bash script to run `fetch_and_save.py` and `merge.py` sequentially.
- **README.md**: Project documentation.

## Prerequisites

- Python 3.x
- News API key (obtain one from [News API](https://newsapi.org/))

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/DannyMeb/NewsPDFGenerator.git

3. **Set up your environment and intall dependencies:**
   ./setup.py

3. **Run Experiment:**
   cd NewsPDFGenerator
   ./run_experiment.sh

 **Alternatively, Run Scripts Manually**
    python3 source/fetch_and_save.py
    python3 source/merge.py

