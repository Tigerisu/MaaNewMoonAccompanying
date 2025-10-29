import { defineUserConfig } from "vuepress";
import recoTheme from "vuepress-theme-reco";
import { viteBundler } from "@vuepress/bundler-vite";

import nav from "./router/nav";
import sidebar from "./router/sidebar";

export default defineUserConfig({
  title: "MNMA文档站",
  description:
    "MNMA 是一款基于 MaaFramework 与 MFAAvalonia 的新月同行小助手，基于图像识别技术，一键完成全部日常任务，旨在帮您完成重复的日常。",
  bundler: viteBundler(),
  base: "/mnma/",
  head: [["link", { rel: "icon", href: "/logo.ico" }]],
  theme: recoTheme({
    logo: "/logo.png",
    author: "kqcoxn",
    authorAvatar: "/head.png",
    docsRepo: "https://github.com/kqcoxn/MaaNewMoonAccompanying",
    docsBranch: "main",
    docsDir: "tree/main/DocSite",
    lastUpdatedText: "",
    series: sidebar,
    navbar: nav,
  }),
});
