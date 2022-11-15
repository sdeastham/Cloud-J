#!/bin/bash

if [[ ! -L Code.Cloud-J ]]; then
    ln -s ../../../. Code.Cloud-J
fi

nc_inc=$( nf-config --includedir )
ncf_lib=$( nf-config --flibs )
cj_lib="-LCode.Cloud-J/build/src/Core -lCloudJ_Core"

# Remove any leftovers
if [[ -e CloudJ.pyf ]]; then
    rm CloudJ.pyf
fi
for f in CloudJ.cpython*.so; do
    if [[ -f $f ]]; then
        rm $f
    fi
done

# Split into two so that we can inspect the pyf file
python3 -m numpy.f2py Code.Cloud-J/src/Interfaces/Python/CJ77.f90 -m CloudJ -h CloudJ.pyf
#python3 -m numpy.f2py ${ncf_lib} ${cj_lib} -c --f90flags="-fcheck=bounds -fcheck=pointer -ffpe-trap=invalid,zero,overflow" --debug -I${nc_inc} -ICode.Cloud-J/build/mod CloudJ.pyf Code.Cloud-J/src/Interfaces/Python/CJ77.f90
python3 -m numpy.f2py ${ncf_lib} ${cj_lib} -c -I${nc_inc} -ICode.Cloud-J/build/mod CloudJ.pyf Code.Cloud-J/src/Interfaces/Python/CJ77.f90
