#!/bin/sh

. /opt/hotcake/venv/bin/activate

if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
  # generate RSA key for ssh server
  ckeygen -t rsa -f /etc/ssh/ssh_host_rsa_key --no-passphrase
fi

# start server
hotcake "$@"
