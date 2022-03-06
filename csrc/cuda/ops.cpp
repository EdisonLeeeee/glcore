#include <torch/extension.h>
#include <ATen/SparseTensorUtils.h>

#include <vector>

#define CHECK_CUDA(x) TORCH_CHECK(x.device().is_cuda(), #x " must be a CUDA tensor")


// CUDA Methods
std::vector<torch::Tensor> topk_forward_cuda(
    torch::Tensor edge_idx,
    torch::Tensor edge_weights,
    const int64_t n_edges,
    const int64_t k,
    const int THREADS = 1024);

// CUDA Methods
at::Tensor dimmedian_idx_forward_cuda(
    torch::Tensor X,
    torch::Tensor rowIndices,
    torch::Tensor colIndices,
    torch::Tensor edge_weights,
    const int64_t N,
    const int THREADS = 1024);


// C++ to CUDA Methods
std::vector<at::Tensor> topk_forward(
    torch::Tensor edge_idx,
    torch::Tensor edge_weights,
    const int64_t n_edges,
    const int64_t k)
{
  CHECK_CUDA(edge_idx);
  CHECK_CUDA(edge_weights);
  return topk_forward_cuda(edge_idx, edge_weights, n_edges, k);
}

// C++ to CUDA Methods
at::Tensor dimmedian_idx_forward(
    torch::Tensor X,
    torch::Tensor rowIndices,
    torch::Tensor colIndices,
    torch::Tensor edge_weights,
    const int64_t N)
{
  CHECK_CUDA(X);
  CHECK_CUDA(rowIndices);
  CHECK_CUDA(colIndices);
  CHECK_CUDA(edge_weights);
  return dimmedian_idx_forward_cuda(X, rowIndices, colIndices, edge_weights, N);
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m)
{
  m.def("topk", &topk_forward, "topk forward");
  m.def("dimmedian_idx", &dimmedian_idx_forward, "dimension wise medain idx forward");
}