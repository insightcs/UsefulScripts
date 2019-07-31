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
echo -e "\033[1;32mstarting to compile gstreamer.\033[0m"
sleep 2
#tar -xzvf libffi-3.2.1.tar.gz -C ./build
#cd ./build/libffi-3.2.1
#./configure --prefix=${prefix} --enable-shared=yes --enable-static=no
#make -j4
#make  install
#cd -
#tar -xvf libxml2-2.9.5.tar -C ./build
#cd ./build/libxml2-2.9.5
#./configure --prefix=${prefix} --enable-shared=yes --enable-static=no --with-python=no
#make -j4
#make install
#cd -
#tar -xvf glib-2.50.3.tar -C ./build
#cd ./build/glib-2.50.3
#./configure --prefix=${prefix} --enable-shared=yes --enable-static=no --enable-libmount=no
#make -j4
#make install
#cd -
#tar -xzvf gstreamer-0.10.36.tar.gz -C ./build
cd ./build/gstreamer-0.10.36
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${prefix}"/lib/pkgconfig"
export PATH=${prefix}"/bin":$PATH
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no --disable-loadsave
make -j4
make install
cd -
tar -xzvf gst-plugins-base-0.10.36.tar.gz -C ./build
cd ./build/gst-plugins-base-0.10.36
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no --enable-orc=no
make -j4
make install
cd -
tar -xzvf boost_1_59_0.tar.gz -C ./build
cd ./build/boost_1_59_0
./bootstrap.sh --prefix=${prefix}
./b2 --build-type=minimal link=shared  install
cd -
echo -e "\033[1;32mDone\033[0m"
