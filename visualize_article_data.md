Article Metadata Summaries
================
Toph Allen
4/9/2019

``` r
terms <- read_lines("terms")

articles <- read_csv(here("data", "articles.csv")) %>%
  select(-X1, -id_types, -keywords)
id_types <- read_csv(here("data", "id_types.csv")) %>%
  select(-X1)
keywords <- read_csv(here("data", "keywords.csv")) %>%
  select(-X1)
text_matches <- read_csv(here("data", "text_matches.csv")) %>%
  select(-X1)
geonames <- read_csv(here("data", "geonames.csv")) %>%
  select(-X1)
```

## Prevalence of Text Matches

We searched for four terms in the extracted text of articles, using
MongoDB’s text search capabilities. We think these terms will select
articles which have a fieldwork component over those that don’t. The
terms used are: field work, fieldwork, field study, field site, field
area, study site, study location, study area, research site, research
location, sampling site, sampling location, sampling area.

Matching articles are a smallish subset of the total, 4.442%.

``` r
ktable(articles$any_matches)
```

<table class="table table-hover table-condensed table-responsive" style="width: auto !important; ">

<thead>

<tr>

<th style="text-align:left;">

Var1

</th>

<th style="text-align:right;">

Freq

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

FALSE

</td>

<td style="text-align:right;">

47779

</td>

</tr>

<tr>

<td style="text-align:left;">

TRUE

</td>

<td style="text-align:right;">

2221

</td>

</tr>

</tbody>

</table>

``` r
ktable(articles$text_matches) %>% scroll_box(height = "400px")
```

<div style="border: 1px solid #ddd; padding: 0px; overflow-y: scroll; height:400px; ">

<table class="table table-hover table-condensed table-responsive" style="width: auto !important; ">

<thead>

<tr>

<th style="text-align:left;position: sticky; top:0; background-color: #FFFFFF;">

Var1

</th>

<th style="text-align:right;position: sticky; top:0; background-color: #FFFFFF;">

Freq

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

\[‘field area’, ‘study area’\]

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field area’, ‘study site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field area’\]

</td>

<td style="text-align:right;">

22

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘sampling site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘sampling site’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study area’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study area’\]

</td>

<td style="text-align:right;">

6

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study location’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study site’, ‘research site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study site’, ‘study area’, ‘sampling site’, ‘sampling
area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

7

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study site’, ‘study location’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study site’, ‘study location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’, ‘study site’\]

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field site’\]

</td>

<td style="text-align:right;">

32

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘field site’, ‘study area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘field site’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

3

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘field site’, ‘study site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘field site’\]

</td>

<td style="text-align:right;">

5

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘sampling site’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study area’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study area’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study area’\]

</td>

<td style="text-align:right;">

9

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study site’, ‘sampling site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study site’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study site’, ‘study area’, ‘sampling site’, ‘sampling
area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study site’, ‘study area’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study site’, ‘study location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’, ‘study site’\]

</td>

<td style="text-align:right;">

7

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field study’\]

</td>

<td style="text-align:right;">

64

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘field site’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘field study’, ‘field site’, ‘study site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘field study’, ‘study area’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘field study’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘fieldwork’, ‘field site’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘fieldwork’, ‘field site’, ‘study site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘fieldwork’, ‘field site’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘fieldwork’, ‘study area’\]

</td>

<td style="text-align:right;">

5

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘fieldwork’, ‘study site’, ‘sampling site’, ‘sampling
location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘fieldwork’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

3

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘fieldwork’, ‘study site’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘fieldwork’\]

</td>

<td style="text-align:right;">

9

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘research site’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘study area’\]

</td>

<td style="text-align:right;">

20

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘study location’, ‘study area’\]

</td>

<td style="text-align:right;">

3

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘study site’, ‘sampling location’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘study site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘study site’, ‘study area’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

11

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘study site’, ‘study location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’, ‘study site’\]

</td>

<td style="text-align:right;">

16

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘field work’\]

</td>

<td style="text-align:right;">

74

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘field site’, ‘research site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘field site’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘field site’, ‘study site’, ‘research location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘field site’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘field study’, ‘study area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘field study’, ‘study site’, ‘study area’, ‘sampling
location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘field study’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘field study’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘research site’\]

</td>

<td style="text-align:right;">

3

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘sampling location’\]

</td>

<td style="text-align:right;">

3

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study area’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study area’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study area’, ‘sampling site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study area’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study area’\]

</td>

<td style="text-align:right;">

22

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study location’, ‘research site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study site’, ‘sampling site’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study site’, ‘study area’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study site’, ‘study area’, ‘sampling site’, ‘sampling
area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

17

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study site’, ‘study location’, ‘study area’, ‘sampling
location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’, ‘study site’\]

</td>

<td style="text-align:right;">

14

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘fieldwork’\]

</td>

<td style="text-align:right;">

126

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘research location’\]

</td>

<td style="text-align:right;">

5

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘research site’, ‘research location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘research site’\]

</td>

<td style="text-align:right;">

36

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘sampling area’\]

</td>

<td style="text-align:right;">

39

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘sampling location’, ‘sampling area’\]

</td>

<td style="text-align:right;">

6

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘sampling location’\]

</td>

<td style="text-align:right;">

61

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘sampling site’, ‘sampling area’\]

</td>

<td style="text-align:right;">

