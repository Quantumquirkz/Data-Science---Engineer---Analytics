get_script_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    return(dirname(sub("^--file=", "", file_arg[1])))
  }
  getwd()
}

script_dir <- get_script_dir()
d1=read.table(file.path(script_dir, "../data/raw/student-mat.csv"), sep=";", header=TRUE)
d2=read.table(file.path(script_dir, "../data/raw/student-por.csv"), sep=";", header=TRUE)

d3=merge(d1,d2,by=c("school","sex","age","address","famsize","Pstatus","Medu","Fedu","Mjob","Fjob","reason","nursery","internet"))
print(nrow(d3)) # 382 students
