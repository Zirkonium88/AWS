
# Load libs
library(foreach)
library(parallel)
library(doParallel)
library(pracma)

data <- list()
time <- list()
  
#numCores <- detectCores()
numCores <- 2
k <-  10000

# Create cluster
print(paste0("The following number cores has been detected: ", numCores))
cl <- makeCluster(numCores)
registerDoParallel(cl)

for(j in 1:100) {
  # Use Monte Carlo to estimate pi
  start <- Sys.time()
  results <- foreach(i=1:k) %dopar% {
    x=runif(k)
    y=runif(k)
    z=sqrt(x^2+y^2)
    pi <- length(which(z<=1))*4/length(z)
  }
  end <- Sys.time()
  diff <- end-start
  
  data[j] <- results[k]
  time[j] <- diff
}

df <- data.frame(unlist(data),unlist(time))
colnames(df) <- c("pi","runtime")
print(df)
