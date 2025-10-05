document.addEventListener("DOMContentLoaded", () => {
    // -------------------------------- 以下是自定义内容 -------------------------------- //
    // 从网站配置获取版本号
    const CURRENT_THEME_VERSION = window.MUHUTHEME_CONFIG?.version || "0.0.0";
    
    // 存储的主题版本
    const previousVersion = localStorage.getItem("muhuTheme_version");
    const popupShown = localStorage.getItem("muhuTheme_popup_shown");
    
    console.log('MuhuTheme Info', {
        currentVersion: CURRENT_THEME_VERSION,
        lastVisitVersion: previousVersion,
        isPopupShown: popupShown
    });
    
    // 检查是否是第一次访问或者版本有更新
    const isFirstVisit = !popupShown;
    const isVersionUpdated = previousVersion !== CURRENT_THEME_VERSION;
    
    if (isFirstVisit || isVersionUpdated) {
        console.log('Show Popup: ', isFirstVisit ? 'First visit' : 'Version update');
        
        Snackbar.show({
            text: `本网站主题已由 v${previousVersion} 更新至 v${CURRENT_THEME_VERSION}`, 
            pos: "top-center", 
            actionText: "确定", 
            onClose: () => {
                localStorage.setItem("muhuTheme_popup_shown", "true");
                localStorage.setItem("muhuTheme_version", CURRENT_THEME_VERSION);
            }
        });
        
        // 更新版本信息
        if (isVersionUpdated) {
            localStorage.setItem("muhuTheme_version", CURRENT_THEME_VERSION);
        }
    }
});