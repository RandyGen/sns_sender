#!/bin/sh

SNS_TYPE=all
# MESSAGE=hello

python sender.py \
  --sns_type ${SNS_TYPE}
  # --message ${MESSAGE}