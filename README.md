# AI for Earth Data Labeling

Creating a subset of the PMC OAS for the AI for Earth Data Labeling grant.

## Setup

This repo requires a few things:

- Python. You can install the requirements from `requirements.txt`. Broadly, though, the top-level requirements are: `pymongo`, `pandas`, `jupyter`, and EcoHealth Alliance's packages `EpiTator` and `PubCrawler`.
- R, if you want to update the article data RMarkdown document. A clean install with `tidyverse` should be all you need.
- A copy of the PubMed Central Open Access Subset in a directory, unzipped. You can download that from the [PMC OAS FTP server](ftp.ncbi.nlm.nih.gov/pub/pmc).
- An instance of MongoDB. The defaults assume that it's running locally, but you could pass options to address a remote server.

## Usage

There's a core series of Python scripts which should be run in a specific order. Here's what they do:

### 1. `import_pmc.py`

Imports `-n` articles from the specified `--pmc_path` to a MongoDB collection named `articles` in a database named `pmc`.

The collection uses the PMC ID as the `"_id"` field in MongoDB. This field needs to be unique, so if you're re-importing, you'll need to pass in the `--drop` or `-d` flag so that the collection is dropped, or you'll likely get an error. 

You can pass in a random seed with `-s "seed"` or `--seed "seed"`.

We've been using the seed `"2019-04-05"` for our most recent sample, sampling 50000 documents.

### 2. `extract_article_metadata.py`

Iterates over the `articles` collection, setting the following properties for each document:

- `article_title` and `journal_title`
- An `article_meta` subdocument, with a flag `has_body` indicating the presence of the `<body>` tag, and `article_type`.

The script creates an index on the `article_meta` field.

### 3. `index_search_terms.py`

This script searches the `extracted_text` of each article for a set of terms, and writes a `text_matches` array to the MongoDB document with the results of this session's searches.

The terms are read from a text file in the root of the project named `terms`, which has one phrase on each line.

The latter behavior is to allow searches which MongoDB's built-in text search engine doesn't (specifically, we want to be able to search for a logical `OR` on multi-word phrases).

If you want to *add*, rather than *replace*, the `text_matches` array, pass in `--keep_previous`.

### 4. `count_geonames.py`

This script goes through all the documents matching search terms and counts the number of `geospan` objects created by EpiTator's `GeonameAnnotator()`.

It runs in parallel, with a number of threads set by `--num_workers`.

If you run it without passing `--keep_previous`, it'll drop its previous efforts.

### 5. `dump_articles.py`

Dumps a subset of articles into a MongoDump file named `ai4e_articles.gzip`.

The subset includes articles with all of the following:

- `text_matches` for any of the terms
- a `<body>` tag
- `article_type` research-article
- `article_meta.n_geospans` is between the 1st and 99th percentile
- text length is between the 1st and 95th percentiles
- `article_meta.geospan_density` (n_geospans / length) is not more than one standard deviation below the mean (when log-transformed).

### 6. `export_csvs.py`, `count_geonames_to_csvs.py`

These files export CSVs to the `data/` directory for use by `visualize_article_data.Rmd`.

The former iterates through all documents and exports a few different summaries, and the latter samples `-n` articles with and without `text_matches` to run our GeoName annotator (from `EpiTator`) and count the number of GeoNames found for each article.

### 7. `visualize_article_data.Rmd`

Build this with `rmarkdown::render()` in R, and it'll update the Markdown and HTML reports with summary statistics.