11

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘sampling site’, ‘sampling location’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘sampling site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

32

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘sampling site’\]

</td>

<td style="text-align:right;">

126

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘research site’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘research site’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘research site’\]

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘sampling area’\]

</td>

<td style="text-align:right;">

5

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘sampling location’, ‘sampling area’\]

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘sampling location’\]

</td>

<td style="text-align:right;">

13

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘sampling site’, ‘sampling area’\]

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘sampling site’, ‘sampling location’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘sampling site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

7

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’, ‘sampling site’\]

</td>

<td style="text-align:right;">

28

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study area’\]

</td>

<td style="text-align:right;">

513

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study location’, ‘research site’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study location’, ‘sampling site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study location’, ‘sampling site’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study location’, ‘study area’, ‘sampling site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study location’, ‘study area’\]

</td>

<td style="text-align:right;">

12

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study location’\]

</td>

<td style="text-align:right;">

62

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘research location’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘research location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘research site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘research site’\]

</td>

<td style="text-align:right;">

6

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

6

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘sampling site’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘sampling site’, ‘sampling location’\]

</td>

<td style="text-align:right;">

5

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘sampling site’\]

</td>

<td style="text-align:right;">

18

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study area’, ‘research site’\]

</td>

<td style="text-align:right;">

3

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study area’, ‘sampling area’\]

</td>

<td style="text-align:right;">

6

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study area’, ‘sampling location’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study area’, ‘sampling location’\]

</td>

<td style="text-align:right;">

3

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study area’, ‘sampling site’, ‘sampling area’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study area’, ‘sampling site’, ‘sampling location’,
‘sampling area’\]

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study area’, ‘sampling site’\]

</td>

<td style="text-align:right;">

17

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study area’\]

</td>

<td style="text-align:right;">

120

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study location’, ‘sampling site’, ‘sampling area’\]

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’, ‘study location’\]

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

\[‘study site’\]

</td>

<td style="text-align:right;">

476

</td>

</tr>

</tbody>

</table>

</div>

``` r
text_matches %>%
  filter(!is.na(text_matches)) %>%
  ggplot(aes(x = factor(text_matches))) +
  geom_bar(stat = "count") +
  theme_bw()
```

![](visualize_article_data_files/figure-gfm/text_matches_2-1.png)<!-- -->

## Examining characteristics of the subset

I pulled a few pieces of metadata for our subset of articles. These
include:

  - What type of article is it?
  - Does it have a `<body>` tag?
  - How long is it?
  - Associated keywords
  - What types of document identifiers does it have?

### Article types

There are many article types, but only a few which are widely used.

``` r
articles %<>%
  mutate(article_type = fct_infreq(article_type))
ktable(articles$article_type) %>% scroll_box(height = "400px")
```

<div style="border: 1px solid #ddd; padding: 0px; overflow-y: scroll; height:400px; ">

<table class="table table-hover table-condensed table-responsive" style="width: auto !important; ">

<thead>

<tr>

<th style="text-align:left;position: sticky; top:0; background-color: #FFFFFF;">

Var1

</th>

<th style="text-align:right;position: sticky; top:0; background-color: #FFFFFF;">

Freq

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

research-article

</td>

<td style="text-align:right;">

36358

</td>

</tr>

<tr>

<td style="text-align:left;">

review-article

</td>

<td style="text-align:right;">

3313

</td>

</tr>

<tr>

<td style="text-align:left;">

case-report

</td>

<td style="text-align:right;">

2274

</td>

</tr>

<tr>

<td style="text-align:left;">

other

</td>

<td style="text-align:right;">

1800

</td>

</tr>

<tr>

<td style="text-align:left;">

abstract

</td>

<td style="text-align:right;">

1322

</td>

</tr>

<tr>

<td style="text-align:left;">

brief-report

</td>

<td style="text-align:right;">

801

</td>

</tr>

<tr>

<td style="text-align:left;">

editorial

</td>

<td style="text-align:right;">

785

</td>

</tr>

<tr>

<td style="text-align:left;">

book-review

</td>

<td style="text-align:right;">

772

</td>

</tr>

<tr>

<td style="text-align:left;">

letter

</td>

<td style="text-align:right;">

759

</td>

</tr>

<tr>

<td style="text-align:left;">

correction

</td>

<td style="text-align:right;">

626

</td>

</tr>

<tr>

<td style="text-align:left;">

news

</td>

<td style="text-align:right;">

224

</td>

</tr>

<tr>

<td style="text-align:left;">

article-commentary

</td>

<td style="text-align:right;">

201

</td>

</tr>

<tr>

<td style="text-align:left;">

meeting-report

</td>

<td style="text-align:right;">

163

</td>

</tr>

<tr>

<td style="text-align:left;">

discussion

</td>

<td style="text-align:right;">

95

</td>

</tr>

<tr>

<td style="text-align:left;">

protocol

</td>

<td style="text-align:right;">

85

</td>

</tr>

<tr>

<td style="text-align:left;">

obituary

</td>

<td style="text-align:right;">

83

</td>

</tr>

<tr>

<td style="text-align:left;">

product-review

</td>

<td style="text-align:right;">

56

</td>

</tr>

<tr>

<td style="text-align:left;">

rapid-communication

</td>

<td style="text-align:right;">

45

</td>

</tr>

<tr>

