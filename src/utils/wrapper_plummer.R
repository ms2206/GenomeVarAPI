#/usr/local/bin/Rscript

# wrapper to run plumber with file at $1
library(plumber)

args = commandArgs(trailingOnly = TRUE)

filepath = args[1]


plumber::plumb(filepath)$run(port=3001)
