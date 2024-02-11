docker build -t brain-computer-interface .
docker run -ti --rm -v ./shared:/shared brain-computer-interface
