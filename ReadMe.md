

> [!Warning]
> this repo is **no longer maintained**, and may not able to work as designed. But you can still refer to the implementation and create your own project.
> 
> 这个项目已经**停止维护**, ~~可能~~无法完成预设功能. 本项目代码仅供参考(电子骨灰盒, 留念😭)

Although not recommended, if you still want to try it out, you may follow the code logic and modify the corresponding paths of the web elements according to the current webpage at https://xk.nju.edu.cn.

尽管不推荐这么做(因为费时费力, 同时也不一定能work), 如果你仍然想尝试正常运行这份代码, 你可能需要根据现在的选课网页(的元素布局), 参考本项目的代码逻辑, 对抓取的相应网页元素的路径进行修改. 

# Automatic Course Selector 选课平台补选抢课器

## Intro 

### Why do we need this application?

设计这个项目的初衷是为了更方便的进行补选的抢课. 鄙校的补选抢课方式是不太人性化的, 虽说先到先得是公平的举措, 但是名额放出的时间却是随机的,
因此对于部分比较热门的课程, 往往白天时不时就登录平台看一看有没有空余名额, 甚至半夜起来看.

然而蹲补选实际上是比较重复单调的过程: 登录系统, 看看有没有刷新出课程名额, 有的话就抢.

既然如此, 本人就开发了该自动化抢课软件, 以解放人力.

### What can we do with it?

- 实时查看当前的课程状态(已选课程/收藏课程)
- 自动化抢课

## features & plans
### feathers implemented
- 基于`selenium`的网络资源爬取 & 自动化操作
- 基于`超级鹰验证码识别api`的模拟登录
- 基于`PySide2`的GUI界面设计

### project plans
- `v0.5` 实现模拟登录 基本抢课功能
- `v0.6` 实现课程查看功能
- `v0.7` 实现GUI界面设计
- `v1.0` 实现全部预设功能

## modules design

### 功能介绍

- 我的课程信息: 查看当前已经选中的课程, 并形成可视化表格展示

- 输入需要抢的课程, 软件进行自动循环抢课, 知道抢中或取消

- [TODO]支持导入抢课名单(即输入检索的要求), 会循环进行检索


## How to use

> 如有问题, 欢迎联系作者

1. clone项目到本地
2. 登录"超级鹰"平台, 创建账号, 购买题分(用于验证码识别API服务)
3. 修改`crawl.py`文件
   1. 修改自己的学号/登录选课系统的密码
   2. 修改超级鹰API的参数
4. 配置编译运行环境(作者为`Anaconda(python 3.9)` + `Pycharm`
5. 编译运行.


