#!/bin/bash

sudo su - postgres  <<'EOF'
createuser treschat_app
createdb treschatdb
psql -c "ALTER ROLE treschat_app WITH password '12345treschatdb67890'"
psql -c "GRANT ALL PRIVILEGES ON DATABASE treschatdb TO treschat_app"
exit
EOF