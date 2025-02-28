### R code from vignette source 'chromPlot.Rnw'


if (!require("BiocManager", quietly = TRUE)){
    install.packages("BiocManager")
    library(BiocManager)
}

if (!require("chromPlot", quietly = TRUE)){
    BiocManager::install("chromPlot")
    library(chromPlot)
}

if (!require("TxDb.Hsapiens.UCSC.hg19.knownGene", quietly = TRUE)){
    BiocManager::install("TxDb.Hsapiens.UCSC.hg19.knownGene")
    library(TxDb.Hsapiens.UCSC.hg19.knownGene)
}

if (!require("httr", quietly = TRUE)){
    install.packages("httr")
    library(httr)
}

if (!require("jsonlite", quietly = TRUE)){
    install.packages("jsonlite")
    library(jsonlite)
}

if (!require("dplyr", quietly = TRUE)){
    install.packages("dplyr")
    library(dplyr)
}

###################################################
### code chunk number 1: createGraphminus1
###################################################


# data(hg_gap)
# head(hg_gap)

# chromPlot(gaps=hg_gap)


fake_df = data.frame(
            Chrom = c("1", "1", "1", "1", "1", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2"),
            Start = c(20288, 65355, 110423, 136739, 158305, 240436, 280258, 305267, 350414, 388086, 397210, 400385, 401608, 405400, 406849, 409629, 413637, 416882, 418555, 425715),
            End = c(20288, 65355, 110423, 136739, 158305, 240436, 280258, 305267, 350414, 388086, 397210, 400385, 401608, 405400, 406849, 409629, 413637, 416882, 418555, 425715),
            Name = c("GeneA", "GeneB", "GeneC", "GeneD", "GeneE", "GeneF", "GeneG", "GeneH", "GeneI", "GeneJ", "GeneK", "GeneL", "Solyc01g005570.2.1", "GeneM", "GeneN", "GeneO", "GeneP", "GeneQ", "GeneR", "GeneS")
            )

# head(fake_df)
# chromPlot(gaps=fake_df)


###################################################
### Get data from GenomeVarAPI
###################################################

# use curl to get data from GenomeVarAPI
url = 'http://localhost:3000/api/variants/RF_041'


response = tryCatch({
    GET(url)
    }, error = function(e) {
        print('Error fetching data from GenomeVarAPI')
        quit()
    })


if (status_code(response) == 200){
    data = content(response, as = 'text', encoding = 'UTF-8')
    df = fromJSON(data)

    chromPlot_df = df %>% select(chromosome_id, position, gene_name) %>%
                    mutate(Start = position, End = position) %>%
                    rename(Chrom = chromosome_id, Name = gene_name) %>%
                    select(-position) 


    # print(chromPlot_df)
    chromPlot(gaps=chromPlot_df)


} else {
    print('Error fetching data from GenomeVarAPI')
}

