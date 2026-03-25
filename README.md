# ComfyUI-FLUX2MAX-KLEIN9B-API-Nodes

Custom ComfyUI nodes for **Flux 2 Max** and **Flux 2 Klein 9B** via the BFL API — with direct IMAGE input support, built-in progress bars, and no extra base64 converter nodes needed.

> 🔀 **Forked from [gelasdev/ComfyUI-FLUX-BFL-API](https://github.com/gelasdev/ComfyUI-FLUX-BFL-API)**
> Original work by [@gelasdev](https://github.com/gelasdev), [@pleberer](https://github.com/pleberer), and [@Duanyll](https://github.com/Duanyll).
> This fork adds Direct nodes that accept IMAGE inputs natively and show polling progress in the ComfyUI UI.

## What's New

| Node | Description |
|---|---|
| **Flux 2 Max Direct (BFL)** | Flux 2 Max with up to 8 IMAGE inputs — no separate base64 node needed |
| **Flux 2 Klein 9B Direct (BFL)** | Flux 2 Klein 9B with up to 4 IMAGE inputs — same deal |

Both Direct nodes:
- ✅ Accept ComfyUI `IMAGE` tensors directly
- ✅ Convert to base64 internally
- ✅ Show a progress bar while polling the BFL API
- ✅ Return a blank image on failure instead of crashing

All original nodes from the upstream project are still included and work as before.

## Installation

1. Clone into your `custom_nodes` folder:
    ```bash
    cd custom_nodes
    git clone https://github.com/olliethomas1992/ComfyUI-FLUX2MAX-KLEIN9B-API-Nodes.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Get your BFL API key from [api.bfl.ai](https://api.bfl.ai).

4. Add your API key to `config.ini`:
    ```ini
    [API]
    X_KEY = YOUR_API_KEY
    BASE_URL = https://api.bfl.ai/v1/
    ```

   Or use a **Flux Config (BFL)** node to set the key per-node.

## All Nodes

### Direct Nodes (New)
| Node | Description |
|---|---|
| Flux 2 Max Direct (BFL) | Flux 2 Max — accepts up to 8 IMAGE inputs directly |
| Flux 2 Klein 9B Direct (BFL) | Flux 2 Klein 9B — accepts up to 4 IMAGE inputs directly |

### Generation (from upstream)
| Node | Description |
|---|---|
| Flux Pro 1.1 (BFL) | Text-to-image with Flux Pro 1.1 |
| Flux Pro 1.1 Ultra (BFL) | High-resolution text-to-image |
| Flux Dev (BFL) | Text-to-image with Flux Dev |
| Flux Pro Fill (BFL) | Inpainting / outpainting |
| Flux Pro Expand (BFL) | Outpainting with directional padding |
| Flux Kontext Pro (BFL) | Image editing with context (up to 4 images) |
| Flux Kontext Max (BFL) | Image editing with context, max quality |
| Flux 2 Max (BFL) | Flux 2 Max generation |
| Flux 2 Pro (BFL) | Flux 2 Pro generation |
| Flux 2 Pro Preview (BFL) | Flux 2 Pro preview |
| Flux 2 Flex (BFL) | Flux 2 Flex generation |
| Flux 2 Klein 9B (BFL) | Flux 2 Klein 9B generation |
| Flux 2 Klein 9B Preview (BFL) | Flux 2 Klein 9B preview |
| Flux 2 Klein 4B (BFL) | Flux 2 Klein 4B generation |

### Finetune
| Node | Description |
|---|---|
| Flux Pro Fill Finetune (BFL) | Inpainting with a finetuned model |
| Flux Pro 1.1 Ultra Finetune (BFL) | Ultra generation with a finetuned model |
| Flux Finetune Status (BFL) | Check finetune job status |
| Flux My Finetunes (BFL) | List all finetunes |
| Flux Finetune Details (BFL) | Get finetune details |
| Flux Delete Finetune (BFL) | Delete a finetune |

### Config & Utils
| Node | Description |
|---|---|
| Flux Config (BFL) | Override API key, base URL and region per-node |
| Flux Credits (BFL) | Check remaining BFL API credits |
| Image to Base64 (BFL) | Convert IMAGE to base64 (still available for original nodes) |

## Tests

```bash
cd tests && python -m pytest .
```

## Credits

- Original project: [gelasdev/ComfyUI-FLUX-BFL-API](https://github.com/gelasdev/ComfyUI-FLUX-BFL-API)
- Contributors: [@gelasdev](https://github.com/gelasdev), [@pleberer](https://github.com/pleberer), [@Duanyll](https://github.com/Duanyll)
