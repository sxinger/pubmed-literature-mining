setwd("C:/repo/pubmed-literature-mining")

pacman::p_load(tidyverse,
               magrittr,
               rjson)

dat<-fromJSON(file="./data/als-mnd-risk-factor-ab-proc.json")
