#!/usr/bin/env bash

ps -ef | grep python3 | cut -c 9-15| xargs sudo kill -s 9
