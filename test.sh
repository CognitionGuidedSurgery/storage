#!/bin/sh

curl http://localhost:5000/info

curl -X PUT -H "Content-Type: application/binary" --data-binary "@requirements.txt" http:/localhost:5000/requirements.$$.txt

curl http://localhost:5000/requirements.$$.txt > test.txt

diff requirements.txt test.txt