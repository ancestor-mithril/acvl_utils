from typing import Union

import numpy as np
import torch
from skimage.morphology import binary_dilation, binary_erosion
from torch import nn
from dynamic_network_architectures.building_blocks.helper import convert_dim_to_conv_op
from acvl_utils.morphology_helper import generate_ball
from torch.backends import cudnn


def gpu_binary_dilation(binary_array: Union[np.ndarray, torch.Tensor], selem: np.ndarray) -> Union[np.ndarray, torch.Tensor]:
    assert all([i % 2 == 1 for i in selem.shape]), f"Only structure elements of uneven shape supported. Shape is {selem.shape}"
    with torch.no_grad():
        with torch.cuda.amp.autocast():
            conv = convert_dim_to_conv_op(len(binary_array.shape))(in_channels=1, out_channels=1, kernel_size=selem.shape,
                                                                   stride=1, padding=[round((i - 1) / 2) for i in selem.shape],
                                                                   bias=False)
            conv.weight = nn.Parameter(torch.from_numpy(selem[None, None]).half(), requires_grad=False)
            conv = conv.to(0)
            is_torch = isinstance(binary_array, torch.Tensor)
            if not is_torch:
                binary_array = torch.from_numpy(binary_array)
            binary_array = binary_array.half()
            orig_device = binary_array.device
            binary_array = binary_array.to(0)
            out = (conv(binary_array[None, None]) > 0).to(orig_device)[0, 0]
            if not is_torch:
                out = out.numpy()
    torch.cuda.empty_cache()
    return out


def gpu_binary_erosion(binary_array: Union[np.ndarray, torch.Tensor], selem: np.ndarray) -> Union[np.ndarray, torch.Tensor]:
    assert all([i % 2 == 1 for i in selem.shape]), f"Only structure elements of uneven shape supported. Shape is {selem.shape}"
    with torch.no_grad():
        with torch.cuda.amp.autocast():
            conv = convert_dim_to_conv_op(len(binary_array.shape))(in_channels=1, out_channels=1, kernel_size=selem.shape,
                                                                   stride=1, padding=[round((i - 1) / 2) for i in selem.shape],
                                                                   bias=False)
            conv.weight = nn.Parameter(torch.from_numpy(selem[None, None]).half(), requires_grad=False)
            conv = conv.to(0)
            is_torch = isinstance(binary_array, torch.Tensor)
            if not is_torch:
                binary_array = torch.from_numpy(binary_array)
            binary_array = binary_array.half()
            orig_device = binary_array.device
            binary_array = binary_array.to(0)
            out = (conv(binary_array[None, None]) == selem.sum()).to(orig_device)[0, 0]
            if not is_torch:
                out = out.numpy()
    torch.cuda.empty_cache()
    return out


def gpu_binary_opening(binary_array: Union[np.ndarray, torch.Tensor], selem: np.ndarray) -> Union[np.ndarray, torch.Tensor]:
    return gpu_binary_dilation(gpu_binary_erosion(binary_array, selem), selem)


def gpu_binary_closing(binary_array: Union[np.ndarray, torch.Tensor], selem: np.ndarray) -> Union[np.ndarray, torch.Tensor]:
    return gpu_binary_erosion(gpu_binary_dilation(binary_array, selem), selem)


if __name__ == '__main__':
    cudnn.benchmark = True
    from time import time
    inp = np.zeros((128, 128, 128), dtype=bool)
    inp[10:100, 50:100, 100:120] = True
    selem = generate_ball((7, 7, 7))

    start = time()
    output_gpu = gpu_binary_dilation(inp, selem)
    time_gpu = time() - start

    start = time()
    ref = binary_dilation(inp, selem)
    time_skimage = time() - start

    assert np.all(output_gpu == ref)
    print(f'Dilation: GPU: {time_gpu}s, CPU: {time_skimage} s')

    start = time()
    output_gpu = gpu_binary_erosion(inp, selem)
    time_gpu = time() - start

    start = time()
    ref = binary_erosion(inp, selem)
    time_skimage = time() - start

    assert np.all(output_gpu == ref)
    print(f'Erosion: GPU: {time_gpu}s, CPU: {time_skimage} s')


