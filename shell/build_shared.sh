#!/bin/bash
if [ $# -lt 1 ]; then
	#echo "error: need to input installation path"
	#exit 1
	prefix=/usr/local/middle
else
	for arg in "$@"
	do
		echo $arg
	done
	prefix=$1
fi

echo "starting to compile..."
#ffmpeg编译安装
echo "compiling nasm" && \
sudo tar xjvf nasm-2.13.02.tar.bz2 && \
sudo chmod -R 777 nasm-2.13.02 && \
cd nasm-2.13.02 && \
./autogen.sh && \
./configure --prefix=${prefix} --bindir=${prefix}"/bin" && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling yasm" && \
sudo tar xzvf yasm-1.3.0.tar.gz && \
sudo chmod -R 777 yasm-1.3.0 && \
cd yasm-1.3.0 && \
./configure --prefix=${prefix} --bindir=${prefix}"/bin" && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling x264" && \
sudo tar -xzvf x264.tar.gz && \
sudo chmod -R 777 x264 && \
cd x264 && \
export PKG_CONFIG_PATH=${prefix}"/lib/pkgconfig" && \
export PATH=$PATH:${prefix}"/bin" && \
./configure --prefix=${prefix} --bindir=${prefix}"/bin" --enable-static --enable-pic && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling x265" && \
sudo tar -xzvf x265_2.6.tar.gz && \
sudo chmod -R 777 x265_v2.6 && \
cd x265_v2.6/build/linux && \
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=${prefix} -DENABLE_SHARED:BOOL=off -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true ../../source && \
make -j4 && \
sudo make install

cd ../../../ && \
echo "compiling fdk-aac" && \
sudo tar -xzvf fdk-aac.tar.gz && \
sudo chmod -R 777 fdk-aac && \
cd fdk-aac && \
autoreconf -fiv && \
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling mp3lame" && \
sudo tar -xzvf lame-3.100.tar.gz && \
sudo chmod -R 777 lame-3.100 && \
cd lame-3.100 && \
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling opus" && \
sudo tar -xzvf opus-1.2.1.tar.gz && \
sudo chmod -R 777 opus-1.2.1 && \
cd opus-1.2.1 && \
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling ogg" && \
sudo tar -xzvf libogg-1.3.3.tar.gz && \
sudo chmod -R 777 libogg-1.3.3 && \
cd libogg-1.3.3 && \
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling libvorbis" && \
sudo tar -xzvf libvorbis-1.3.5.tar.gz && \
sudo chmod -R 777 libvorbis-1.3.5 && \
cd libvorbis-1.3.5 && \
./configure --prefix=${prefix} --enable-shared=no --enable-static=yes CFLAGS=-fPIC CPPFLAGS=-fPIC && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling libvpx" && \
sudo mkdir libvpx && \
sudo tar -xzvf libvpx.tar.gz -C libvpx && \
sudo chmod -R 777 libvpx && \
cd libvpx && \
export PATH=$PATH:${prefix}"/bin" && \
./configure --prefix=${prefix} --enable-pic  --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling ffmpeg" && \
sudo tar -xjvf ffmpeg-snapshot.tar.bz2 && \
sudo chmod -R 777 ffmpeg && \
cd ffmpeg && \
export PATH=$PATH:${prefix}"/bin" && \
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${prefix}"/lib/pkgconfig" && \
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
  --disable-static && \
make -j4 && \
sudo make install

#gstreamer编译
cd .. && \
echo "compiling libffi" && \
sudo tar -xzvf libffi-3.2.1.tar.gz && \
sudo chmod -R 777 libffi-3.2.1 && \
cd libffi-3.2.1 && \
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling libxml2" && \
sudo tar -xvf libxml2-2.9.5.tar && \
sudo chmod -R 777 libxml2-2.9.5 && \
cd libxml2-2.9.5 && \
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no --with-python=no && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling glib" && \
sudo tar -xvf glib-2.50.3.tar && \
sudo chmod -R 777 glib-2.50.3 && \
cd glib-2.50.3 && \
./autogen.sh && \
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no --enable-libmount=no && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling gstreamer" && \
sudo tar -xzvf gstreamer-0.10.36.tar.gz && \
sudo chmod -R 777 gstreamer-0.10.36 &&\
cd gstreamer-0.10.36 && \
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no && \
make -j4 && \
sudo make install

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${prefix}"/lib/pkgconfig"
./configure --prefix=/home/insight/compiles/local --enable-shared=yes --enable-static=no --disable-loadsave
cd .. && \
echo "compiling gstreamer-plugins-base" && \
sudo tar -xzvf gst-plugins-base-0.10.36.tar.gz && \
sudo chmod -R 777 gst-plugins-base-0.10.36 && \
cd gst-plugins-base-0.10.36 && \
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no --enable-orc=no && \
make -j4 && \
sudo make install

#编译opencv
cd .. && \
echo "compiling opencv" && \
sudo tar -xzvf opencv-3.1.0.tar.gz && \
sudo tar -xzvf opencv_contrib.tar.gz && \
sudo chmod -R 777 opencv-3.1.0 opencv_contrib && \
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${prefix}"/lib/pkgconfig" && \
cd opencv-3.1.0 && \
mkdir build && \
cd build && \
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
		-D BUILD_EXAMPLES=OFF .. && \
sed -i 's#/lib/libbz2.so.1#/lib64/libbz2.so.1#g' CMakeCache.txt && \
make -j4 && \
sudo make install

cd .. && \
echo "compiling curl" && \
sudo tar -xzvf curl-7.58.0.tar.gz && \
sudo chmod -R 777 curl-7.58.0 && \
cd curl-7.58.0 && \
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no && \
make -j4 && \
sudo make install

echo "compiling tensorflow"
chmod +x bazel-0.6.0-installer-linux-x86_64.sh
./bazel-0.6.0-installer-linux-x86_64.sh --user
export PATH=$PATH:$HOME/bin
unzip -xzvf tensorflow-1.5.0-rc0.zip
cd tensorflow-1.5.0-rc0
bazel 




export PATH=$PATH:/usr/local/middle/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/middle/lib
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/middle/lib/pkgconfig

find -name '*.pc' | xargs perl -pi -e 's|/tmp/local|/usr/local/middle/|g'
sed -i 's/\/usr\/local\/middle\//\/usr\/local/g' *.pc
sed -i 's#/lib/libbz2.so.1#/lib64/libbz2.so.1#g' CMakeCache.txt


sudo tar -xzvf pcre-8.40.tar.gz && \
sudo chmod -777 pcre-8.40 && \
cd pcre-8.40 && \
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no --enable-utf8 --enable-unicode-properties && \
make -j4 && \
sudo make install

sudo tar -xzvf libiconv-1.15.tar.gz && \
sudo chmod -777 libiconv-1.15 && \
cd libiconv-1.15 && \
./configure --prefix=${prefix} --enable-shared=yes --enable-static=no && \
make -j4 && \
sudo make install


#cd mysql-5.7.9 && \
#mkdir build && \
#cd build && \
#cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql-5.7.9 \
#-DMYSQL_DATADIR=/var/lib/mysql-5.7.9/data \
#-DDEFAULT_CHARSET=utf8 \
#-DDEFAULT_COLLATION=utf8_general_ci \
#-DMYSQL_TCP_PORT=3306 \
#-DMYSQL_USER=mysql \
#-DWITH_MYISAM_STORAGE_ENGINE=1 \
#-DWITH_INNOBASE_STORAGE_ENGINE=1 \
#-DWITH_ARCHIVE_STORAGE_ENGINE=1 \
#-DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
#-DWITH_MEMORY_STORAGE_ENGINE=1 \
#-DWITH_BOOST=../../boost_1_59_0 .. && \
#make -j4 && \
#sudo make install && \