---
title: 关于本网站的 Solitude 主题
date: 2025-10-05 11:53:16
tags:
  - Hexo
  - Solitude
  - 编程
categories:
  - 编程
cover: https://cnb.cool/muhu-group/tuc/-/git/raw/main/solitude.jpg
---

## 写在开头  
本网站的 Solitude 主题经过了修改。    
MuhuTheme 主题是我根据原有的 Solitude 主题二次修改后发布的主题。  

## 作出的修改

### 一、根据 [@ 星港 Star](https://blog.starsharbor.com/) 的魔改修复部分问题

Github: [commit *3d8adb3* & *165474e*](https://github.com/Muhu-C/MuhuTheme/commit/165474ec1b709f161894835cb8a889f1579b0d10)  

### 二、添加侧边栏日历

Github: [commit 6ccc164](https://github.com/Muhu-C/MuhuTheme/commit/6ccc1649a35b09ce4e1e1a2a720ba4ba6d1a8267)  

![日历](https://cnb.cool/muhu-group/tuc/-/git/raw/main/solitude-changes/0.png)  

### 三、修复主页宽度变化时发生的样式 Bug 并优化主页 home-top 按钮显示

Github: commit   
- [b7f42fd](https://github.com/Muhu-C/MuhuTheme/commit/b7f42fdacb7f1bfc47fba12d2086313083f92513)  
- [9cbe3c2](https://github.com/Muhu-C/MuhuTheme/commit/9cbe3c269cb3bf8d1478dd96ed7554a3e6cd0a0c)  
- [f03eb78](https://github.com/Muhu-C/MuhuTheme/commit/f03eb78e4c508b844bdc47c5b1738baea1d21dfd) 怎么还有二次修改？因为第一次修改后 bug 更严重了（  

{% tabs 主页修改项目, 0 %} 

<!-- tab 样式 Bug @fas fa-tag -->

| 修复前（一瞬间出现的 Bug） | 修复后 |
| -----  | ----- |
| ![Bug 高度异常](https://cnb.cool/muhu-group/tuc/-/git/raw/main/solitude-changes/1.png) | ![修复后](https://cnb.cool/muhu-group/tuc/-/git/raw/main/solitude-changes/2.png) |

<!-- endtab -->
<!-- tab 布局优化 @fas fa-tag -->

![布局优化](https://cnb.cool/muhu-group/tuc/-/git/raw/main/solitude-changes/3.png)

<!-- endtab -->
{% endtabs %}

### 优化 Swiper 问题

Github: commit  
- [3d8adb3](https://github.com/Muhu-C/MuhuTheme/commit/3d8adb3e7bc80c38293d7129a3d41b7f097dcdda)  
- [6ccc164](https://github.com/Muhu-C/MuhuTheme/commit/6ccc1649a35b09ce4e1e1a2a720ba4ba6d1a8267)  

### 修复在系统默认主题下右击菜单显示错误的问题

Github: [commit a8cd2da](https://github.com/Muhu-C/MuhuTheme/commit/a8cd2dad13c9399fcc7658c3ab3867dd1275d128)  

| 修复前 | 修复后 |
| -----  | ----- |
| ![Bug 右键菜单异常](https://cnb.cool/muhu-group/tuc/-/git/raw/main/solitude-changes/4.png) | ![修复后](https://cnb.cool/muhu-group/tuc/-/git/raw/main/solitude-changes/5.png) |

### 添加是否在主页显示即刻短文的功能

Github: [commit a8cd2da](https://github.com/Muhu-C/MuhuTheme/commit/a8cd2dad13c9399fcc7658c3ab3867dd1275d128)  

![功能展示](https://cnb.cool/muhu-group/tuc/-/git/raw/main/solitude-changes/6.png)

### 修复特定情况下文章页面中，标题块底部覆盖顶栏的问题  
  
Github: commit  
- [32cf81f](https://github.com/Muhu-C/MuhuTheme/commit/32cf81f97900124f5d17ec3fda6d4a35d04d27b0)  
- [06ef3b0](https://github.com/Muhu-C/MuhuTheme/commit/06ef3b0c2c44a09f546ed8c51e70873fdfd8ab18)  
  
若有其他功能建议以及浏览中的问题，希望大家及时提议或指出。  