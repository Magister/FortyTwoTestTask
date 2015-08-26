#!/bin/sh

echo "Cleaning old static..."
rm -rf static/*
echo "Installing bower dependencies..."
make bower-install
echo "Running post-deploy script..."
../uwsgi/post_deploy.sh
