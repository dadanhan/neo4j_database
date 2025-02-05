# command to create neo4j docker image

docker run \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=/path/to/your/data:/data \
    neo4j:5.26.1

default username/password is neo4j/neo4j

# save locally 

docker save -o neo4j-5.26.1.tar neo4j:5.26.1

# load locally
docker load --input neo4j-5.26.1.tar