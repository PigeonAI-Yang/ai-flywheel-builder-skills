<img src="assets/header.png" alt="AI Flywheel Builder" width="100%">

# AI Flywheel Builder

把做过的 AI 实践，持续变成值得传播的内容。

## 解决什么问题

很多 AI 实践者手上攒了一堆东西——做的工具、调的 workflow、踩过的坑、跑通的实验。材料越多，越不知道从哪开始写。

这不是写作能力的问题。是判断问题：你不知道自己做的这些东西里，什么值得讲、讲给谁、怎么讲、哪些不能讲。

AI Flywheel Builder 接上了这条从实践到内容的断层。

## 怎么工作

给它一个项目目录。乱的也行。

它读完，不直接吐稿子。先给你一个内容框架：写给谁、主线是什么、正文怎么展开、哪里还缺你的真实经历、什么绝对不能写。你确认方向对了，补几段关键经历，它把框架和经历接在一起，扩成完整稿。

发出去之后，反馈——评论、截图、转发——也可以回到系统里。不是看一眼数据就完了，而是搞清楚问题出在哪，写回下一轮行动。

每一次实践都让下一次判断更容易。越用越知道什么值得讲。

## 快速开始

1. 克隆仓库到你的 Claude Code skills 目录：

```bash
git clone https://github.com/PigeonAI-Yang/ai-flywheel-builder-skills.git
```

2. 在 Claude Code 中调用：

```text
/ai-flywheel-builder
```

3. 第一次使用会引导你完成初始化。已经有项目？直接把目录给它就行。

## 项目结构

```text
skills/          # 技能模块
templates/       # 输出模板
scripts/         # 验证脚本
themes/          # HTML 交付主题
docs/            # 详细文档
workspace/       # 你的工作区（运行时生成）
```

## 版本

当前 V0.1。下一个版本将支持更多创作场景——不止已有产品，心得体会、学习笔记也能跑。

详见 [CHANGELOG.md](CHANGELOG.md) 和 [Roadmap](docs/03_ROADMAP.md)。

## 参与改进

如果你喜欢这个项目，点个 star 是对我最大的鼓励。

有 bug、建议、想贡献代码？欢迎提 [Issue](https://github.com/PigeonAI-Yang/ai-flywheel-builder-skills/issues) 或 PR。

## 许可

MIT License
