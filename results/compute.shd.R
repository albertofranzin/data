suppressMessages(library("bnstruct"))
library("bnstruct")

# usage: Rscript compute.shd.R <mode> <mat.1> <mat.2>
# mode: 1 to compare 2 adjacency matrices contained in two files
#       2 to compare two matrices, the first in a file, the second as string of factors
# mat.1: adjacency matrix file
# mat.2: adjacency matrix file or string, depending on mode parameter

args         <- commandArgs(trailingOnly = TRUE)
mode         <- as.integer(args[1])
input.file.1 <- args[2]
a <- read.table(input.file.1, header=FALSE, sep=" ")
if (mode == 1) {
  input.file.2 <- args[3]
  b <- read.table(input.file.2, header=FALSE, sep=" ")
} else if (mode == 2) {
  b <- factors.to.graph(args[3])
}

cat("SHD: ", shd(a,b),"\n")
