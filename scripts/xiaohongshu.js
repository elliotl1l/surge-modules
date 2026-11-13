/**
 * 小红书极速纯净去广告脚本 (Pure Adblock - Zero Watermark/IO Bloat)
 * - 0 日志输出 (移除所有 console.log 与 JSON 冗余序列化)
 * - 0 磁盘 I/O (移除所有 $persistentStore 读写)
 * - 仅在信息流/搜索/开屏拦截广告，不干涉详情页大图/视频/评论区
 */

const url = $request.url;
if (!$response.body) {
  $done({});
}

try {
  let obj = JSON.parse($response.body);

  // 1. 首页瀑布流（去除推广赞助、直播、带货与商品卡片）
  if (url.includes("/homefeed")) {
    if (Array.isArray(obj?.data)) {
      obj.data = obj.data.filter(item => {
        if (item?.model_type === "live_v2") return false; // 直播卡片
        if (item?.hasOwnProperty("ads_info")) return false; // 赞助广告
        if (item?.hasOwnProperty("card_icon")) return false; // 带货卡片
        if (item?.note_attributes?.includes("goods")) return false; // 推广商品
        return true;
      });
      for (let item of obj.data) {
        if (item?.related_ques) delete item.related_ques;
      }
    }
  }

  // 2. 关注流（去除推荐用户卡片）
  else if (url.includes("/followfeed")) {
    if (Array.isArray(obj?.data?.items)) {
      obj.data.items = obj.data.items.filter(item => !["recommend_user"].includes(item?.recommend_reason));
    }
  }

  // 3. 搜索流与搜索提示（去除推广笔记、搜索栏热门发现与推荐词）
  else if (url.includes("/search/notes")) {
    if (Array.isArray(obj?.data?.items)) {
      obj.data.items = obj.data.items.filter(item => item?.model_type === "note");
    }
  }
  else if (url.includes("/search/hot_list")) {
    if (obj?.data) obj.data.items = [];
  }
  else if (url.includes("/search/hint")) {
    if (obj?.data) obj.data.hint_words = [];
  }
  else if (url.includes("/search/trending")) {
    if (obj?.data) {
      obj.data.queries = [];
      obj.data.hint_word = {};
    }
  }
  else if (url.includes("/search/banner_list")) {
    if (obj?.data) obj.data = {};
  }

  // 4. 开屏与系统配置（去除开屏广告预载与活动主题）
  else if (url.includes("/system_service/splash_config")) {
    if (Array.isArray(obj?.data?.ads_groups)) {
      for (let group of obj.data.ads_groups) {
        group.start_time = 3818332800; // 2090年
        group.end_time = 3818419199;
        if (Array.isArray(group?.ads)) {
          for (let ad of group.ads) {
            ad.start_time = 3818332800;
            ad.end_time = 3818419199;
          }
        }
      }
    }
  }
  else if (url.includes("/system_service/config")) {
    const removeKeys = ["app_theme", "loading_img", "splash", "store"];
    if (obj?.data) {
      for (let k of removeKeys) {
        delete obj.data[k];
      }
    }
  }

  // 5. 详情页微件（去除合作品牌与商业活动挂件）
  else if (url.includes("/note/widgets")) {
    const removeWidgets = ["cooperate_binds", "generic", "note_next_step", "widget_list"];
    if (obj?.data) {
      for (let w of removeWidgets) {
        delete obj.data[w];
      }
    }
  }

  $done({ body: JSON.stringify(obj) });
} catch (e) {
  $done({});
}
