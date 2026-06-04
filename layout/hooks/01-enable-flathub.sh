#!/bin/bash
# BrambleOS ISO Build Hook: Enable Flathub Natively

echo "Configuring Flatpak and Flathub repository..."

# 1. Add the official Flathub repository link to the system profile
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# 2. Force the GNOME Software center to refresh its database to show Flatpaks instantly
glib-compile-schemas /usr/share/glib-2.0/schemas/ 2>/dev/null