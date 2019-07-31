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
echo -e "\033[1;32mstarting to compile ffmpeg.\033[0m"
tar xjvf nasm-2.13.02.tar.bz2 -C ./build
cd ./build/nasm-2.13.02
#./autogen.sh
./configure --prefix=${prefix} --bindir=${prefix}"/bin"
make -j4
make install
cd -
tar -xzvf yasm-1.3.0.tar.gz -C ./build
cd ./build/yasm-1.3.0
./configure --prefix=${prefix} --bindir=${prefix}"/bin"
make -j4
make install
cd -
tar -xzvf x264.tar.gz -C ./build
cd ./build/x264
export PKG_CONFIG_PATH=${prefix}"/lib/pkgconfig"
export PATH=$PATH:${prefix}"/bin"
./configure --prefix=${prefix} --bindir=${prefix}"/bin" --enable-static --enable-pic
make -j4
make install
cd -
tar -xzvf x265_2.6.tar.gz -C ./build
cd ./build/x265_v2.6/build/linux
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=${prefix} -DENABLE_SHARED:BOOL=off -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true ../../source
make -j4
make install
cd -
tar -xzvf fdk-aac.tar.gz -C ./build
cd ./build/fdk-aac
#autoreconf -fiv
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC
make -j4
make install
cd -
tar -xzvf lame-3.100.tar.gz -C ./build
cd ./build/lame-3.100
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC
make -j4
make install
cd -
tar -xzvf opus-1.2.1.tar.gz -C ./build
cd ./build/opus-1.2.1
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC
make -j4
make install
cd -
tar -xzvf libogg-1.3.3.tar.gz -C ./build
cd ./build/libogg-1.3.3
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC
make -j4
make install
cd -
tar -xzvf libvorbis-1.3.5.tar.gz -C ./build
cd ./build/libvorbis-1.3.5
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC
make -j4
make install
cd -
mkdir ./build/libvpx
tar -xzvf libvpx.tar.gz -C ./build/libvpx
cd ./build/libvpx
export PATH=$PATH:${prefix}"/bin"
./configure --prefix=${prefix} --enable-pic  --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm
make -j4
make install
cd -
tar -xjvf ffmpeg-snapshot.tar.bz2 -C ./build
cd ./build/ffmpeg
export PATH=$PATH:${prefix}"/bin"
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${prefix}"/lib/pkgconfig"
./configure --prefix=${prefix} \
  --pkg-config-flags="--static" \
  --extra-cflags=-I${prefix}"/include" \
  --extra-ldflags=-L${prefix}"/lib" \
  --extra-libs=-lpthread \
  --extra-libs=-lm \
  --bindir=${prefix}"/bin" \
  --enable-gpl \
  --enable-libfdk_aac \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree \
  --enable-avresample \
  --enable-shared \
  --disable-static
make -j4
make  install
cd -
echo -e "\033[1;32mDone\033[0m"
