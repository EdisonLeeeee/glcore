import torch
from glcore.sampler import neighbor_sampler_cpu


def assert_error(*args, **kwargs):
    raise RuntimeError("glcore was compiled without support for CUDA.")


try:
    from glcore.ops import topk
    from glcore.ops import dimmedian_idx
except ModuleNotFoundError:
    topk = dimmedian_idx = assert_error


__all__ = ["neighbor_sampler_cpu", "topk", "dimmedian_idx"]
