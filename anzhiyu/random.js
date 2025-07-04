var posts=["2024/06/04/如何建立自己的博客(旧博客)/","2025/07/04/木沪时间表2-0-0-0更新了！/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };