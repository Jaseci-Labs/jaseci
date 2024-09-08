find . -name "*.svg" -exec rsvg-convert -f pdf -o '{}'.pdf '{}' \;
