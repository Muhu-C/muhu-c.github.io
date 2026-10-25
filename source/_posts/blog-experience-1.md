---
title: 记自己建立博客的曲折历程（一）
date: 2024-06-04 09:14:47
tags:
    - 成长之路
    - 经验
    - 教程
categories: 学习
cover: https://pic.mc118cn.cn/images/hexo.png
---

*本文章相比旧博客略有修改。该文章可能过时，请注意辨别。*  
*本文以 Windows 10 / Windows 11 + Git Bash 为例；Linux 用户可将 “Git Bash” 替换为系统终端，并注意不同系统的命令差异。*  
*建议 Node.js 20 LTS 或更高版本部署 Hexo。*  

## 前言

### 介绍

- **GitHub Pages** 是 GitHub 提供的静态网站托管服务，可以免费托管个人主页或项目站点。  
- **Hexo** 是一个快速、简洁的静态博客框架，主要使用 Markdown 写文章，并在几秒内生成静态网页，具有较好的自由度和个性化能力。  

### 提示

本教程会访问 GitHub、Node.js 等网站。如果你的网络无法稳定访问这些站点，请先准备好可用的网络环境，或使用 Watt Toolkit 等加速工具。

### 要求

1. 一台可联网的 Windows / Linux 计算机（建议 Windows 10 / Windows 11 / Linux）。  
2. 一个 GitHub 账号，或能够注册 GitHub 账号。  
3. 基本的命令行操作知识。  
4. 一定的英语和计算机基础知识。

## 第一步 创建 GitHub Pages 仓库

使用 Hexo 需要先安装必要软件：

