docker build -f build/Dockerfile.base -t brain-computer-interface .

# you might want to expose some ports using the -p flag
docker run -ti --rm --name my-brain-computer-interface -v ./shared:/shared brain-computer-interface
# you might want to connect time volumes with '-v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro -v /usr/share/zoneinfo:/usr/share/zoneinfo:ro'
