# Machine Learning Engineer Technical Assignment

Build and Running instructions:
1. Clone this repo into the directory of your choice
2. From the command line, cd into the cloned directory (in the same directory as the Dockerfile)
3. In this directory, create a directory named 'data', and inside 'data', a directory named 'wavs'
4. From the command line, cd into the cloned directory and run the command: docker build -t scraper_image .
5. From the same directory as above, run command: docker run -it -v <path/to/cloned/directory>:/root/data --name scraper_cntnr scraper_image
6. From the same directory as above, run command: start -i scraper_cntnr
7. After the process has completed, the 'data' folder will be populated

Thank you!
