#!/bin/bash

# Script for adding source files to grader
# Copyright 2014 Bogdan Cristian Tataroiu, Andrei Parvu
# ONI 2014, Pitesti

if ! [ $# -eq 1 ]; then
  echo "$0 problem_name"
  exit
fi

set -e

GRADER="/home/$USER/Desktop/grader"

prob_name=$1

rm -rf $prob_name
unzip ${prob_name}.zip
rm -rf __MACOSX/

sudo rm -rf $GRADER/stud/*${prob_name}*

mkdir -p $GRADER/prob/${prob_name}

cp -f ${prob_name}/teste/* ${GRADER}/prob/${prob_name}/
cd ${prob_name}
for file in *.c*; do
  echo "Creating ${file%%.c*} directory..."
  mkdir -p ${GRADER}/stud/${file%%.c*};
  cp $file ${GRADER}/stud/${file%%.c*}/${prob_name}.${file##*.};
done

cd -
cd ${GRADER}/stud/
echo "   ID         Surname          Given-name           From" > ~/Desktop/grader/stud.txt

for dir in *; do
  echo -e "$dir\t$dir\t$dir\thome";
done >> ../stud.txt

cd -
cd ${GRADER}
echo $prob_name > total-probs.txt
cd -

