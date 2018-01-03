library(stringr)
setwd("C:\\Users\\Trevor Lee\\Documents\\workspace\\tobigs 8th project")
fileName <- commandArgs(trailingOnly=TRUE)

data<-read.csv(fileName[1], sep = ",", stringsAsFactor = F, header = F)

data<-t(data)
# colnames(data) <- t(data)[,1]
rownames(data) <- NULL
# data <- data[-1,]
# head(data)

# data[1,1]
# str(data)

rst <- matrix(ncol=3)
colnames(rst) <- c("keyword","start","end")
for(j in 1:dim(data)[2])
{
  keyword = NULL
  start = NULL
  end = NULL
  for(i in 1:(length(data[data[,j] != "",j])-1))
  {
    if(i == 1) # store ketword
    {
      keyword <- data[i,j]
    }
    else # store start, end time
    {
      data[i,j] <- unlist(str_split(data[i,j], "T"))[1]
      if(is.null(start))
        start = as.Date(data[i,j])
      if(as.Date(data[i,j]) - as.Date(data[i+1,j]) == 1)
      {
        end = as.Date(data[i+1,j])
      }
      else
      {
        if(!is.null(end))
        {
          # cat(keyword, '\t', format(start, "%Y.%m.%d"), '\t', format(end, "%Y.%m.%d"), "\n")
          rst<-rbind(rst, c(keyword, format(start, "%Y.%m.%d"), format(end, "%Y.%m.%d")))
        }
        else
        {
          # cat(keyword, '\t', format(start, "%Y.%m.%d"), '\t', format(start, "%Y.%m.%d"), "\n")
          rst<-rbind(rst, c(keyword, format(start, "%Y.%m.%d"), format(start, "%Y.%m.%d")))
        }
        start = NULL
        end = NULL   
      }
    }
  }
}
rst <- rst[-1,]
temp <- rst[,2]
rst[,2] <- rst[,3]
rst[,3] <- temp
write.csv(rst,file = fileName[1], row.names = F)
