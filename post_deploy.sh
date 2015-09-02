#!/bin/sh

echo "Cleaning old static..."
rm -rf assets/libs
rm -rf static/*
echo "Installing bower dependencies..."
make bower-install
echo "Running post-deploy script..."
sh ../uwsgi/post_deploy.sh
