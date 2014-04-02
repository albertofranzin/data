suppressMessages
get.inst.name <- function(name, s = "_") {
  #print(name)
  curr.tokens <- unlist(strsplit(name, '_'))
  curr <- paste(c(curr.tokens[1], curr.tokens[2]), collapse=s)
  return(curr)
}

args         <- commandArgs(trailingOnly = TRUE)
inst  <- args[1]
file1 <- args[2]
file2 <- args[3]
file3 <- args[4]
file4 <- args[5]

d1 <- as.matrix(read.table(file1, header = FALSE, sep = " "))
d2 <- as.matrix(read.table(file2, header = FALSE, sep = " "))
d3 <- as.matrix(read.table(file3, header = FALSE, sep = " "))
d4 <- as.matrix(read.table(file4, header = FALSE, sep = " "))


vals <- NULL
vals[[1]] <- list()
vals[[2]] <- list()
vals[[3]] <- list()
vals[[4]] <- list()
k <- 1
for (i in 1:nrow(d1)) {
  inst.name <- get.inst.name(d1[i,1])
  val       <- as.numeric(d1[i,2])
  if (inst == inst.name && !is.na(val)) {
    vals[[k]][[length(vals[[k]])+1]] <- val
  }
}

k <- 2
for (i in 1:nrow(d2)) {
  inst.name <- get.inst.name(d2[i,1])
  val       <- as.numeric(d2[i,2])
  if (inst == inst.name && !is.na(val)) {
    vals[[k]][[length(vals[[k]])+1]] <- val
  }
}

k <- 3
for (i in 1:nrow(d3)) {
  inst.name <- get.inst.name(d3[i,1])
  val       <- as.numeric(d3[i,2])
  if (inst == inst.name && !is.na(val)) {
    vals[[k]][[length(vals[[k]])+1]] <- val
  }
}

k <- 4
for (i in 1:nrow(d4)) {
  inst.name <- get.inst.name(d4[i,1])
  val       <- as.numeric(d4[i,2])
  if (inst == inst.name && !is.na(val)) {
    vals[[k]][[length(vals[[k]])+1]] <- val
  }
}

#print(vals)

boxplot(c(unlist(vals[[1]])), c(unlist(vals[[2]])), c(unlist(vals[[3]])), c(unlist(vals[[4]])),
        names=c("EO-CP", "MMHC", "G-Pa", "G-S"),
        col=c("red", "blue", "green", "yellow"))
