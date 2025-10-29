const nav = [
  { text: "首页", link: "/" },
  { text: "用户手册", link: "/docs/users/guide/start" },
  { text: "开发者文档", link: "/docs/developers/agreement" },
  {
    text: "友情链接",
    children: [
      {
        text: "Mirror酱",
        link: "https://mirrorchyan.com/zh/get-start",
      },
      {
        text: "MaaFramework",
        link: "https://github.com/MaaXYZ/MaaFramework",
      },
      {
        text: "MFAAvalonia",
        link: "https://github.com/SweetSmellFox/MFAAvalonia",
      },
      {
        text: "MaaPipelineEditor",
        link: "https://github.com/kqcoxn/MaaPipelineEditor",
      },
    ],
  },
];

export default nav;
