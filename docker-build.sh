# !/bin/bash

prj_dir="/home/thawnf/dev/soa/midproj-650554530"


docker build -t thethanh02/cellphones_service:latest $prj_dir"/cellphones_service"
docker build -t thethanh02/fpt_service:latest $prj_dir"/fpt_service"
docker build -t thethanh02/gearvn_service:latest $prj_dir"/gearvn_service"
docker build -t thethanh02/caching_service:latest $prj_dir"/caching_service"
docker build -t thethanh02/comparision_service:latest $prj_dir"/comparision_service"
docker build -t thethanh02/comparision_client:latest $prj_dir"/client"