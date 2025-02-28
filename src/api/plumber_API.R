#/usr/local/bin/Rscript

# install.packages if not installed
if (!require('plumber', quietly = TRUE)) {
  install.packages('plumber')
}
if (!require('ggplot2', quietly = TRUE)) {
  install.packages('ggplot2')
}
if (!require('httr', quietly = TRUE)) {
  install.packages('httr')
}
if (!require('jsonlite', quietly = TRUE)) {
  install.packages('jsonlite')
}

if (!require('dplyr', quietly = TRUE)) {
  install.packages('dplyr')
}

if (!require("BiocManager", quietly = TRUE)){
    install.packages("BiocManager")
    
}

if (!require("chromPlot", quietly = TRUE)){
    BiocManager::install("chromPlot")
    
}

# load libraries
library(plumber)
library(ggplot2)
library(httr)
library(jsonlite)
library(dplyr)
library(BiocManager)



#* @apiTitle Genome Variant API
#* Barplot of the number of variants per chromosome for a given genome.

#* @get /count_variants
#* @param genome_id The genome ID to fetch variant counts for
#* @serializer contentType list(type = 'image/png')

function(genome_id = '') {

  url = paste0('http://localhost:3000/api/genomes/', genome_id, '/variants')
  request = GET(url)
  response = content(request, as = 'text', encoding = 'UTF-8')
  
  df = fromJSON(response)
  
  # Create a temporary file to save the plot
  tmp = tempfile(fileext = '.png')
  png(tmp, width = 800, height = 600)

  tryCatch({
    p = ggplot(df, aes(x = chromosome_id, y = num_variants)) +
        geom_bar(stat = 'identity') +
        theme_minimal() +
        labs(title = paste('Number of Variants per Chromosome for Genome', genome_id),
            x = 'Chromosome',
            y = paste('Number of Variants', genome_id))
      print(p)
  }, error = function(e) {
    print('Error creating plot, check the input is correct')
  }
  )

  dev.off()
    
    # Read the image back and return it
    readBin(tmp, 'raw', n = file.info(tmp)$size)
 
}

#* @get /plot_chromosome
#* @param genome_id The genome ID 
#* @serializer contentType list(type = 'pdf')

function(genome_id = '') {
  
  # use curl to get data from GenomeVarAPI
  url = paste0('http://localhost:3000/api/variants/', genome_id)


  response = tryCatch({
      GET(url)
      }, error = function(e) {
          print('Error fetching data from GenomeVarAPI')
          quit()
      })


  if (status_code(response) == 200){
      data = content(response, as = 'text', encoding = 'UTF-8')
      df = fromJSON(data)


      chromPlot_df = df %>% dplyr::select(chromosome_id, position, gene_name) %>%
                      dplyr::mutate(Start = position, End = position) %>%
                      dplyr::rename(Chrom = chromosome_id, Name = gene_name) %>%
                      dplyr::select(-position) 

        # Create a temporary file to save the plot
        tmp = tempfile(fileext = '.png')
        png(tmp, width = 800, height = 600)


        # print(chromPlot_df)
        chromPlot(gaps=chromPlot_df)

        dev.off()

        readBin(tmp, 'raw', n = file.info(tmp)$size)


  } else {
      print('Error fetching data from GenomeVarAPI')
  }

}