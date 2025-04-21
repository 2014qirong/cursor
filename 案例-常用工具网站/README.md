# 实用工具集网站

这是一个基于网页的实用工具集合网站，提供多种常用的在线工具，帮助用户提高工作效率。

## 功能特点

- 免费使用：所有工具完全免费
- 在线操作：无需下载安装，直接在浏览器中使用
- 隐私保护：所有处理在本地完成，不会上传敏感数据到服务器
- 响应式设计：适配PC和移动设备
- 简洁美观的界面

## 可用工具

网站包含以下实用工具：

### 已实现

- **图片转PDF**：将多张图片合并为一个PDF文件，方便分享和打印

### 计划实现

- **文件转换**：支持多种格式文件的相互转换
- **图片压缩**：无损压缩图片，减小文件大小
- **图片水印**：为图片添加文字或图片水印
- **图片裁剪**：裁剪图片尺寸或调整比例
- **图片去重**：自动识别并移除重复图片

## 项目结构

```
实用工具集/
├── index.html                # 网站首页
├── styles/                   # 样式文件目录
│   ├── main.css              # 全局样式
│   ├── responsive.css        # 响应式设计样式
│   └── tools.css             # 工具页面公共样式
├── scripts/                  # 脚本文件目录
│   ├── main.js               # 全局脚本
│   ├── utils.js              # 工具函数库
│   └── tools/                # 各工具脚本
│       ├── image-to-pdf.js   # 图片转PDF工具脚本
│       └── ...               # 其他工具脚本
├── tools/                    # 工具页面目录
│   ├── image-to-pdf.html     # 图片转PDF工具
│   ├── image-compressor.html # 图片压缩工具
│   └── ...                   # 其他工具页面
├── assets/                   # 资源文件目录
│   ├── images/               # 图片资源
│   ├── icons/                # 图标资源
│   └── libs/                 # 第三方库
└── README.md                 # 项目说明文档
```

## 使用技术

- HTML5
- CSS3 (Flexbox, Grid, 自定义变量)
- 原生JavaScript (ES6+)
- 响应式设计
- FontAwesome 图标

## 本地运行方法

1. 克隆或下载本仓库到本地
2. 使用现代浏览器(Chrome, Firefox, Safari, Edge等)直接打开 `index.html` 文件
3. 或者使用本地服务器运行项目，例如：

```bash
# 使用Python创建简单的HTTP服务器
python -m http.server

# 或者使用Node.js的http-server
npm install -g http-server
http-server
```

## 浏览器兼容性

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 16+

## 贡献指南

欢迎贡献新的工具或改进现有功能。如需贡献，请遵循以下步骤：

1. Fork本仓库
2. 创建新的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m '添加了某个特性'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，请通过以下方式联系我们：

- 邮箱: contact@toolbox.com
- 网站: [实用工具集](https://toolbox.example.com)

---

感谢使用实用工具集！ 