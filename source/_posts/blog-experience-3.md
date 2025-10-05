---
title: 记自己建立博客的曲折历程（三）
date: 2025-10-01 21:17:07
tags: 
    - 成长之路
    - 教程
categories: 学习
cover: https://s21.ax1x.com/2025/10/01/pVTukcT.md.png
---
## 前言

### 提示  
- **本文有非常重要的内容：Umami 在静态网站上无中转直接读取 API 并显示数据**
- 此过程包含不少访问国外网站的要求，如无法访问，请使用 [Watt Toolkit](https://steampp.net/) 等加速软件。  
- 若有**公网 IP 服务器**，可以直接把 SSL 证书添加到 Nginx 反向代理中进行访问，详见 **第一步 配置 Nginx**  
- 本文章为 Solitude 主题的配置提供方法，因此从 Solitude 派生的其他主题都可使用此方法，若主题不是 Solitude 且没有内置的 Umami 统计显示，请自行修改网页代码！*（博主通过自己的文件、AI 以及其他教程摸索出了 Solitude 主题下的网站结构）*  
- 本文章与前一篇**记自己建立博客的曲折历程**有联系。
  
### 要求  
   
1. 一台可正常运行的 **Linux** 主机（以 Ubuntu 为例） 
2. 能访问 [Github](https://github.com/) 的网络 ( 可能需要 Watt Toolkit 等加速 )  
3. 一定的英语和 Linux 命令行知识储备   
4. 一个**自己的域名**  


## 第一步 使用 Nginx 把本地 Umami 进行反向代理

### 下载 Nginx

执行命令安装 Nginx (Ubuntu 方法)  
```Bash
sudo apt update
sudo apt upgrade
sudo apt install -y nginx
```

开启 Nginx
```Bash
sudo systemctl enable --now nginx
```

访问 `localhost:80`，若出现 ***Welcome to Nginx*** 字样，则表示安装成功  

### 配置 Nginx

编辑 `/etc/nginx/sites-enabled/default`
```Nginx 根据实际修改
server {
    # 你反向代理之后的最终网页端口，配置 Frp 时使用这个
    listen 80;

    # --------------!!!这一段文本如果使用 Frp 方案，请注释掉!!!--------------
    listen 443 ssl;  
    ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_certificate /路径/fullchain.pem;
    ssl_certificate_key /路径/privkey.pem;
    # --------------------------------------------------------------------

    server_name <umami-api.example.com(你的 Umami 网站域名)>;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

保存后重启 Nginx
```Bash
sudo systemctl restart nginx
```

## 第二步 获取 SSL 证书
若已经有证书 `fullchain.pem` 和 `privkey.pem` 可以跳过此步。  
这里使用 **Let's Encrypt (Certbot)** 方案，每 60 天内需要更新一次，本文章包括处理自动更新的方法。  

### 下载 Certbot

运行命令以安装 Certbot  

```Bash Ubuntu
sudo apt - get install certbot python3 - certbot - nginx
```

```Bash CentOS
sudo yum install epel - release -y
sudo yum install certbot -y
```

### 方案一 DNS

通过添加 DNS TXT 记录来证明域名所有权，支持通配符域名，无需服务器运行或开放端口，但需要有 DNS 控制权限。

输入命令
```Bash 根据实际修改
sudo certbot certonly --manual --preferred-challenges dns -d <umami-api.example.com(替换为你的域名)>
```
按步骤设置 DNS，需要比较好的网络条件

### 方案二 HTTP 检测本地（Frp 方案谨慎选择）

Let's Encrypt 会要求在网站指定路径下创建一个特定文件，然后通过访问该文件来验证域名控制权。

{% note 'warn' 'fas fa-triangle-exclamation' %}
需要服务器开放 80 端口到公网！使用 Frp 的用户不建议选择此方案。
{% endnote %}

输入命令
```Bash 根据实际修改
# 关闭 Nginx 以防端口被占用
sudo systemctl stop nginx
# 获取 SSL 证书
sudo certbot --nginx -d <umami-api.example.com(替换为你的域名)>
```

### 设置 Certbot 自动续期

创建 Certbot 定时服务
```Bash
sudo nano /etc/systemd/system/certbot-renew.service
```

编辑文件（尖括号内根据实际修改）  
```ini 根据实际修改
[Unit]
Description=Certbot automatic renewal service
After=network.target

[Service]
Type=oneshot
# 执行证书更新（--renew-hook指定更新后执行的命令）
ExecStart=/usr/bin/certbot renew --quiet --renew-hook "/bin/systemctl restart frp.service"
# 赋予证书证书权限（关键：解决FRP读取权限问题）
ExecStartPost=/bin/chmod 755 /etc/letsencrypt
ExecStartPost=/bin/chgrp root /etc/letsencrypt
ExecStartPost=/bin/chmod 750 /etc/letsencrypt/live /etc/letsencrypt/archive
ExecStartPost=/bin/chgrp <你的用户名> /etc/letsencrypt/live /etc/letsencrypt/archive
ExecStartPost=/bin/chmod 750 /etc/letsencrypt/live/<你的 API 地址> /etc/letsencrypt/archive/<你的 API 地址>
ExecStartPost=/bin/chgrp -R <你的用户名> /etc/letsencrypt/live/<你的 API 地址> /etc/letsencrypt/archive/<你的 API 地址>
ExecStartPost=/bin/chmod 640 /etc/letsencrypt/live/<你的 API 地址>/* /etc/letsencrypt/archive/<你的 API 地址>/*
ExecStartPost=/bin/systemctl restart frp.service
```

创建定时器
```Bash
sudo nano /etc/systemd/system/certbot-renew.timer
```

编辑文件（根据实际修改）
```ini 根据实际修改
[Unit]
Description=Run Certbot every 5 months

[Timer]
# 首次运行延迟 10 分钟
OnBootSec=10min
# 之后每 50 天运行一次
OnUnitActiveSec=50d
# 允许 1 天误差，避免系统时钟精确对齐
AccuracySec=1d

[Install]
WantedBy=timers.target
```

启动 Certbot 自动更新
```Bash
sudo systemctl enable --now certbot-renew.timer
```

测试
```Bash
# 手动触发一次证书更新
sudo systemctl start certbot-renew.service
# 查看执行日志，确认无错误
sudo journalctl -u certbot-renew.service -f
```

{% note 'warn' 'fas fa-triangle-exclamation' %}
注意：关闭、重启 Certbot 服务都选择 certbot-renew.timer，而不是 certbot-renew.service！
{% endnote %}

## 第三步 使用 Nginx 反向代理到外网

### 方案一 Frp

在 Frp 服务端（商）配置内网穿透，协议为 HTTPS，内网端口为上文 Nginx 配置中提示的端口，检查是否有 https2http 字段。在 https2http 字段下配置

```ini 根据实际修改
plugin_crt_path = fullchain.pem # 证书文件的路径
plugin_key_path = privkey.pem # 私钥文件的路径
```

完成服务端（商）配置后，按照要求绑定域名  

配置 Frp 服务并自动随 Certbot 更新而更新   

```Bash
sudo nano /etc/systemd/system/frp.service
```

编辑文件（尖括号内根据实际修改）
```ini 根据实际修改
[Unit]
Description=FRP Client Service
After=network.target

[Service]
# 关键：使用有权限访问证书的用户（非root也可，需确保证书权限正确）
User=<你的用户名>
Group=<你的用户名>
# 启动FRP客户端（替换为实际路径）
ExecStart=/<地址>/frpc -c /<地址>/frpc.ini
# 自动重启（崩溃或证书更新后）
Restart=always
RestartSec=5
# 环境变量（可选，如需指定证书路径）
Environment="SSL_CERT_DIR=/etc/letsencrypt/live/"

[Install]
WantedBy=multi-user.target
```

启用 Frp 并设置开机启动
```Bash
sudo systemctl enable --now frp.service
```


### 方案二 公网

不注释并按情况修改 Nginx 配置中的文本
```Nginx
    listen 443 ssl;  
    ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_certificate /路径/fullchain.pem;
    ssl_certificate_key /路径/privkey.pem;
```

注释掉 Nginx 配置中的文本
```Nginx
    listen 80;
```

按照自己的情况，将公网 IP 连接到自己的域名

## 第四步 处理 Umami API 并应用

以下步骤均为 Solitude 主题环境！  
回到 Hexo 所在电脑

### 配置并处理问题
由于 Solitude 在 Umami 加载失败时不显示该块内容，我们在这里添加**错误提示**与**正在加载**的功能  

更改 `<主题文件夹>\layout\includes\widgets\page\about\other.pug` 中的 `when 'custom'` 字段，可以根据后文 **常用 Javascript 时间段获取** 自行修改

```js Hexo pug
                    when 'umami'
                        script.
                            // Umami 配置
                            const umamiConfig = {
                                url: '#{tj.umami.url || ""}',
                                websiteId: '#{tj.umami.website_id || ""}',
                                authToken: '#{tj.umami.auth_token || ""}'
                            };

                            function getTimestamp(date) {
                                return date.getTime();
                            }

                            function formatUmamiUrl(url) {
                                return url.endsWith('/') ? url : url + '/';
                            }

                            (function() {
                                'use strict';
                                
                                let umamiInitialized = false;
                                
                                // 获取 Umami 数据
                                async function fetchUmamiData() {
                                    try {
                                        const baseUrl = formatUmamiUrl(umamiConfig.url);
                                        
                                        // 检查配置是否完整
                                        if (!umamiConfig.url || !umamiConfig.websiteId || !umamiConfig.authToken) {
                                            throw new Error('错误: Umami 配置不完整，请检查 _config.yml 中的 umami 设置。');
                                        }

                                        // 计算各个时间段
                                        const now = new Date();
                                        const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());

                                        // 昨日时间范围
                                        const yesterdayStart = new Date(todayStart);
                                        yesterdayStart.setDate(yesterdayStart.getDate() - 1);
                                        const yesterdayEnd = new Date(todayStart);
                                        yesterdayEnd.setMilliseconds(yesterdayEnd.getMilliseconds() - 1);

                                        // 30 天内时间范围
                                        const thirtyDaysAgo = new Date(now);
                                        thirtyDaysAgo.setDate(now.getDate() - 30);

                                        // 今年时间范围
                                        const yearlyStart = new Date(now.getFullYear(), 0, 1);

                                        // 自建站以来的时间范围
                                        const totalStart = new Date(2024, 5, 2);

                                        // 获取所有数据
                                        const [todayRes, yesterdayRes, thirtyDaysRes, yearlyRes, totalRes] = await Promise.all([
                                            // 今日数据
                                            fetch(`${baseUrl}api/websites/${umamiConfig.websiteId}/stats?` + new URLSearchParams({
                                                startAt: getTimestamp(todayStart),
                                                endAt: getTimestamp(now)
                                            }), { 
                                                headers: { 'Authorization': `Bearer ${umamiConfig.authToken}` },
                                                timeout: 10000 
                                            }).then(res => res.json()),
                                            
                                            // 昨日数据
                                            fetch(`${baseUrl}api/websites/${umamiConfig.websiteId}/stats?` + new URLSearchParams({
                                                startAt: getTimestamp(yesterdayStart),
                                                endAt: getTimestamp(yesterdayEnd)
                                            }), { 
                                                headers: { 'Authorization': `Bearer ${umamiConfig.authToken}` },
                                                timeout: 10000 
                                            }).then(res => res.json()),
                                            
                                            // 30 天内数据
                                            fetch(`${baseUrl}api/websites/${umamiConfig.websiteId}/stats?` + new URLSearchParams({
                                                startAt: getTimestamp(thirtyDaysAgo),
                                                endAt: getTimestamp(now)
                                            }), { 
                                                headers: { 'Authorization': `Bearer ${umamiConfig.authToken}` },
                                                timeout: 10000 
                                            }).then(res => res.json()),
                                            
                                            // 今年数据
                                            fetch(`${baseUrl}api/websites/${umamiConfig.websiteId}/stats?` + new URLSearchParams({
                                                startAt: getTimestamp(yearlyStart),
                                                endAt: getTimestamp(now)
                                            }), { 
                                                headers: { 'Authorization': `Bearer ${umamiConfig.authToken}` },
                                                timeout: 10000 
                                            }).then(res => res.json()),

                                            // 全部数据
                                            fetch(`${baseUrl}api/websites/${umamiConfig.websiteId}/stats?` + new URLSearchParams({
                                                startAt: getTimestamp(totalStart),
                                                endAt: getTimestamp(now)
                                            }), { 
                                                headers: { 'Authorization': `Bearer ${umamiConfig.authToken}` },
                                                timeout: 10000 
                                            }).then(res => res.json())
                                        ]);

                                        // 处理数据
                                        const statsData = {
                                            today_uv: todayRes.visitors?.value || 0,
                                            today_pv: todayRes.pageviews?.value || 0,
                                            yesterday_uv: yesterdayRes.visitors?.value || 0,
                                            thirty_days_pv: thirtyDaysRes.pageviews?.value || 0,
                                            yearly_pv: yearlyRes.pageviews?.value || 0,
                                            total_pv: totalRes.pageviews?.value || 0
                                        };

                                        updateStatistics(statsData);
                                        
                                    } catch (error) {
                                        console.error('获取 Umami 数据失败: ', error);
                                        showError(error.message);
                                    }
                                }

                                // 统计显示
                                function updateStatistics(data) {
                                    const title = {
                                        "today_uv": "今日人数", 
                                        "today_pv": "今日访问", 
                                        "yesterday_uv": "昨日人数", 
                                        "thirty_days_pv": "30 天访问", 
                                        "yearly_pv": "今年访问", 
                                        "total_pv": "总访问数"
                                    };

                                    const s = document.getElementById("statistic");
                                    let html = '';

                                    for (let key in data) {
                                        if (data.hasOwnProperty(key) && title[key]) {
                                            html += `<div><span>${title[key]}</span><span id="${key}">${data[key]}</span></div>`;
                                        }
                                    }

                                    s.innerHTML = html;
                                }

                                // 显示错误信息
                                function showError(message) {
                                    const s = document.getElementById("statistic");
                                    s.innerHTML = '<div class="statistic-error">统计信息暂时不可用<br><small>请检查网络连接或查看控制台</small><small>若出现问题请联系博主</small></div>';
                                }

                                function showLoading() {
                                    const s = document.getElementById("statistic");
                                    if (s) {
                                        s.innerHTML = '<div class="statistic-loading">统计信息正在加载中<br><small>请稍后...</small></div>';
                                    }
                                }

                                function initUmamiStats() {
                                    if (umamiInitialized) return;
                                    
                                    const statisticElement = document.getElementById('statistic');
                                    if (!statisticElement) {
                                        console.log('统计元素未找到，等待重试...');
                                        setTimeout(initUmamiStats, 100);
                                        return;
                                    }
                                    
                                    umamiInitialized = true;
                                    console.log('Solitude 主题下初始化 Umami 统计');
                                    
                                    showLoading();
                                    fetchUmamiData();
                                }

                                if (typeof window.refreshFn !== 'undefined') {
                                    const originalRefreshFn = window.refreshFn;
                                    window.refreshFn = function() {
                                        if (typeof originalRefreshFn === 'function') {
                                            originalRefreshFn();
                                        }
                                        setTimeout(initUmamiStats, 300);
                                    };
                                }

                                document.addEventListener('DOMContentLoaded', function() {
                                    setTimeout(initUmamiStats, 500);
                                });

                                window.addEventListener('load', function() {
                                    if (!umamiInitialized) {
                                        initUmamiStats();
                                    }
                                });
                            })();
```

在 `<博客根目录>\source\_data\about.yml` 中添加以下字段

```YAML 根据实际修改
# 网站统计数据展示模块
tj: # 统计
  provider: umami # 51la / umami / custom
  img: https://s21.ax1x.com/2025/09/14/pVWzPPK.jpg # 背景根据自己情况设置
  desc: 使用自建统计 # 提示
  # Umami 统计
  umami:
    url: "https://umami-api.example.com"  # 你的 Umami 实例 URL 根目录
    website_id: "<ID>"  # 你的网站 ID
    # 你的认证令牌
    auth_token: "<token>"
```

在 `<主题文件夹>\source\css\_page\_about\statistic.styl` 中的 `#statistic` 中添加以下字段

```stylus 根据实际修改
.statistic-error
        margin-top: 15px
        width: 100%
        display: flex
        align-items: center
        justify-content: center
        flex-direction: column
        text-align: center
        color: #ff6b6b
        font-weight: bold
        font-size: 20px
        padding: 40px 20px
        background: rgba(255, 107, 107, 0.1)
        border-radius: 12px
        border: 2px dashed rgba(255, 107, 107, 0.3)
        
        small
            display: block
            margin-top: 4px
            line-height: 1.2
            font-size: 15px
            color: rgba(255, 107, 107, 0.8)
            font-weight: normal
        
      .statistic-loading
        margin-top: 15px
        width: 100%
        display: flex
        align-items: center
        justify-content: center
        flex-direction: column
        text-align: center
        color: #28b
        font-weight: bold
        font-size: 20px
        padding: 40px 20px
        background: rgba(20, 109, 200, 0.1)
        border-radius: 12px
        border: 2px dashed rgba(34, 102, 200, 0.3)
        
        small
            display: block
            margin-top: 4px
            line-height: 1.2
            font-size: 15px
            color: rgba(64, 132, 200, 0.8)
            font-weight: normal
```

重启 Hexo ，访问本地网页，检查是否正常

### 常用 Javascript 时间段获取
- 基础日期获取  
```JS
const now = new Date(); // 当前时间

// 获取各个时间组件
const year = now.getFullYear();        // 2024
const month = now.getMonth();          // 0-11 (0=一月)
const date = now.getDate();            // 1-31
const day = now.getDay();              // 0-6 (0=周日)
const hours = now.getHours();          // 0-23
const minutes = now.getMinutes();      // 0-59
const seconds = now.getSeconds();      // 0-59
const milliseconds = now.getMilliseconds(); // 0-999
```
- 常用时间范围
```JS
const now = new Date();

// 今天开始时间 (00:00:00)
const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());

// 今天结束时间 (23:59:59.999)
const todayEnd = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999);

// 昨天开始时间
const yesterdayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1);

// 昨天结束时间
const yesterdayEnd = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1, 23, 59, 59, 999);

// 明天开始时间
const tomorrowStart = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
```

- 本周相关
```JS
const now = new Date();
const dayOfWeek = now.getDay(); // 0=周日, 1=周一, ..., 6=周六

// 本周第一天 (周日)
const weekStart = new Date(now);
weekStart.setDate(now.getDate() - dayOfWeek);
weekStart.setHours(0, 0, 0, 0);

// 本周最后一天 (周六)
const weekEnd = new Date(weekStart);
weekEnd.setDate(weekStart.getDate() + 6);
weekEnd.setHours(23, 59, 59, 999);

// 本周周一
const monday = new Date(now);
monday.setDate(now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1));
monday.setHours(0, 0, 0, 0);
```
- 本月相关
```JS
const now = new Date();

// 本月第一天
const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);

// 本月最后一天
const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0);
monthEnd.setHours(23, 59, 59, 999);

// 上个月第一天
const lastMonthStart = new Date(now.getFullYear(), now.getMonth() - 1, 1);

// 下个月第一天
const nextMonthStart = new Date(now.getFullYear(), now.getMonth() + 1, 1);
```
- 今年相关
```JS
const now = new Date();

// 今年第一天
const yearStart = new Date(now.getFullYear(), 0, 1); // 1月1日

// 今年最后一天
const yearEnd = new Date(now.getFullYear(), 11, 31); // 12月31日
yearEnd.setHours(23, 59, 59, 999);

// 去年第一天
const lastYearStart = new Date(now.getFullYear() - 1, 0, 1);

// 明年第一天
const nextYearStart = new Date(now.getFullYear() + 1, 0, 1);
```
- 相对时间计算
```JS
const now = new Date();

// 30天前
const thirtyDaysAgo = new Date(now);
thirtyDaysAgo.setDate(now.getDate() - 30);

// 7天后
const sevenDaysLater = new Date(now);
sevenDaysLater.setDate(now.getDate() + 7);

// 3小时前
const threeHoursAgo = new Date(now);
threeHoursAgo.setHours(now.getHours() - 3);

// 15分钟后
const fifteenMinutesLater = new Date(now);
fifteenMinutesLater.setMinutes(now.getMinutes() + 15);
```
- 格式化日期函数
```JS
function formatDate(date, format = 'YYYY-MM-DD') {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

// 使用示例
console.log(formatDate(now)); // "2024-01-15"
console.log(formatDate(now, 'YYYY年MM月DD日 HH:mm:ss')); // "2024年01月15日 14:30:25"
```
- 时间戳转换
```JS
// 获取时间戳（毫秒）
const timestamp = now.getTime(); // 1705311025000

// 时间戳转Date对象
const dateFromTimestamp = new Date(1705311025000);

// 获取Unix时间戳（秒）
const unixTimestamp = Math.floor(now.getTime() / 1000); // 1705311025
```
- 日期比较
```JS
const date1 = new Date(2024, 0, 15);
const date2 = new Date(2024, 0, 20);

// 比较日期
console.log(date1 < date2); // true
console.log(date1 > date2); // false

// 计算日期差（天数）
const diffTime = Math.abs(date2 - date1);
const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); // 5
```