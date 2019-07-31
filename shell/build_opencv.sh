#!/bin/bash
set -e
#
dir=$(pwd)
prefix=${dir}/local
if [ ! -d "$prefix" ]
then 
	mkdir ${prefix}
fi
#tar -xzvf source_packages.tar.gz
#cd source_packages
if [ ! -d "./build" ]
then
        mkdir ./build
fi
echo -e "\033[1;32mstarting to compile opencv.\033[0m"
sleep 2
tar -xzvf opencv-3.1.0.tar.gz -C ./build
tar -xzvf opencv_contrib.tar.gz -C ./build
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${prefix}"/lib/pkgconfig"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${prefix}"/lib"
cd ./build/opencv-3.1.0
if [ ! -d "./build" ]
then
	mkdir ./build
fi
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=${prefix} \
		-D INSTALL_C_EXAMPLES=OFF \
		-D INSTALL_PYTHON_EXAMPLES=OFF \
		-D BUILD_PNG=ON \
		-D BUILD_JASPER=ON \
		-D BUILD_JPEG=ON \
		-D BUILD_TIFF=ON \
		-D BUILD_ZLIB=ON \
		-D BUILD_TBB=ON \
		-D WITH_JPEG=ON \
		-D WITH_PNG=ON \
		-D WITH_JASPER=ON \
		-D WITH_TIFF=ON \
		-D WITH_ZLIB=ON \
		-D WITH_QT=OFF \
		-D WITH_OPENGL=OFF \
		-D PYTHON_EXCUTABLE=/usr/bin/python2.7 \
		-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
		-D BUILD_EXAMPLES=OFF ..
sed -i 's#/lib/libbz2.so.1#/lib64/libbz2.so.1#g' CMakeCache.txt
make -j4
make install
cd - && cd -
echo -e "\033[1;32mDone\033[0m"
