#!/bin/bash

PORTCHECK="ss -lptnH sport ="

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PORTCHECK="ss -lptnH sport ="
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PORTCHECK="lsof -i"
fi

python3 -m venv env
source 'env/bin/activate'

export PYTHONPATH="$(pwd)"

pip3 install -r <(comm -23 <(cat venvpackages.txt | sort | uniq) <(pip freeze | sort | uniq))

docker_port=0
for (( i = 5000; i < 65535; i++ )); do
    docker_port=$($PORTCHECK :$i)
    if [ -z "$docker_port" ]; then # Finding first free port
      # shellcheck disable=SC2155
      export POSTGRES_PORT=$i
      break
    fi
done


#Starting up docker container
cat ./DB_and_comm/docker/docker-compose-template.yml | sed "s/DOCKERPORT/${POSTGRES_PORT}/g" > ./DB_and_comm/docker/docker-compose.yml
sudo docker compose -f ./DB_and_comm/docker/docker-compose.yml --env-file ./.env up -d

back_end_port=0
for (( i = 5000; i < 8000; i++ )); do
     back_end_port=$($PORTCHECK :$i)
    if [ -z "$back_end_port" ]; then # Finding first free port
      # shellcheck disable=SC2155
      export back_end_port=$i
      break
    fi
done

# Starting up backend
env/bin/flask --app ./DB_and_comm/backend/endpoints.py run --debug --port "${back_end_port}" &
backendpid="$!"

front_end_port=0
for (( i = 5000; i < 8000; i++ )); do
     front_end_port=$($PORTCHECK :$i)
    if [ -z "$front_end_port" ]; then # Finding first free port
      if [ "$i" != "$back_end_port" ]; then
        # shellcheck disable=SC2155
        export front_end_port=$i
        break
      fi
    fi
done

# Starting up front end
env/bin/flask --app ./Web_UI/app.py run --port "${front_end_port}" &
frontendpid="$!"

sleep 4

echo ""
echo "---------------- PORT INFO ----------------"
echo "$POSTGRES_PORT" " : PostGRES port"
echo "$back_end_port" " : DB_and_comms port"
echo "$front_end_port" " : Web_UI port <- OPEN THIS ONE"
echo ""

read -p "press enter to quit and cleanup"

kill $backendpid $frontendpid