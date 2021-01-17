#!/bin/bash
sudo jetson_clocks --fan

sudo systemctl restart nvargus-daemon.service

export TF_GPU_ALLOCATOR=CUDA_MALLOC

python3 trt_mtcnn.py --onboard 1
