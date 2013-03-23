#!/bin/bash
wget http://redis.googlecode.com/files/redis-2.6.11.tar.gz
tar xzf redis-2.6.11.tar.gz
cd redis-2.6.11
make
cd src
cp redis-benchmark /usr/bin/redis-benchmark
cp redis-check-aof /usr/bin/redis-check-aof
cp redis-cli /usr/bin/redis-cli
cp redis-server /usr/bin/redis-server
cd ../../
rm -rf redis-2.6.11*

                 
