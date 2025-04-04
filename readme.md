# 工具说明

## 免责声明与风险提醒

**重要提示：本脚本可能存在误删除源代码内容的风险。请务必仔细阅读以下内容。**

本 Python 脚本旨在模仿 `isort` 的功能，用于对 C++ 源代码文件中的 `#include` 头文件进行排序。  
  
**但请注意，本脚本并非完善，功能可能存在缺陷（bugs）。**

**强烈建议您在使用本脚本之前，务必对您的 C++ 源代码进行完整备份。**

**使用本脚本所带来的任何风险和后果，包括但不限于：**

* **源代码内容被错误地修改或删除。**
* **代码编译失败或产生预期之外的行为。**
* **其他任何形式的数据损失或损坏。**

**均由使用者自行承担。**

**开发者不对因使用本脚本而造成的任何直接或间接损失承担任何责任。**

**您在使用本脚本时，应：**

* **充分理解脚本的功能和潜在风险。**
* **在测试环境或备份的源代码上进行充分测试。**
* **仔细检查脚本的输出结果，确保其符合您的预期。**
* **了解如何恢复您的源代码（例如，通过版本控制系统）。**

**如果您选择使用本脚本，即表示您已阅读、理解并同意本免责声明与风险提醒的所有内容。**

**请谨慎使用。**

## 工具说明

模仿python中的isort，对C++源代码中的头文件进行排序的脚本。排序依据，参与Google C++代码风格。用法如下：

```shell
python -u cpp_isort.py --src my_cpp.cpp --toml project.toml --dst my_cpp_out.cpp --encoding utf-8
```

project.toml参考python中的pyproject.toml，可以配置哪些头文件是第三方库，哪些头文件是本地库。

## 下载地址
我用pyinstaller编译了一个windows 64w位的exe，方便不熟悉python的同行使用。  
https://github.com/chuzhixing/isort/releases/download/v0.01/cpp_isort.zip  

不太方便登录github的，可以在百度网盘中下载：  
链接: https://pan.baidu.com/s/1-sJJi70yCLuGckCFSl3rxw?pwd=e95e 提取码: e95e  

## 效果演示

排序前：  

```c++
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

排序的效果演示：  

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

按照google C++代码风格，对头文件分为C 语言系统文件组、C++标准库的头文件组、其他库的头文件组（第三方库的头文件组）、本项目的头文件组。  
如果，某些头文件，在相应的头组中，不想排序，那么可以在该头文件后面加上如下注释：  

```c++
// isort:skip
```

同一组内，加上`isort:skip`注释的头文件，在相应的组中，保留原来的出现顺序，并且追加到相应组中的末尾。 这个可以参考演示demo中的`#include "aaaa.h"  // isort:skip`例子。    


某些头文件，在相应的头组中，不想排序，且想让它处于相应组的开头位置，那么可以在头文件后面加上如下注释： 

```c++
// isort:skip,top
```

这个，可以参考上面`#include "yyyy.h"  // isort:skip,top`与`#include "xxxx.h"  // isort:skip,top`的例子。

## cpp_isort.py
cpp_isort.py 对C++代码进行include排序，并自动处理`#if `内部的`#include `。  

conditional includes不进行排序，具体说明如下：  
如果有如下的，定义在`#if `内部的`#include `代码，手工把它放到其它所有的inclucde最后面。  
现有的逻辑是，遇到`#if `的行及后面的所有代码，均视为非include代码，不再对它们进行排序。  

```C++
#if MICRO_NAME
#include "openvinoSegNew.h"
#elif _WIN32
```

## 在vscode中使用该脚本 

Visual Studio Code 的Task（任务）文件可以被用来运行脚本或启动一个进程。  
许多现有的工具都可以通过Task直接在Visual Studio Code中运行，而不需要额外在命令行中输入命令。Task被配置在.vscode文件夹的tasks.json文件中。  

可以在vscode中，配置一个task。在源代码的页面，`run task`，会自动调用本地的python脚本对代码的头文件进行排序。

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run My Python Script, sort include",
            "type": "shell",
            "command": "D:\\xxxx\\Users\\Envs\\basic_p38\\Scripts\\python.exe",
            "args": [
                "D:\\xxxx\\cpp_isort.py",
                "--src",
                "${file}",
                "--toml",
                "D:\\xxxx\\project.toml",
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

## 参考文献
[1] https://blog.csdn.net/weixin_44814196/article/details/130607664  
