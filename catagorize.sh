#! /bin/bash

# Moves Talisman Test Suite images into folders for each disease category.
# Run HUtoRGB.py before running this script.

mkdir healthy
mkdir emphysema
mkdir ground_glass
mkdir fibrosis
mkdir micronodules

mv healthy_* healthy/.
mv emphysema_* emphysema/.
mv ground_glass_* ground_glass/.
mv fibrosis_* fibrosis/.
# slow hack to get around limitations of mv
find . -name 'micronodules_*' -exec mv {} micronodules/. \;