- Git：[官网下载](https://git-scm.com/)  
- Node.js：[官网下载](http://nodejs.cn/)，建议安装 LTS 版本  

Windows 安装 Git 时，建议保留默认的 **Git Bash** 选项。

1. 打开 [GitHub](https://github.com/)，如果没有账号，先点击 **Sign up** 注册。  
2. 登录后，点击页面右上角的 **+** 图标，选择 **New repository**。  
3. **Repository name** 必须填写为：  
   `你的GitHub用户名.github.io`  
   例如用户名为 `example`，则仓库名为：`example.github.io`。  
4. 仓库类型建议选择 **Public**。  
5. 如果没有特殊需要，可以不初始化 README，保持空仓库。  
6. 点击 **Create repository** 完成创建。  

![新建仓库](https://pic.mc118cn.cn/images/blog-experience-1/0.png)

> 注意：个人博客仓库名必须严格遵循 `username.github.io` 规则，否则无法作为 GitHub 个人主页 / 博客站点使用。

## 第二步 配置 Git 与 SSH

在电脑中准备一个空文件夹，作为 Hexo 博客根目录。

在该文件夹中打开 **Git Bash**（Windows）或 **终端**（Linux），执行以下命令：

```Bash
git config --global user.name "你的 GitHub 用户名"
git config --global user.email "你的 GitHub 邮箱"
```

### 安装 Hexo CLI

```Bash
npm install -g hexo-cli
```

### 生成 SSH 密钥

推荐生成 Ed25519 密钥：

```Bash
ssh-keygen -t ed25519 -C "你的 GitHub 邮箱"
```

如果你的环境更习惯 RSA 密钥，也可以使用：

```Bash
ssh-keygen -t rsa -b 4096 -C "你的 GitHub 邮箱"
```

生成过程中如果提示输入路径或密码，建议直接回车使用默认值。

生成后，查看用户目录下的 `.ssh` 文件夹：

- 使用 Ed25519 时，公钥文件通常是 `id_ed25519.pub`。  
- 使用 RSA 时，公钥文件通常是 `id_rsa.pub`。  

复制公钥文件中的全部内容。

公钥格式通常类似：

```Text
ssh-ed25519 密钥字符... 你的 GitHub 邮箱
```

### 上传 SSH 公钥到 GitHub

打开 GitHub，进入：

**Settings -> SSH and GPG keys -> New SSH key**

- **Title**：自定义，例如 `My PC`  
- **Key type**：选择 **Authentication Key**  
- **Key**：粘贴刚才复制的公钥内容  

点击 **Add SSH key**。

### 验证 SSH

在 Git Bash 或终端中执行：

```Bash
ssh -T git@github.com
```

如果看到类似以下内容，说明 SSH 配置成功：

```Text
Hi 你的用户名! You've successfully authenticated, but GitHub does not provide shell access.
```

如果提示 `Connection closed by ... port 22`，说明 22 端口可能无法访问。可以尝试通过 443 端口连接：

```Bash
ssh -T -p 443 git@ssh.github.com
```

如果出现成功认证信息，说明可以使用 443 端口。

### 推荐：固定使用 443 端口

如果 443 端口可用，建议编辑 SSH 配置，让 `git@github.com` 自动走 443 端口。

创建或编辑：

```Bash
~/.ssh/config
```

写入：

```Bash
Host github.com
    HostName ssh.github.com
    Port 443
    User git
```

保存后再执行：

```Bash
ssh -T git@github.com
```

如果认证成功，后续部署会更稳定。

## 第三步 创建并配置 Hexo 博客

### 初始化 Hexo

在博客根目录中执行：

```Bash
hexo init
npm install
```

安装部署插件：

```Bash
npm install hexo-deployer-git
```

启动本地服务：

```Bash
hexo server
```

也可以简写为：

```Bash
hexo s
```

成功后，终端会显示本地访问地址，通常是：

```Text
http://localhost:4000/
```

在浏览器中打开该地址即可看到默认博客。

### 认识目录结构

Hexo 初始化后，根目录通常包含 `source` 和 `themes` 两个重要文件夹。

```Text
根目录/
├── source/
│   └── _posts/
│       └── hello-world.md
└── themes/
    └── landscape/
```

- `source/_posts`：用于存放 Markdown 文章。  
- `themes`：用于存放主题文件夹。  

一个完整主题通常包含 `_config.yml`、`layout`、`source` 等文件或文件夹。

### 修改站点基本配置

打开根目录中的 `_config.yml`。

找到 **Site** 部分，可以根据个人情况修改：

```YAML
# Site
title: 你的博客标题
subtitle: 你的博客副标题
author: 你的名字
language: zh-CN
timezone: 'Asia/Shanghai'
```

不同主题对 `language` 的要求可能略有差异，例如 `zh-CN`、`zh_CN`、`zh`。如果不确定，可以查看主题文档。

### 配置部署信息

在 GitHub 仓库页面中，点击 **Code -> Local -> SSH**，复制仓库 SSH 地址，例如：

```Text
git@github.com:你的用户名/你的用户名.github.io.git
```

![获取 SSH git](https://pic.mc118cn.cn/images/blog-experience-1/1.png)

回到 Hexo 根目录的 `_config.yml`，找到 **Deployment** 部分，配置如下：

```YAML
# Deployment
deploy:
  type: git
  repo: git@github.com:你的用户名/你的用户名.github.io.git
  branch: main
```

如果你的仓库默认分支是 `master`，则填写：

```YAML
  branch: master
```

部署完成后，请在 Github 仓库内 `Settings-Pages-Source` 将提交分支设为 `Source` 。  

### 更换主题

#### 方式一：直接下载主题（推荐新手）

在 [Hexo 主题站](https://hexo.io/themes/) 中选择喜欢的主题。

下载主题压缩包，解压后得到主题文件夹，将该文件夹放入：

```Text
根目录/themes/
```

放入后，根目录结构类似：

```Text
themes/
└── 主题文件夹名/
    ├── _config.yml
    ├── layout/
    ├── source/
    └── ...
```

打开 Hexo 根目录中的 `_config.yml`，将 `theme` 修改为主题文件夹名：

```YAML
theme: 主题文件夹名
```

然后重新启动本地服务：

```Bash
hexo server
```

如果主题有单独的配置文件，通常还需要修改：

```Text
根目录/themes/主题文件夹名/_config.yml
```

常见主题配置包括：

```YAML
language: zh-CN
menu:
  home: /
  tags: /tags/
  categories: /categories/
  archives: /archives/
```

具体配置项请以对应主题文档为准。

#### 方式二：通过 npm 安装主题（可选）

这里以 Solitude 主题为例：

```Bash
npm i hexo-theme-solitude
```

安装后，主题文件通常位于：

```Text
根目录/node_modules/hexo-theme-solitude
```

Hexo 默认从 `themes` 目录加载主题，因此通常还需要把主题复制或软链接到 `themes` 目录。

Windows Git Bash 中可以尝试：

```Bash
cp -r node_modules/hexo-theme-solitude themes/solitude
```

Linux / macOS 中可以使用：

```Bash
cp -r node_modules/hexo-theme-solitude themes/solitude
```

或者创建软链接：

```Bash
ln -s node_modules/hexo-theme-solitude themes/solitude
```

完成后，在 Hexo 根目录的 `_config.yml` 中修改：

```YAML
theme: solitude
```

> 对新手来说，直接下载主题源码放入 `themes` 更直观，也更不容易出错。

### 发布文章

使用以下命令新建文章：

```Bash
hexo new post "文章题目"
```

文章会生成在：

```Text
source/_posts/
```

打开生成的 `.md` 文件，你会看到类似以下内容：

```YAML
---
title: 文章标题
date: 2024-06-04 09:14:47
tags:
    - 标签 A
    - 标签 B
categories: 分类
cover: /images/cover.jpg
---
```

其中 `title`、`date`、`tags`、`categories`、`cover` 等字段统称为 **Front-matter**。不同主题支持的字段可能不同，具体以主题文档为准。

如果封面图片是本地图片，建议把图片放入 Hexo 静态资源目录，例如：

```Text
source/images/cover.jpg
```

然后填写相对路径：

```YAML
cover: /images/cover.jpg
```

如果封面图片是网络图片，也可以填写外链：

```YAML
cover: https://example.com/image.jpg
```

Front-matter 下方就可以使用 Markdown 语法编辑文章正文。

## 第四步 生成并部署网站

在 Hexo 根目录中执行：

```Bash
hexo generate
hexo deploy
```

或者合并为：

```Bash
hexo g -d
```

如果部署失败，可以先清理缓存再重新生成部署：

```Bash
hexo clean
hexo g -d
```

部署完成后，访问：

```Text
https://你的GitHub用户名.github.io/
```

即可看到你的博客。

## 常见问题

### 1. 本地可以访问，线上 404

检查以下几点：

- GitHub 仓库名是否为 `你的用户名.github.io`。  
- `deploy.branch` 是否与仓库实际分支一致，例如 `main` 或 `master`。  
- `deploy.repo` 是否复制正确。  
- `hexo g -d` 是否执行成功。  
- GitHub Pages 是否仍在构建中。

### 2. SSH 验证失败

检查：

- Git 用户名和邮箱是否配置正确。  
- 是否上传了正确的公钥。  
- 是否使用了正确的密钥文件。  
- 网络是否需要通过 443 端口访问 GitHub。

### 3. `hexo server` 启动失败

常见原因：

- Node.js 版本过低。  
- `npm install` 未完成。  
- 端口 4000 被占用。  
- 当前目录不是 Hexo 根目录。

可以尝试：

```Bash
hexo clean
npm install
hexo server
```

### 4. 主题样式丢失

检查：

- `theme` 字段是否填写正确。  
- 主题文件夹是否完整放入 `themes` 目录。  
- 是否修改了主题 `_config.yml` 中的资源路径。  
- 是否执行了 `hexo clean && hexo g`。

## 小结

到这里，一个基础的 Hexo 博客已经可以通过 GitHub Pages 发布。后续可以继续学习：

- 更换和深度配置主题。  
- 使用 GitHub Actions 自动部署。  
- 配置自定义域名。  
- 添加评论系统、搜索、RSS、统计等插件。
