#/usr/local/bin/Rscript

# install.packages if not installed
if (!require('plumber')) {
  install.packages('plumber')
}
if (!require('ggplot2')) {
  install.packages('ggplot2')
}
if (!require('httr')) {
  install.packages('httr')
}
if (!require('jsonlite')) {
  install.packages('jsonlite')
}

if (!require('dplyr')) {
  install.packages('dplyr')
}

# load libraries
library(plumber)
library(ggplot2)
library(httr)
library(jsonlite)
library(dplyr)


#* @apiTitle Genome Variant API
#* get some data from GenomeVarAPI

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