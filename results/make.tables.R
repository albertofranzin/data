suppressMessages
get.inst.name <- function(name, s = "_") {
  #print(name)
  curr.tokens <- unlist(strsplit(name, '_'))
  curr <- paste(c(curr.tokens[1], curr.tokens[2]), collapse=s)
  return(curr)
}

results <- c()
instances <- c()
for (f in c("time/time_eocp.txt", "time/time_mmhc.txt", "time/time_gobnilp_palim.txt", "time/time_gobnilp_scores.txt")) {
  d <- as.matrix(read.table(f, header = FALSE, sep = " "))#, col.names=c("instance", "score")))
  vals <- c()
  curr <- get.inst.name(d[1,1])
  if (!is.element(curr, instances)) {
    instances <- c(instances, curr)
  }
  for (i in 1:nrow(d)) {
    inst.name <- d[i,1] <- get.inst.name(d[i,1])
    val       <- as.numeric(d[i,2])
    print(d[i,2])
    if (curr == get.inst.name(inst.name)) {
      vals <- c(vals, val)
    } else {
      print(paste(curr, median(vals, TRUE)))
      results <- c(results, median(vals, TRUE))
      curr <- get.inst.name(inst.name)
      if (!is.element(curr, instances)) {
        instances <- c(instances, get.inst.name(curr))
      }
      vals <- c()
    }
  }
  print(paste(curr, median(vals, TRUE)))
  results <- c(results, median(vals, TRUE))
  if (!is.element(curr, instances)) {
    instances <- c(instances, get.inst.name(curr))
  }
}
print(results)
results <- (matrix(results, c(length(results)/4,4)))
print(results)
rs <- NULL
for (row in 1:nrow(results)) {
  rs[[row]] <- paste(paste(c(instances[row], results[row,]), collapse=" & "), "\\\\")
}
write(rs, file="time/timetable.tex")