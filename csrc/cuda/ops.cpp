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
    const int n_threads = 1024);

at::Tensor dimmedian_idx_forward_cuda(
    torch::Tensor X,
    torch::Tensor edge_idx,
    torch::Tensor edge_weights,
    const int n_rows,
    const int n_threads = 1024);


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

at::Tensor dimmedian_idx_forward(
    torch::Tensor X,
    torch::Tensor edge_idx,
    torch::Tensor edge_weights,
    const int n_rows)
{
  CHECK_CUDA(X);
  CHECK_CUDA(edge_idx);
  CHECK_CUDA(edge_weights);
  return dimmedian_idx_forward_cuda(X, edge_idx, edge_weights, n_rows);
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m)
{
  m.def("topk", &topk_forward, "topk forward");
  m.def("dimmedian_idx", &dimmedian_idx_forward, "dimension wise medain idx forward");
}