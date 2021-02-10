# NUIST_HealthyReport
## NUIST健康打卡    By Infinity.

基于GitHub项目：https://github.com/dsus4wang/NUIST_AutoDailyHealthReport 大量修改而来，无需手动抓包修改FormData，操作更简单。

### 特别提醒

这里仅实现了健康日报的单次自动提交，一定程度上可以节约**身体健康的同学**填报健康日报的时间，但**请不要隐瞒自己的健康状况！**

**自动化不是不会写**，而是本着对他人负责的原则，**希望大家能够按照自己身体实际情况按需使用！**

如身体出现发热等情况，请**立即停止使用本项目**并**按实际情况手动**填写！**请务必对自己和他人负责！**

**因隐瞒自身健康状况导致的一切后果，本项目一概不负责！**

### 使用前

请将70行和71行的username和password分别修改为自己的学号和信息门户密码

```python
username = '请修改此处为学号'
password = '请修改此处为密码'
```

### Windows系统

系统需安装好Python3，pip

安装Python依赖PyExecJS、lxml、beautifulsoup4

```powershell
pip install PyExecJS lxml beautifulsoup4
```

CMD或者PowerShell进入目录

```powershell
cd E:\Desktop\DailyHealthReport
```

py运行run.py文件

```powershell
py run.py
```

请大家每天在确认自己身体健康之后再调用本项目，**务必对自己和他人负责！**

### 自动化填写

**强烈不建议自动化填写**，因此这里不提供任何自动化的方法

再次提醒：本项目不加自动化的原因，是本着对他人负责的原则，**希望大家能够按照自己身体实际情况按需使用！**

如身体出现发热等情况，请**立即停止使用本项目**并且**按实际情况手动**填写！**请务必对自己和他人负责！**

**因隐瞒自身健康状况导致的一切后果，本项目一概不负责！**

