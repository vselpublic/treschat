#!/bin/bash

export FLASK_CONFIG="development"
export SECRET_KEY="4bs^7bre5aq8%$&JFDgtfd4#@"
export DEV_DATABASE_URL="postgresql://treschat_app:12345treschatdb67890@fordevpurpose.cn2hbxgdnr5i.eu-west-1.rds.amazonaws.com:5432/treschatdb"
export TEST_DATABASE_URL="postgresql://treschat_app:12345treschatdb67890@localhost/treschatdbtest"
export PROD_DATABASE_URL="postgresql://treschat_app:12345treschatdb67890@localhost/treschatdb"