<td style="text-align:left;">

in-brief

</td>

<td style="text-align:right;">

39

</td>

</tr>

<tr>

<td style="text-align:left;">

methods-article

</td>

<td style="text-align:right;">

33

</td>

</tr>

<tr>

<td style="text-align:left;">

reply

</td>

<td style="text-align:right;">

33

</td>

</tr>

<tr>

<td style="text-align:left;">

retraction

</td>

<td style="text-align:right;">

28

</td>

</tr>

<tr>

<td style="text-align:left;">

systematic-review

</td>

<td style="text-align:right;">

25

</td>

</tr>

<tr>

<td style="text-align:left;">

data-paper

</td>

<td style="text-align:right;">

22

</td>

</tr>

<tr>

<td style="text-align:left;">

introduction

</td>

<td style="text-align:right;">

21

</td>

</tr>

<tr>

<td style="text-align:left;">

report

</td>

<td style="text-align:right;">

10

</td>

</tr>

<tr>

<td style="text-align:left;">

announcement

</td>

<td style="text-align:right;">

7

</td>

</tr>

<tr>

<td style="text-align:left;">

addendum

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

books-received

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

calendar

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

oration

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

expression-of-concern

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

index

</td>

<td style="text-align:right;">

2

</td>

</tr>

</tbody>

</table>

</div>

``` r
articles %>% 
  group_by(article_type) %>%
  mutate(n = n()) %>%
  filter(n > 50) %>%
  ungroup() %>%
  ggplot(aes(x = factor(article_type))) +
  geom_bar() +
  theme_bw() + theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

![](visualize_article_data_files/figure-gfm/article_types_2-1.png)<!-- -->

Does the usage of these differ between the fieldwork subset?

``` r
articles %>% 
  group_by(any_matches) %>%
  mutate(n_matches = n()) %>%
  group_by(any_matches, article_type) %>%
  summarize(type_freq = (n() / n_matches)[1]) %>%
  ungroup() %>%
  group_by(article_type) %>%
  filter(n() > 1) %>%
  ungroup() %>%
  ggplot(aes(x = factor(article_type), y = type_freq, fill = any_matches)) +
  geom_col(position = "dodge") +
  theme_bw() + theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

![](visualize_article_data_files/figure-gfm/article_types_3-1.png)<!-- -->

There are more research articles, and fewer of everything else.

### Presence of `<body>` tag

``` r
ktable(articles$has_body)
```

<table class="table table-hover table-condensed table-responsive" style="width: auto !important; ">

<thead>

<tr>

<th style="text-align:left;">

Var1

</th>

<th style="text-align:right;">

Freq

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

FALSE

</td>

<td style="text-align:right;">

4519

</td>

</tr>

<tr>

<td style="text-align:left;">

TRUE

</td>

<td style="text-align:right;">

45481

</td>

</tr>

</tbody>

</table>

``` r
ktable(articles$article_type, articles$has_body) %>% scroll_box(height = "400px")
```

<div style="border: 1px solid #ddd; padding: 0px; overflow-y: scroll; height:400px; ">

<table class="table table-hover table-condensed table-responsive" style="width: auto !important; ">

<thead>

<tr>

<th style="text-align:left;position: sticky; top:0; background-color: #FFFFFF;">

</th>

<th style="text-align:right;position: sticky; top:0; background-color: #FFFFFF;">

FALSE

</th>

<th style="text-align:right;position: sticky; top:0; background-color: #FFFFFF;">

TRUE

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

research-article

</td>

<td style="text-align:right;">

2056

</td>

<td style="text-align:right;">

34302

</td>

</tr>

<tr>

<td style="text-align:left;">

review-article

</td>

<td style="text-align:right;">

115

</td>

<td style="text-align:right;">

3198

</td>

</tr>

<tr>

<td style="text-align:left;">

case-report

</td>

<td style="text-align:right;">

13

</td>

<td style="text-align:right;">

2261

</td>

</tr>

<tr>

<td style="text-align:left;">

other

</td>

<td style="text-align:right;">

1021

</td>

<td style="text-align:right;">

779

</td>

</tr>

<tr>

<td style="text-align:left;">

abstract

</td>

<td style="text-align:right;">

270

</td>

<td style="text-align:right;">

1052

</td>

</tr>

<tr>

<td style="text-align:left;">

brief-report

</td>

<td style="text-align:right;">

17

</td>

<td style="text-align:right;">

784

</td>

</tr>

<tr>

<td style="text-align:left;">

editorial

</td>

<td style="text-align:right;">

79

</td>

<td style="text-align:right;">

706

</td>

</tr>

<tr>

<td style="text-align:left;">

book-review

</td>

<td style="text-align:right;">

500

</td>

<td style="text-align:right;">

272

</td>

</tr>

<tr>

<td style="text-align:left;">

letter

</td>

<td style="text-align:right;">

137

</td>

<td style="text-align:right;">

622

</td>

</tr>

<tr>

<td style="text-align:left;">

correction

</td>

<td style="text-align:right;">

25

</td>

<td style="text-align:right;">

601

</td>

</tr>

<tr>

<td style="text-align:left;">

news

</td>

<td style="text-align:right;">

93

</td>

<td style="text-align:right;">

131

</td>

</tr>

<tr>

<td style="text-align:left;">

article-commentary

</td>

