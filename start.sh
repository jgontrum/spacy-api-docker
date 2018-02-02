#!/bin/bash

sed -i "s/PORT/$PORT/g" /etc/nginx/sites-enabled/default
supervisord -n
