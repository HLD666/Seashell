#!/usr/bin/env bash

# Get last version
version=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
echo Get last webdriver version: ${version}

# Download the last version chrome driver for linux.
rm -f chromedriver_linux64.zip
wget https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip

# Extract driver to python env path
unzip chromedriver_linux64.zip -d ../../venv/bin/
rm -f chromedriver_linux64.zip
