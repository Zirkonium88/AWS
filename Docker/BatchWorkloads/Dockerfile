FROM r-base
ADD pi.R /usr/local/src/myscripts/
ADD installDependencies.R /usr/local/src/myscripts/
RUN Rscript /usr/local/src/myscripts/installDependencies.R
WORKDIR /usr/local/src/myscripts/
CMD ["Rscript", "pi.R"]