# check_gpu.py
import torch
import subprocess

print("🔍 Checking GPU Status...\n")

# 1. Check NVIDIA driver
try:
    result = subprocess.check_output(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"])
    print("✅ NVIDIA GPU detected:")
    print(result.decode().strip())
except:
    print("❌ NVIDIA GPU not found (or nvidia-smi not in PATH)")

# 2. Check PyTorch + CUDA (this is what our RAG system uses)
print("\n🔥 PyTorch GPU Check:")
print(f"CUDA available      : {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU device name     : {torch.cuda.get_device_name(0)}")
    print(f"CUDA version        : {torch.version.cuda}")
    print(f"GPU memory          : {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # Quick test: move a tensor to GPU
    x = torch.rand(1000, 1000).cuda()
    y = torch.rand(1000, 1000).cuda()
    z = x @ y
    print("✅ GPU tensor test passed! (GPU is fully functional)")
else:
    print("⚠️  CUDA not available → running on CPU only")

print("\n" + "="*60)
print("If you see 'CUDA available: True' + tensor test passed → your GPU is ready for faster embeddings & LLM!")