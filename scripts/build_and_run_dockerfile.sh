docker build -f Dockerfile.base -t brain-computer-interface .

# you might want to expose some ports using the -p flag
docker run -ti --rm --name my-brain-computer-interface -v ./shared:/shared brain-computer-interface
