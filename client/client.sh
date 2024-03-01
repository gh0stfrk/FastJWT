#!/bin/bash

URL=http://localhost:8080


if [[ $# -eq 0 ]]; then
    echo "Error: No arguments provided"
    echo "Usage: $0 <command>"
    exit 1
fi

function auth(){

    if [[ $# -ne 2 ]]; then
        echo "Error: Invalid number of arguments"
        echo "Usage: $0 auth <email> <password>"
        exit 1
    fi
    data="{\"email\":\"${1}\",\"password\":\"${2}\"}"
    curl -X POST -H "Content-Type: application/json" -d "$data" ${URL}/auth
}

function create_user() {
    data="{\"email\":\"${1}\",\"password\":\"${2}\"}"
    curl -X GET -H "Content-Type: application/json" -d "$data" ${URL}/fill
}


case $1 in
    "auth")
        auth $2 $3
        ;;
    "create_user")
        create_user $2 $3
        ;;
    *)
        echo "Invalid arguments"
        echo "Valid arguments : auth, create_user"
        exit 1
esac

