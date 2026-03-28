# monoframe

<p align="center">
  <img src="https://github.com/user-attachments/assets/db41b578-9b9b-4d6b-ab0c-6217ec6552ff" width="500">
</p>

A transparent window that applies real-time image processing to whatever is on your screen. 

Built for learning and experimenting with OpenCV.


## Installation

Requires [uv](https://github.com/astral-sh/uv).

```bash
git clone https://github.com/thigoai/monoframe
cd monoframe
uv sync
uv run src/main.py
```

Dependencies are declared in `pyproject.toml` and installed automatically by `uv`.

## 🗁 Project Structure
 
```
monoframe/
├── src/
│   ├── core/
│   │   ├── capturer.py       
│   │   ├── filters.py       
│   │   └── vision_engine.py 
│   └── ui/
│       ├── lens_widget.py    
│       └── main.py          
```
