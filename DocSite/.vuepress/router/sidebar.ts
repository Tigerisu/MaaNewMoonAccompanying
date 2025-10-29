const sidebar = {
  "/docs/users/": [
    {
      text: "用户手册",
      children: [
        "guide/start",
        "guide/install",
        "guide/init",
        "guide/funcs",
        "guide/errors",
      ],
    },
    {
      text: "使用技巧",
      children: ["tricks/software", "tricks/task"],
    },
  ],
  "/docs/developers/": [
    {
      text: "开发者文档",
      children: ["agreement", "init", "structure"],
    },
  ],
};

export default sidebar;
