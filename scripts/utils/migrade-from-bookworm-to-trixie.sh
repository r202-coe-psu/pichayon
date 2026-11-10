#!/bin/bash

echo "Update current version"
sudo apt update
sudo apt full-upgrade -y


echo "Upgrade new version"
sudo sed -i 's/bookworm/trixie/g' /etc/apt/sources.list /etc/apt/sources.list.d/*.list
sudo apt update -y
sudo apt full-upgrade -y \
  -o Dpkg::Options::="--force-confdef" \
  -o Dpkg::Options::="--force-confnew" \
  --purge --auto-remove

echo "Remove obsolete package"
sudo apt purge '?obsolete' -y
sudo apt purge '?config-files' -y
sudo apt autoremove -y

