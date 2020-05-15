#!/usr/bin/env bash
source ../venv/bin/activate

if [ ! -f ".env" ];then
    echo "Create the env file as production"
    cp env.txt .env
fi

#while true; do
#    flask deploy
#    # shellcheck disable=SC2181
#    if [[ "$?" == "0" ]]; then
#        break
#    fi
#    echo Deploy command failed, retrying in 5 secs...
#    sleep 5
#done

nohup gunicorn -b :5000 --access-logfile - --error-logfile - start_app:flask_app > flask_node.log 2>&1 &
