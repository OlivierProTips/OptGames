#!/bin/bash
docker build --tag=whamazon .
docker run -p 1337:80 --rm --name=whamazon -it whamazon