#!/bin/sh

echo "Cleaning old static..."
if [ ! -d assets/libs ]; then
    rm -rf assets/libs
fi
rm -rf static/*
echo "Installing bower dependencies..."
make bower-install
echo "Running post-deploy script..."
sh ../uwsgi/post_deploy.sh
