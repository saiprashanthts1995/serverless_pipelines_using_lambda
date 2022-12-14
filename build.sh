#!/bin/bash
# Below code works in normal shell
declare -a PYTHON_PACKAGES=('github_archive')

rm -rf build
echo "creating the folder for downloading the python packages present in requirements_for_build.txt"
mkdir build


rm -rf build_code
echo "creating the folder for lambda code"
mkdir build_code


python3 -m pip install -r requirements.txt -t build

for package in ${PYTHON_PACKAGES[@]}
do
  echo "Zipping the contents present inside "$package
  zip -rq build_code/${package}.zip $package
  cd build
  echo "Adding the packages present in requirements_for_build.txt to the package "$package
  zip -rq ../build_code/${package}.zip .
done

echo "Process Completed"

rm -rf ../build
