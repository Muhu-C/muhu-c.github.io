---
title: 折腾 Umami
tags:
  - 教程
  - 经验
  - Hexo
categories:
  - 教程
cover: https://free.picui.cn/free/2025/10/05/68e22b661535b.jpg
date: 2025-10-05 16:26:00
---


## 缘由
起初，我在我家里的小服务器部署 Umami 并将网站用 Frp 公布到公网。但一看访问情况，实在是惨不忍睹。  
{% spoiler 'blur' '为啥它是小服务器？因为它的确小，是 HP Elitedesk 800 G2 DM' %}  

## 第一步 配置 Netlify 上的 Umami （只告诉注意事项）
由于我以前有一个丢弃的 **Neon 数据库**用于存放 Umami 的数据，*我想把它放到服务商。脑海中浮现的第一个想法便是 Netlify。*  
*Github 仓库建了又拆，折腾了一晚上*，发现启动命令的 `yarn run build` 需要在**第一次部署前**配置好。
最后，成功建立了一个 Netlify 部署的 Umami 项目。  
![项目状态](https://free.picui.cn/free/2025/10/05/68e22f8831e4d.png)  

## 第二步 配置 Vercel 上的 Umami （只告诉注意事项）
*然而多疑的我，没有完成这次配置。*  
又测速了一次网站，发现国内的地区没有覆盖得这么好，于是开始找起其他项目，最终目光聚焦在了 Vercel 上。  
*Vercel 不是国内不能访问吗？*    
不一定，把 Vercel 网页项目**绑定到自己的域名**即可。  
![绑定域名](https://free.picui.cn/free/2025/10/05/68e2303c8c946.png)  

*又折腾一会，把 Vercel 上的 Umami 也部署了，安上自己的域名，配置好网站，开始干其他事了。*  

## 第三步 资源的充分利用
*不对。  
我突然想起了这些网站是有免费额度的*，回头一看，**4 小时**的 CPU 活跃时间。  
![限制](https://free.picui.cn/free/2025/10/05/68e2326682e35.png)
再看使用情况。才没五次刷新，就用了七秒钟了。根据测量，其中**读取统计结果**要用的时间占了绝大多数。  
![Vercel 使用情况](https://free.picui.cn/free/2025/10/05/68e23206df568.png)
回来看 Netlify，发现我用的是 **Legacy 计划**，资源还挺充足的  
![Netlify 使用情况及 Legacy 计划下的限制](https://free.picui.cn/free/2025/10/05/68e232f7201dc.png)
{% note 'warn' 'fas fa-triangle-exclamation' %}
自 2025 年 9 月 4 日以来，Netlify 更改了新登录用户所使用的策略，资源变得紧张，因此新 Netlify 用户谨慎选择方案。
{% endnote %}
*那我就把网站连上 Netlify 部署的 Umami 吧。
但是，Vercel 的访问速度还挺快，总不能浪费吧。*
**于是我想出了一个方法。** 由于我的 Vercel 与 Netlify 的项目使用同一个 Neon 数据库，我可以将它们分别用于 **对应的功能**。列出一个表格  

| 特征 | Netlify | Vercel |
| :--: | :-----: | :----: |
| 国内访问速度 | 较慢，小部分地区有时不可访问 | 较快，基本所有地区可访问 |
| 资源 | 若使用 Legacy 计划，资源较为充足 | 资源较为紧张 | 

最终得到方案：

| 特征 | Netlify | Vercel |
| :--: | :-----: | :----: |
| 国内访问速度 | 较慢，小部分地区有时不可访问 | 较快，基本所有地区可访问 |
| 资源 | 若使用 Legacy 计划，资源较为充足 | 资源较为紧张 | 
| 使用方式 | Umami 统计信息显示 | Umami 统计 |

至此，该问题在以免费为基础的情况下解决。
若有其他以免费为前提的、更好的建议，欢迎大家来评论区探讨。