
# Tool Description

## Video explanation
Bilibili video link: https://www.bilibili.com/video/BV1bRZdYdE4i/   


## Disclaimer and Risk Warning

**Important Notice: This script may carry the risk of unintentionally deleting source code content. Please read the following carefully.**

This Python script aims to mimic the functionality of `isort` for sorting `#include` header files in C++ source code files.   
  
**However, please be aware that this script is not perfect, and its functionality may contain defects (bugs).**

**You are strongly advised to make a complete backup of your C++ source code before using this script.**

**Any risks and consequences arising from the use of this script, including but not limited to:**

* **Source code content being incorrectly modified or deleted.**
* **Code compilation failures or unexpected behavior.**
* **Any other form of data loss or damage.**

**are solely the responsibility of the user.**

**The developer assumes no responsibility for any direct or indirect loss caused by the use of this script.**

**When using this script, you should:**

* **Fully understand the script's functionality and potential risks.**
* **Thoroughly test the script in a testing environment or on backed-up source code.**
* **Carefully review the script's output to ensure it meets your expectations.**
* **Understand how to restore your source code (e.g., through a version control system).**

**By choosing to use this script, you indicate that you have read, understood, and agree to all the contents of this disclaimer and risk warning.**

**Please use with caution.**

## Tool Description

A script that mimics `isort` in Python to sort `#include` header files in C++ source code. The sorting is based on the Google C++ Style Guide. Usage is as follows:

```shell
python -u cpp_isort.py --src my_cpp.cpp --toml project.toml --dst my_cpp_out.cpp --encoding utf-8
```

Or use the packaged exe:
```shell
cpp_isort.exe --src my_cpp.cpp --toml project.toml --dst my_cpp_out.cpp --encoding utf-8
```

`project.toml` refers to `pyproject.toml` in Python and can configure which header files are third-party libraries and which are local libraries.

## Download link
I compiled a Windows 64w bit exe using pyinstaller, which is convenient for colleagues who are not familiar with Python to use.  
https://github.com/chuzhixing/isort/releases/download/v0.01/cpp_isort.zip   

For those who are not very convenient to log in to GitHub, you can download it from Baidu Netdisk:  
Link: https://pan.baidu.com/s/1-sJJi70yCLuGckCFSl3rxw?pwd=e95e Extract code: e95e  

## Installation instructions
```shell
pip install -r requirements.txt
```

## Effect Demonstration

Before sorting:

```C++
#include "yyyy.h"  // isort:skip,top
#include "xxxx.h"  // isort:skip,top
#include "aaaa.h"  // isort:skip
#include "my_global.h"
#include "test_visualizer.hpp"

#include <opencv2/opencv.hpp>
#include "predictor/yolov8_onnx.h"
#include "pystring.h"
#include "argparse.hpp"
#include <fmt/core.h>
#include <opencv2/imgproc/types_c.h>  // NOLINT

#include <sstream>
#include <string>
#include <vector>
#include <cmath>
#include <filesystem>
#include <iostream>
```

Effect after sorting:

```c++
#include <cmath>
#include <filesystem>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "argparse.hpp"
#include "pystring.h"
#include <fmt/core.h>
#include <opencv2/imgproc/types_c.h>  // NOLINT
#include <opencv2/opencv.hpp>

#include "yyyy.h"  // isort:skip,top
#include "xxxx.h"  // isort:skip,top
#include "my_global.h"
#include "predictor/yolov8_onnx.h"
#include "test_visualizer.hpp"
#include "aaaa.h"  // isort:skip
```

According to the Google C++ Style Guide, header files are divided into the following groups: C language system files, C++ standard library header files, other library header files (third-party library header files), and project header files.

If you do not want certain header files to be sorted within their respective groups, you can add the following comment after the header file:

```c++
// isort:skip
```
Header files with the `isort:skip` comment within the same group will retain their original order of appearance within that group and will be appended to the end of the respective group. Refer to the `#include "aaaa.h"  // isort:skip` example in the demonstration.

If you do not want certain header files to be sorted within their respective groups and want them to be at the beginning of the respective group, you can add the following comment after the header file:
```c++
// isort:skip,top
```

Refer to the examples of `#include "yyyy.h"  // isort:skip,top` and `#include "xxxx.h"  // isort:skip,top` above.

## cpp_isort.py

`cpp_isort.py` sorts includes in C++ code and automatically handles `#include` directives within `#if` blocks.

Conditional includes are not sorted. Specific details are as follows:

If you have `#include` code defined within `#if` blocks like the following, manually place it after all other includes.

The current logic treats any line starting with `#if` and all subsequent code as non-include code and will no longer sort them.

```C++
#if MICRO_NAME
#include "openvinoSegNew.h"
#elif _WIN32
```

## Using the Script in VS Code
Visual Studio Code Tasks can be used to run scripts or launch processes.  

Many existing tools can be run directly within Visual Studio Code through Tasks, without needing to enter commands in the command line separately. Tasks are configured in the tasks.json file located in the .vscode folder.  

You can configure a task in VS Code. On the source code page, `Run Task` will automatically call the local Python script to sort the header files of the code.

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run My Python Script, sort include by python",
            "type": "shell",
            "command": "D:\\workon\\dev\\Scripts\\python.exe",
            "args": [
                "E:\\PythonWorkspaceSet\\git_or_gitee\\isort\\cpp_isort.py",
                "--src",
                "${file}",
                "--toml",
                "E:\\PythonWorkspaceSet\\git_or_gitee\\isort\\project.toml",
                "--dst",
                "${file}"
            ],
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            }
        },
        {
            "label": "Run My Python Script, sort include by exe",
            "type": "shell",
            "command": "E:\\PythonWorkspaceSet\\git_or_gitee\\isort\\dist\\cpp_isort\\cpp_isort.exe",
            "args": [
                "--src",
                "${file}",
                "--toml",
                "E:\\PythonWorkspaceSet\\git_or_gitee\\isort\\project.toml",
                "--dst",
                "${file}"
            ],
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": false
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            }
        }
    ]
}
```
## reference
[1] https://blog.csdn.net/weixin_44814196/article/details/130607664  
