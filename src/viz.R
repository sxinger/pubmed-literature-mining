setwd("C:/repo/pubmed-literature-mining")

pacman::p_load(tidyverse,
               magrittr,
               rjson,
               ggrepel)

dat<-fromJSON(file="./data/als-mnd-risk-factor-ab-proc.json")

yr_lst<-names(dat)
df<-data.frame(yr=as.integer(),
               doc=as.integer(),
               word=as.character(),
               cnt=as.integer(),
               stringsAsFactors = F)

for (yr_str in yr_lst){
  df %<>%
    bind_rows(data.frame(yr=as.numeric(yr_str),
                         doc=dat[[yr_str]][[1]],
                         word=dat[[yr_str]][[2]],
                         cnt=dat[[yr_str]][[3]]))
}

df %<>%
  mutate(rel_cnt = cnt/doc,
         cnt_log10 = log10(cnt),
         gene_ind = case_when(grepl("(gene|c9or|tdp-|smn|atxn2|variant|allel|cell)+",word) ~ 'Genetic',
                              TRUE ~ 'Non-Genetic'))


ggplot(df,aes(x=yr,y=cnt,label=word,color=gene_ind))+
  geom_point()+
  geom_smooth(method = 'loess', formula = 'y ~ x',
              aes(group=gene_ind)) + 
  geom_text_repel(point.padding = 0, 
                  min.segment.length = 0,
                  max.time = 1, max.iter = 1e5, 
                  box.padding = 0.3,
                  max.overlaps = 40,
                  segment.color ="grey",
                  fontface ="bold") +
  labs(x="Publication Year",y="Word Frequency",color="Genetic-Focus")+
  theme(legend.position = c(0.1, 0.85),
        text = element_text(size=15,face="bold"))