<td style="text-align:right;">

3

</td>

<td style="text-align:right;">

198

</td>

</tr>

<tr>

<td style="text-align:left;">

meeting-report

</td>

<td style="text-align:right;">

98

</td>

<td style="text-align:right;">

65

</td>

</tr>

<tr>

<td style="text-align:left;">

discussion

</td>

<td style="text-align:right;">

2

</td>

<td style="text-align:right;">

93

</td>

</tr>

<tr>

<td style="text-align:left;">

protocol

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

85

</td>

</tr>

<tr>

<td style="text-align:left;">

obituary

</td>

<td style="text-align:right;">

72

</td>

<td style="text-align:right;">

11

</td>

</tr>

<tr>

<td style="text-align:left;">

product-review

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

56

</td>

</tr>

<tr>

<td style="text-align:left;">

rapid-communication

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

45

</td>

</tr>

<tr>

<td style="text-align:left;">

in-brief

</td>

<td style="text-align:right;">

1

</td>

<td style="text-align:right;">

38

</td>

</tr>

<tr>

<td style="text-align:left;">

methods-article

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

33

</td>

</tr>

<tr>

<td style="text-align:left;">

reply

</td>

<td style="text-align:right;">

7

</td>

<td style="text-align:right;">

26

</td>

</tr>

<tr>

<td style="text-align:left;">

retraction

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

28

</td>

</tr>

<tr>

<td style="text-align:left;">

systematic-review

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

25

</td>

</tr>

<tr>

<td style="text-align:left;">

data-paper

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

22

</td>

</tr>

<tr>

<td style="text-align:left;">

introduction

</td>

<td style="text-align:right;">

2

</td>

<td style="text-align:right;">

19

</td>

</tr>

<tr>

<td style="text-align:left;">

report

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

10

</td>

</tr>

<tr>

<td style="text-align:left;">

announcement

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

7

</td>

</tr>

<tr>

<td style="text-align:left;">

addendum

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

books-received

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

4

</td>

</tr>

<tr>

<td style="text-align:left;">

calendar

</td>

<td style="text-align:right;">

3

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

oration

</td>

<td style="text-align:right;">

3

</td>

<td style="text-align:right;">

1

</td>

</tr>

<tr>

<td style="text-align:left;">

expression-of-concern

</td>

<td style="text-align:right;">

0

</td>

<td style="text-align:right;">

2

</td>

</tr>

<tr>

<td style="text-align:left;">

index

</td>

<td style="text-align:right;">

2

</td>

<td style="text-align:right;">

0

</td>

</tr>

</tbody>

</table>

</div>

### Length

``` r
types <- articles %>%
  group_by(any_matches) %>%
  mutate(match_n = n()) %>%
  group_by(article_type) %>%
  mutate(type_n = n()) %>%
  group_by(any_matches, article_type) %>%
  summarize(match_x_type = n(),
            match_n = match_n[1],
            type_n = type_n[1]) %>%
  ungroup() %>%
  mutate(x_over_match = match_x_type / match_n,
         x_over_type = match_x_type / type_n)

type_filter <- types %>%
  filter(x_over_match > 0.005) %>%
  group_by(article_type) %>%
  filter(n() > 1) %>%
  pull(article_type) %>%
  unique()
```

``` r
ggplot(articles, aes(x = text_length)) +
  geom_density() +
  scale_x_log10(labels = comma) +
  theme_bw()
```

![](visualize_article_data_files/figure-gfm/length_2-1.png)<!-- -->

``` r
ggplot(articles, aes(x = text_length, fill = any_matches)) +
  geom_density(alpha = 0.5) +
  scale_x_log10(labels = comma) +
  theme_bw()
```

![](visualize_article_data_files/figure-gfm/length_2-2.png)<!-- -->

``` r
articles %>%
  group_by(article_type) %>%
  filter(n() > 100) %>%
  ggplot(aes(x = text_length, fill = article_type)) +
  geom_density(alpha = 0.25) +
  scale_x_log10(labels = comma) +
  theme_bw()
```

![](visualize_article_data_files/figure-gfm/length_2-3.png)<!-- -->

``` r
articles %>%
  filter(article_type %in% type_filter) %>%
  ggplot(aes(x = text_length, fill = article_type)) +
  geom_density() +
  scale_x_log10(labels = comma) +
  facet_grid(article_type ~ any_matches) +
  theme_bw()
```

![](visualize_article_data_files/figure-gfm/length_2-4.png)<!-- -->

### Usage of Keywords

``` r
keywords_per_paper <- keywords %>%
  group_by(id) %>%
  summarize(any_matches = unique(any_matches),
            n = n())
```

A total of 25549 papers out of 50000 (51.098%) had keywords.

For those matching fieldwork terms:

``` r
k <- keywords_per_paper %>%
  filter(any_matches == TRUE) %>%
  nrow()
nk <- articles %>%
  filter(any_matches == TRUE) %>%
  nrow()

k / nk * 100
```

    ## [1] 57.6317

For those not matching fieldwork terms:

``` r
k <- keywords_per_paper %>%
  filter(any_matches == FALSE) %>%
  nrow()
nk <- articles %>%
  filter(any_matches == FALSE) %>%
  nrow()

k / nk * 100
```

    ## [1] 50.79428

These are the top twenty-five keywords used in all documents:

