#!/bin/bash


cd ~/alpha-investment
source deployment_env/bin/activate
PYTHONPATH="." python lambda_function/future_rollover.py
deactivate