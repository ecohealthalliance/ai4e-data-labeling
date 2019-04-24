python import_pmc.py --pmc_path "/Volumes/Transcend/datasets/pmc/2019-04-03/oa_bulk/" -n 100000 -s "2019-04-05" --drop &&\
python extract_article_metadata.py &&\
python index_search_terms.py &&\
python count_geonames.py --num_workers 4 &&\
python dump_articles.py

# Optionally
python export_csvs.py &&\
python export_subset_csv.py &&\
python count_geonames_to_csvs.py
