var posts=["2025/06/04/如何建立自己的博客(旧博客)/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };