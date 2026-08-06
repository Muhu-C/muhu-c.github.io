(() => {
  const utilsFn = {
    throttle: (func, wait, { leading = true, trailing = true } = {}) => {
      let timeout,
        previous = 0;
      const later = (context, args) => {
        timeout = previous = leading === false ? 0 : Date.now();
        func.apply(context, args);
      };
      return function () {
        const now = Date.now();
        if (!previous && leading === false) previous = now;
        const remaining = wait - (now - previous);
        if (remaining <= 0 || remaining > wait) {
          if (timeout) clearTimeout(timeout);
          later(this, arguments);
        } else if (!timeout && trailing !== false) {
          timeout = setTimeout(() => later(this, arguments), remaining);
        }
      };
    },
    fadeIn: (ele, time) => {
      ele.style.display = "block";
      ele.style.animation = `to_show ${time}s`;
    },
    fadeOut: (ele, time) => {
      const resetStyles = () => {
        ele.style.display = "none";
        ele.style.animation = "";
        ele.removeEventListener("animationend", resetStyles);
      };
      ele.addEventListener("animationend", resetStyles);
      ele.style.animation = `to_hide ${time}s`;
    },
    snackbarShow: (text, showAction = false, duration = 5000) => {
      Snackbar.show({ text, showAction, duration, pos: "top-center" });
    },
    copy: async (text) => {
      const message = await navigator.clipboard
        .writeText(text)
        .then(() => Solitude.config.lang.copy.success)
        .catch(() => Solitude.config.lang.copy.error);
      Solitude.snackbarShow(message, false, 2000);
    },
    getEleTop: (ele) => {
      let actualTop = ele.offsetTop;
      while (ele.offsetParent) {
        ele = ele.offsetParent;
        actualTop += ele.offsetTop;
      }
      return actualTop;
    },
    siblings: (ele, selector) => {
      return [...ele.parentNode.children].filter(
        (child) => child !== ele && (!selector || child.matches(selector))
      );
    },
    randomNum: (length) => Math.floor(Math.random() * length),
    timeDiff: (timeObj, today) =>
      Math.floor((today.getTime() - timeObj.getTime()) / (1000 * 3600 * 24)),
    scrollToDest: (pos, time = 500) => {
      const currentPos = window.pageYOffset;
      const isNavFixed = document
        .getElementById("page-header")
        .classList.contains("nav-fixed");
      pos = currentPos > pos || isNavFixed ? pos - 70 : pos;

      if ("scrollBehavior" in document.documentElement.style) {
        window.scrollTo({ top: pos, behavior: "smooth" });
        return;
      }

      const distance = pos - currentPos;
      const step = (currentTime) => {
        const progress = currentTime - (start || currentTime);
        if (progress < time) {
          window.scrollTo(0, currentPos + (distance * progress) / time);
          window.requestAnimationFrame(step);
        } else {
          window.scrollTo(0, pos);
        }
      };

      window.requestAnimationFrame(step);
    },
    isMobile: () =>
      /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
      ),
    isHidden: (e) => e.offsetHeight === 0 && e.offsetWidth === 0,
    animateIn: (ele, text) => {
      Object.assign(ele.style, { display: "block", animation: text });
    },
    animateOut: (ele, text) => {
      const resetAnimation = () => {
        ele.style.display = "";
        ele.style.animation = "";
        ele.removeEventListener("animationend", resetAnimation);
      };
      ele.addEventListener("animationend", resetAnimation);
      ele.style.animation = text;
    },
    wrap: (selector, eleType, options) => {
      const createEle = document.createElement(eleType);
      Object.entries(options).forEach(([key, value]) =>
        createEle.setAttribute(key, value)
      );
      selector.parentNode.insertBefore(createEle, selector);
      createEle.appendChild(selector);
    },
    lazyloadImg: () => {
      window.lazyLoadInstance = new LazyLoad({
        elements_selector: "img",
        threshold: 0,
        data_src: "lazy-src",
        callback_error: (img) => (img.src = Solitude.config.lazyload.error),
      });
    },
    lightbox: function (selector) {
      const lightboxType = Solitude.config.lightbox;
      const options = {
        class: "fancybox",
        "data-fancybox": "gallery",
      };

      if (lightboxType === "mediumZoom") {
        mediumZoom &&
          mediumZoom(selector, { background: "var(--efu-card-bg)" });
      } else if (lightboxType === "fancybox") {
        selector.forEach((i) => {
          if (i.parentNode.tagName !== "A") {
            options.href = options["data-thumb"] = i.dataset.lazySrc || i.src;
            options["data-caption"] = i.title || i.alt || "";
            Solitude.wrap(i, "a", options);
          }
        });

        if (!window.fancyboxRun) {
          Fancybox.bind("[data-fancybox]", {
            Hash: false,
            animated: true,
            Thumbs: { showOnStart: false },
            Images: { Panzoom: { maxScale: 4 } },
            Carousel: { transition: "slide" },
            Toolbar: {
              display: {
                left: ["infobar"],
                middle: [
                  "zoomIn",
                  "zoomOut",
                  "toggle1to1",
                  "rotateCCW",
                  "rotateCW",
                  "flipX",
                  "flipY",
                ],
                right: ["slideshow", "thumbs", "close"],
              },
            },
          });
          window.fancyboxRun = true;
        }
      }
    },
    diffDate: (d, more = false) => {
      const dateNow = new Date();
      const datePost = new Date(d);
      const dateDiff = dateNow - datePost;
      const minute = 60000;
      const hour = 3600000;
      const day = 86400000;
      const month = 2592000000;
      const { time } = Solitude.config.lang;

      const dayCount = Math.floor(dateDiff / day);
      if (!more) return dayCount;

      const minuteCount = Math.floor(dateDiff / minute);
      const hourCount = Math.floor(dateDiff / hour);
      const monthCount = Math.floor(dateDiff / month);

      if (monthCount > 12) return datePost.toISOString().slice(0, 10);
      if (monthCount >= 1) return `${monthCount} ${time.month}`;
      if (dayCount >= 1) return `${dayCount} ${time.day}`;
      if (hourCount >= 1) return `${hourCount} ${time.hour}`;
      if (minuteCount >= 1) return `${minuteCount} ${time.min}`;
      return time.just;
    },
    loadComment: (dom, callback) => {
      const observerItem =
        "IntersectionObserver" in window
          ? new IntersectionObserver(
              (entries) => {
                if (entries[0].isIntersecting) {
                  callback();
                  observerItem.disconnect();
                }
              },
              { threshold: [0] }
            )
          : null;

      observerItem ? observerItem.observe(dom) : callback();
    },
    escapeHtml: (unsafe) =>
      unsafe.replace(
        /[&<"']/g,
        (m) =>
          ({
            "&": "&amp;",
            "<": "&lt;",
            '"': "&quot;",
            "'": "&#039;",
          }[m])
      ),
    // 日历卡片渲染（侧边栏）
    renderCalendar: () => {
      const now = new Date();
      const year = now.getFullYear();
      const month = now.getMonth();
      const week = now.getDay();
      const date = now.getDate();

      // 处理侧边栏日历
      const asideCal = document.getElementById('card-widget-calendar');
      const containers = [asideCal].filter(Boolean);

      containers.forEach((el) => {
        const weekStr = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][week];
        const monthData = [
          { month: '1月', days: 31 },
          { month: '2月', days: year % 4 === 0 && year % 100 !== 0 || year % 400 === 0 ? 29 : 28 },
          { month: '3月', days: 31 },
          { month: '4月', days: 30 },
          { month: '5月', days: 31 },
          { month: '6月', days: 30 },
          { month: '7月', days: 31 },
          { month: '8月', days: 31 },
          { month: '9月', days: 30 },
          { month: '10月', days: 31 },
          { month: '11月', days: 30 },
          { month: '12月', days: 31 }
        ];

        const monthStr = monthData[month].month;
        const dates = monthData[month].days;
        const n = (week + 8 - date % 7) % 7;
        let t = '', r = false;
        const d = 7 - n;
        const o = (dates - d) % 7 === 0 ? Math.floor((dates - d) / 7) + 1 : Math.floor((dates - d) / 7) + 2;
        const mainEl = el.querySelector('#calendar-main');
        if (!mainEl) return;

        const dateEl = el.querySelector('#calendar-date');
        if (dateEl) {
          dateEl.style.fontSize = ['64px', '48px', '36px'][Math.min(o - 3, 2)];
        }

        for (let i = 0; i < o; i++) {
          if (!mainEl.querySelector('.calendar-r' + i)) {
            mainEl.innerHTML += '<div class="calendar-r' + i + '"></div>';
          }
          for (let j = 0; j < 7; j++) {
            if (i === 0 && j === n) { t = 1; r = true; }
            const cls = t === date ? " class='now'" : '';
            if (!mainEl.querySelector(`.calendar-r${i} .calendar-d${j} a`)) {
              if (t != '')
                mainEl.querySelector(`.calendar-r${i}`).innerHTML += `<div class="calendar-d${j}"><a${cls}>${t}</a></div>`;
              else mainEl.querySelector(`.calendar-r${i}`).innerHTML += `<div class="calendar-d${j}"></div>`;
            }
            if (t >= dates) { t = ''; r = false; }
            if (r) t += 1;
          }
        }

        // 农历信息（依赖 chinese_lunar.js）
        if (typeof chineseLunar !== 'undefined') {
          const lunar = chineseLunar.solarToLunar(new Date(year, month, date));
          const animalYear = chineseLunar.format(lunar, 'A');
          const ganzhiYear = chineseLunar.format(lunar, 'T').slice(0, -1);
          const lunarMon = chineseLunar.format(lunar, 'M');
          const lunarDay = chineseLunar.format(lunar, 'd');
          const asideTime = new Date(year + '/01/01 00:00:00');
          const asideDay = ((now - asideTime) / 86400000);
          const asideDayNum = Math.floor(asideDay);
          const weekNum = week - asideDayNum % 7 >= 0 ? Math.ceil(asideDayNum / 7) : Math.ceil(asideDayNum / 7) + 1;

          const weekEl = el.querySelector('#calendar-week');
          const dateDisplayEl = el.querySelector('#calendar-date');
          const solarEl = el.querySelector('#calendar-solar');
          const lunarEl = el.querySelector('#calendar-lunar');

          if (weekEl) weekEl.innerHTML = '第' + weekNum + '周&nbsp;' + weekStr;
          if (dateDisplayEl) dateDisplayEl.innerHTML = date.toString().padStart(2, '0');
          if (solarEl) solarEl.innerHTML = year + '年' + monthStr + '&nbsp;第' + asideDay.toFixed(0) + '天';
          if (lunarEl) lunarEl.innerHTML = ganzhiYear + animalYear + '年&nbsp;' + lunarMon + lunarDay;
        }
      });
    },
  };
  Object.assign(window.Solitude, utilsFn);
})();