``` r
keyword_summary <- keywords %>%
  group_by(keywords) %>%
  summarize(n = n()) %>%
  arrange(-n) %>%
  head(25)

knitr::kable(keyword_summary) %>%
  kable_styling(bootstrap_options = c("hover", "condensed", "responsive"),
                full_width = FALSE,
                position = "left") %>%
  scroll_box(height = "400px")
```

<div style="border: 1px solid #ddd; padding: 0px; overflow-y: scroll; height:400px; ">

<table class="table table-hover table-condensed table-responsive" style="width: auto !important; ">

<thead>

<tr>

<th style="text-align:left;position: sticky; top:0; background-color: #FFFFFF;">

keywords

</th>

<th style="text-align:right;position: sticky; top:0; background-color: #FFFFFF;">

n

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

inflammation

</td>

<td style="text-align:right;">

174

</td>

</tr>

<tr>

<td style="text-align:left;">

breast cancer

</td>

<td style="text-align:right;">

173

</td>

</tr>

<tr>

<td style="text-align:left;">

apoptosis

</td>

<td style="text-align:right;">

171

</td>

</tr>

<tr>

<td style="text-align:left;">

cancer

</td>

<td style="text-align:right;">

163

</td>

</tr>

<tr>

<td style="text-align:left;">

HIV

</td>

<td style="text-align:right;">

163

</td>

</tr>

<tr>

<td style="text-align:left;">

prognosis

</td>

<td style="text-align:right;">

138

</td>

</tr>

<tr>

<td style="text-align:left;">

Breast cancer

</td>

<td style="text-align:right;">

121

</td>

</tr>

<tr>

<td style="text-align:left;">

Epidemiology

</td>

<td style="text-align:right;">

118

</td>

</tr>

<tr>

<td style="text-align:left;">

obesity

</td>

<td style="text-align:right;">

113

</td>

</tr>

<tr>

<td style="text-align:left;">

Obesity

</td>

<td style="text-align:right;">

111

</td>

</tr>

<tr>

<td style="text-align:left;">

meta-analysis

</td>

<td style="text-align:right;">

106

</td>

</tr>

<tr>

<td style="text-align:left;">

oxidative stress

</td>

<td style="text-align:right;">

106

</td>

</tr>

<tr>

<td style="text-align:left;">

children

</td>

<td style="text-align:right;">

105

</td>

</tr>

<tr>

<td style="text-align:left;">

Inflammation

</td>

<td style="text-align:right;">

104

</td>

</tr>

<tr>

<td style="text-align:left;">

epidemiology

</td>

<td style="text-align:right;">

102

</td>

</tr>

<tr>

<td style="text-align:left;">

colorectal cancer

</td>

<td style="text-align:right;">

93

</td>

</tr>

<tr>

<td style="text-align:left;">

depression

</td>

<td style="text-align:right;">

91

</td>

</tr>

<tr>

<td style="text-align:left;">

Children

</td>

<td style="text-align:right;">

88

</td>

</tr>

<tr>

<td style="text-align:left;">

aging

</td>

<td style="text-align:right;">

87

</td>

</tr>

<tr>

<td style="text-align:left;">

Apoptosis

</td>

<td style="text-align:right;">

87

</td>

</tr>

<tr>

<td style="text-align:left;">

microRNA

</td>

<td style="text-align:right;">

86

</td>

</tr>

<tr>

<td style="text-align:left;">

Iran

</td>

<td style="text-align:right;">

85

</td>

</tr>

<tr>

<td style="text-align:left;">

Alzheimer’s disease

</td>

<td style="text-align:right;">

84

</td>

</tr>

<tr>

<td style="text-align:left;">

Prognosis

</td>

<td style="text-align:right;">

83

</td>

</tr>

<tr>

<td style="text-align:left;">

metastasis

</td>

<td style="text-align:right;">

80

</td>

</tr>

</tbody>

</table>

</div>

For those matching fieldwork terms:

``` r
fw_keyword_summary <- keywords %>%
  filter(any_matches == TRUE) %>%
  group_by(keywords) %>%
  summarize(n = n()) %>%
  arrange(-n) %>%
  head(25)

knitr::kable(fw_keyword_summary) %>%
  kable_styling(bootstrap_options = c("hover", "condensed", "responsive"),
                full_width = FALSE,
                position = "left") %>%
  scroll_box(height = "400px")
```

<div style="border: 1px solid #ddd; padding: 0px; overflow-y: scroll; height:400px; ">

<table class="table table-hover table-condensed table-responsive" style="width: auto !important; ">

<thead>

<tr>

<th style="text-align:left;position: sticky; top:0; background-color: #FFFFFF;">

keywords

</th>

<th style="text-align:right;position: sticky; top:0; background-color: #FFFFFF;">

n

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

Malaria

</td>

<td style="text-align:right;">

30

</td>

</tr>

<tr>

<td style="text-align:left;">

HIV

</td>

<td style="text-align:right;">

20

</td>

</tr>

<tr>

<td style="text-align:left;">

epidemiology

</td>

<td style="text-align:right;">

19

</td>

</tr>

<tr>

<td style="text-align:left;">

Ethiopia

</td>

<td style="text-align:right;">

18

</td>

</tr>

<tr>

<td style="text-align:left;">

Epidemiology

</td>

<td style="text-align:right;">

16

</td>

</tr>

<tr>

<td style="text-align:left;">

Plasmodium falciparum

</td>

<td style="text-align:right;">

15

</td>

</tr>

<tr>

<td style="text-align:left;">

India

</td>

<td style="text-align:right;">

13

</td>

</tr>

<tr>

<td style="text-align:left;">

Africa

</td>

<td style="text-align:right;">

12

</td>

</tr>

<tr>

<td style="text-align:left;">

malaria

</td>

<td style="text-align:right;">

12

</td>

</tr>

<tr>

<td style="text-align:left;">

Prevalence

</td>

<td style="text-align:right;">

12

</td>

</tr>

<tr>

<td style="text-align:left;">

South Africa

</td>

<td style="text-align:right;">

12

</td>

</tr>

<tr>

<td style="text-align:left;">

Tuberculosis

</td>

<td style="text-align:right;">

11

</td>

</tr>

<tr>

<td style="text-align:left;">

children

</td>

<td style="text-align:right;">

10

</td>

</tr>

<tr>

<td style="text-align:left;">

Tanzania

</td>

<td style="text-align:right;">

10

</td>

</tr>

<tr>

<td style="text-align:left;">

Brazil

</td>

<td style="text-align:right;">

9

</td>

</tr>

<tr>

<td style="text-align:left;">

Iran

</td>

<td style="text-align:right;">

9

</td>

</tr>

<tr>

<td style="text-align:left;">

Adolescents

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

GIS

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

influenza

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

Mental health

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

Physical activity

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

Plasmodium vivax

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

Risk factors

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

viruses

</td>

<td style="text-align:right;">

8

</td>

</tr>

<tr>

<td style="text-align:left;">

Children

</td>

<td style="text-align:right;">

7

</td>

</tr>

</tbody>

</table>

</div>

And those with no matches for fieldwork terms:

``` r
nofw_keyword_summary <- keywords %>%
  filter(any_matches == FALSE) %>%
  group_by(keywords) %>%
  summarize(n = n()) %>%
  arrange(-n) %>%
  head(25)

knitr::kable(nofw_keyword_summary) %>%
  kable_styling(bootstrap_options = c("hover", "condensed", "responsive"),
                full_width = FALSE,
                position = "left") %>%
  scroll_box(height = "400px")
```

<div style="border: 1px solid #ddd; padding: 0px; overflow-y: scroll; height:400px; ">

<table class="table table-hover table-condensed table-responsive" style="width: auto !important; ">

<thead>

<tr>

<th style="text-align:left;position: sticky; top:0; background-color: #FFFFFF;">

keywords

</th>

<th style="text-align:right;position: sticky; top:0; background-color: #FFFFFF;">

n

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

inflammation

</td>

<td style="text-align:right;">

174

</td>

</tr>

<tr>

<td style="text-align:left;">

apoptosis

</td>

<td style="text-align:right;">

171

</td>

</tr>

<tr>

<td style="text-align:left;">

breast cancer

</td>

<td style="text-align:right;">

170

</td>

</tr>

<tr>

<td style="text-align:left;">

cancer

</td>

<td style="text-align:right;">

161

</td>

</tr>

<tr>

<td style="text-align:left;">

HIV

</td>

<td style="text-align:right;">

143

</td>

</tr>

<tr>

<td style="text-align:left;">

prognosis

</td>

<td style="text-align:right;">

137

</td>

</tr>

<tr>

<td style="text-align:left;">

Breast cancer

</td>

<td style="text-align:right;">

119

</td>

</tr>

<tr>

<td style="text-align:left;">

obesity

</td>

<td style="text-align:right;">

107

</td>

</tr>

<tr>

<td style="text-align:left;">

oxidative stress

</td>

<td style="text-align:right;">

105

</td>

</tr>

<tr>

<td style="text-align:left;">

Obesity

</td>

<td style="text-align:right;">

104

</td>

</tr>

<tr>

<td style="text-align:left;">

Inflammation

</td>

<td style="text-align:right;">

103

</td>

</tr>

<tr>

<td style="text-align:left;">

meta-analysis

</td>

<td style="text-align:right;">

103

</td>

</tr>

<tr>

<td style="text-align:left;">

Epidemiology

</td>

<td style="text-align:right;">

102

</td>

</tr>

<tr>

<td style="text-align:left;">

children

</td>

<td style="text-align:right;">

95

</td>

</tr>

<tr>

<td style="text-align:left;">

colorectal cancer

</td>

<td style="text-align:right;">

93

</td>

</tr>

<tr>

<td style="text-align:left;">

depression

</td>

<td style="text-align:right;">

88

</td>

</tr>

<tr>

<td style="text-align:left;">

Apoptosis

</td>

<td style="text-align:right;">

87

</td>

</tr>

<tr>

<td style="text-align:left;">

aging

</td>

<td style="text-align:right;">

86

</td>

</tr>

<tr>

<td style="text-align:left;">

microRNA

</td>

<td style="text-align:right;">

86

</td>

</tr>

<tr>

<td style="text-align:left;">

epidemiology

</td>

<td style="text-align:right;">

83

</td>

</tr>

<tr>

<td style="text-align:left;">

Alzheimer’s disease

</td>

<td style="text-align:right;">

81

</td>

</tr>

<tr>

<td style="text-align:left;">

Children

</td>

<td style="text-align:right;">

81

</td>

</tr>

<tr>

<td style="text-align:left;">

Prognosis

</td>

<td style="text-align:right;">

81

</td>

</tr>

<tr>

<td style="text-align:left;">

metastasis

</td>

<td style="text-align:right;">

80

</td>

</tr>

<tr>

<td style="text-align:left;">

Cancer

</td>

<td style="text-align:right;">

76

</td>

</tr>

</tbody>

</table>

</div>

And per fieldwork term:

``` r
kwd_x_match <- keywords %>%
  left_join(select(articles, id, text_matches), by = "id") %>%
  mutate(text_matches = replace_na(text_matches, ""))

for (term in terms) {
  print(paste("Term: ", term))
  kwd_x_match %>%
    filter(map_lgl(kwd_x_match$text_matches, ~str_detect(.x, fixed(term)))) %>%
    group_by(keywords) %>%
    summarize(n = n()) %>%
    arrange(desc(n)) %>%
    print()
    print("\n")
}
```

    ## [1] "Term:  field work"
    ## # A tibble: 481 x 2
    ##    keywords            n
    ##    <chr>           <int>
    ##  1 India               4
    ##  2 Malaria             3
    ##  3 epidemiology        2
    ##  4 Ghana               2
    ##  5 HIV/AIDS            2
    ##  6 Kenya               2
    ##  7 Loop migration      2
    ##  8 malaria             2
    ##  9 Mayotte             2
    ## 10 microsatellites     2
    ## # … with 471 more rows
    ## [1] "\n"
    ## [1] "Term:  fieldwork"
    ## # A tibble: 762 x 2
    ##    keywords           n
    ##    <chr>          <int>
    ##  1 South Africa       6
    ##  2 HIV                5
    ##  3 Africa             3
    ##  4 hypertension       3
    ##  5 Malawi             3
    ##  6 obesity            3
    ##  7 Brazil             2
    ##  8 children           2
    ##  9 climate change     2
    ## 10 dispersal          2
    ## # … with 752 more rows
    ## [1] "\n"
    ## [1] "Term:  field study"
    ## # A tibble: 356 x 2
    ##    keywords              n
    ##    <chr>             <int>
    ##  1 Epidemiology          3
    ##  2 Malaria               3
    ##  3 Chiroptera            2
    ##  4 Drug resistance       2
    ##  5 Europe                2
    ##  6 health                2
    ##  7 Mosquito              2
    ##  8 seed treatment        2
    ##  9 West Nile virus       2
    ## 10 “quiet” courtyard     1
    ## # … with 346 more rows
    ## [1] "\n"
    ## [1] "Term:  field site"
    ## # A tibble: 250 x 2
    ##    keywords                     n
    ##    <chr>                    <int>
    ##  1 Malaria                      3
    ##  2 Malawi                       2
    ##  3 "\nAnthophila\n"             1
    ##  4 "\nApoidea\n"                1
    ##  5 Acacia longifolia            1
    ##  6 Acoustic communication       1
    ##  7 Acoustic tracking            1
    ##  8 adaptive landscape           1
    ##  9 Aerial photography           1
    ## 10 agricultural abandonment     1
    ## # … with 240 more rows
    ## [1] "\n"
    ## [1] "Term:  field area"
    ## # A tibble: 57 x 2
    ##    keywords           n
    ##    <chr>          <int>
    ##  1 Antioxidants       1
    ##  2 Archaea            1
    ##  3 asymmetry          1
    ##  4 Axis selective     1
    ##  5 axon               1
    ##  6 breast cancer      1
    ##  7 breast dose        1
    ##  8 C5aR1              1
    ##  9 Cancer             1
    ## 10 cancer therapy     1
    ## # … with 47 more rows
    ## [1] "\n"
    ## [1] "Term:  study site"
    ## # A tibble: 2,244 x 2
    ##    keywords                   n
    ##    <chr>                  <int>
    ##  1 HIV                       16
    ##  2 Malaria                   14
    ##  3 Plasmodium falciparum      9
    ##  4 Tuberculosis               7
    ##  5 epidemiology               6
    ##  6 Ethiopia                   5
    ##  7 South Africa               5
    ##  8 Adolescents                4
    ##  9 antiretroviral therapy     4
    ## 10 Europe                     4
    ## # … with 2,234 more rows
    ## [1] "\n"
    ## [1] "Term:  study location"
    ## # A tibble: 327 x 2
    ##    keywords                       n
    ##    <chr>                      <int>
    ##  1 Activities of daily living     2
    ##  2 Disability                     2
    ##  3 Epidemiology                   2
    ##  4 Malaria                        2
    ##  5 Malaysia                       2
    ##  6 meta-analysis                  2
    ##  7 Meta-analysis                  2
    ##  8 Obesity                        2
    ##  9 Physical activity              2
    ## 10 Prevalence                     2
    ## # … with 317 more rows
    ## [1] "\n"
    ## [1] "Term:  study area"
    ## # A tibble: 2,364 x 2
    ##    keywords                  n
    ##    <chr>                 <int>
    ##  1 Ethiopia                 18
    ##  2 Malaria                  17
    ##  3 Epidemiology             10
    ##  4 epidemiology              9
    ##  5 malaria                   9
    ##  6 Iran                      7
    ##  7 Prevalence                7
    ##  8 GIS                       6
    ##  9 India                     6
    ## 10 Plasmodium falciparum     6
    ## # … with 2,354 more rows
    ## [1] "\n"
    ## [1] "Term:  research site"
    ## # A tibble: 208 x 2
    ##    keywords                      n
    ##    <chr>                     <int>
    ##  1 expectations                  2
    ##  2 Mental health                 2
    ##  3 Pilot study                   2
    ##  4 qualitative research          2
    ##  5 accelerated EPI               1
    ##  6 Adolescent girls              1
    ##  7 Africa                        1
    ##  8 African American              1
    ##  9 agrobiodiversity              1
    ## 10 AHA Scientific Statements     1
    ## # … with 198 more rows
    ## [1] "\n"
    ## [1] "Term:  research location"
    ## # A tibble: 38 x 2
    ##    keywords                 n
    ##    <chr>                <int>
    ##  1 indoor air pollution     2
    ##  2 particulate matter       2
    ##  3 PM2.5                    2
    ##  4 Aged                     1
    ##  5 Aged, 80 and Over        1
    ##  6 Androgenic alopecia      1
    ##  7 biomass fuels            1
    ##  8 Caregivers               1
    ##  9 Case study               1
    ## 10 casino                   1
    ## # … with 28 more rows
    ## [1] "\n"
    ## [1] "Term:  sampling site"
    ## # A tibble: 843 x 2
    ##    keywords                             n
    ##    <chr>                            <int>
    ##  1 Genetic diversity                    4
    ##  2 16S rRNA gene                        3
    ##  3 bacteria                             3
    ##  4 Biodiversity                         3
    ##  5 Genetic structure                    3
    ##  6 16S rRNA                             2
    ##  7 Adaptive radiation                   2
    ##  8 Allergy                              2
    ##  9 Ammonia-oxidizing archaea (AOA)      2
    ## 10 Ammonia-oxidizing bacteria (AOB)     2
    ## # … with 833 more rows
    ## [1] "\n"
    ## [1] "Term:  sampling location"
    ## # A tibble: 509 x 2
    ##    keywords                      n
    ##    <chr>                     <int>
    ##  1 16S rRNA gene                 3
    ##  2 adaptation                    2
    ##  3 Air                           2
    ##  4 Antarctica                    2
    ##  5 Brazil                        2
    ##  6 Crustacea                     2
    ##  7 Effective population size     2
    ##  8 environmental assessment      2
    ##  9 Genetic diversity             2
    ## 10 particulate matter            2
    ## # … with 499 more rows
    ## [1] "\n"
    ## [1] "Term:  sampling area"
    ## # A tibble: 302 x 2
    ##    keywords                      n
    ##    <chr>                     <int>
    ##  1 bacteria                      2
    ##  2 16S rRNA metagenome           1
    ##  3 A. incertus                   1
    ##  4 abundance                     1
    ##  5 Acanthuridae                  1
    ##  6 Adolescent                    1
    ##  7 adult Anura                   1
    ##  8 African buffaloes             1
    ##  9 agricultural activity         1
    ## 10 Al2O3–ZrO2 nanocomposites     1
    ## # … with 292 more rows
    ## [1] "\n"

