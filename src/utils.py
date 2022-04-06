def word_dist_over_year(fw:list,kw:list,yr_key:list,w:int,top_k:int):
    yr_words = dict.fromkeys(yr_key,[])
    yr_docs = dict.fromkeys(yr_key,0)  
    for k, v in ab.items():
        # pre-screening
        incld_fw = [i for i in range(len(v)) if v[i] in fw]
        incld_kw = [i for i in range(len(v)) if v[i] in kw]
        if not incld_fw or not incld_kw:
            continue
        
        # retrieve document year
        yr = meta.loc[[int(k)]]['Publication Year'].iat[0]
        yr_docs[yr] = yr_docs[yr] + 1

        # collection of words
        word_lst =[]
        for key in kw:
            # get words in proximity of key in kw
            if key not in v: 
                continue
            kw_idx = v.index(key)
            search_start = max(kw_idx - w - 1, 0)
            search_end = min(kw_idx + w + 1, len(v))
            word_lst += v[search_start:search_end] 
            yr_words[yr] = yr_words[yr] + word_lst  

    # get word frequencies for each year
    yr_wordist = {}
    for yr, w in yr_words.items():
        if not w:
            continue
        else:
            fdist = FreqDist(w)
            fdist_sorted = {k: v for k, v in sorted(fdist.items(), key=lambda item: item[1],reverse = True)}
            yr_wordist[yr] = [yr_docs[yr],
                              list(fdist_sorted.keys())[:top_k],
                              list(fdist_sorted.values())[:top_k]
                             ]    
    # output
    return(yr_wordist)