## GeoNames

It looks like articles that match the fieldwork terms have many more
geonames in them than those that don’t.

``` r
summary(geonames)
```

    ##     n_spans       n_spans_over90   text_matches       any_matches    
    ##  Min.   :  0.00   Min.   :  0.00   Length:600         Mode :logical  
    ##  1st Qu.:  4.00   1st Qu.:  1.00   Class :character   FALSE:300      
    ##  Median : 12.00   Median :  3.00   Mode  :character   TRUE :300      
    ##  Mean   : 24.91   Mean   :  9.37                                     
    ##  3rd Qu.: 29.00   3rd Qu.: 11.00                                     
    ##  Max.   :647.00   Max.   :211.00

``` r
geonames %>% filter(any_matches == TRUE) %>% summary
```

    ##     n_spans       n_spans_over90   text_matches       any_matches   
    ##  Min.   :  0.00   Min.   :  0.00   Length:300         Mode:logical  
    ##  1st Qu.: 10.00   1st Qu.:  2.00   Class :character   TRUE:300      
    ##  Median : 22.00   Median :  6.00   Mode  :character                 
    ##  Mean   : 37.94   Mean   : 13.66                                    
    ##  3rd Qu.: 38.00   3rd Qu.: 16.00                                    
    ##  Max.   :647.00   Max.   :188.00

``` r
geonames %>% filter(any_matches == FALSE) %>% summary
```

    ##     n_spans       n_spans_over90   text_matches       any_matches    
    ##  Min.   :  0.00   Min.   :  0.00   Length:300         Mode :logical  
    ##  1st Qu.:  1.00   1st Qu.:  0.00   Class :character   FALSE:300      
    ##  Median :  6.00   Median :  1.00   Mode  :character                  
    ##  Mean   : 11.89   Mean   :  5.08                                     
    ##  3rd Qu.: 14.00   3rd Qu.:  5.00                                     
    ##  Max.   :240.00   Max.   :211.00

## Summary

We should use documents which

  - match this set of search terms;
  - have a `<body>` tag;
  - are a `"research-article"`.

We could also consider including `"review-article"` and `"brief-report"`
types, but those seem fairly uncommon.
