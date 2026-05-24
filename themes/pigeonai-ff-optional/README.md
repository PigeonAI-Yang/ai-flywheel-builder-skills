# PigeonAI-FF 可选主题说明

## 定位

这是作者本机品牌主题的适配说明，不是 AI Flywheel Builder 开源核心依赖。

如果用户本机安装了 `PigeonAI-FF-design-spec`，并且明确希望使用雾灯会 / PigeonAI 的报告风格，可以把该设计 skill 作为可选主题使用。

## 依赖边界

- 开源核心不能要求用户安装 `PigeonAI-FF-design-spec`。
- 验收脚本不能把该私有 skill 当作必需文件。
- 生成 HTML 失败时，必须回退到 `J:/pigeonAI/AI-flywheel-Builder/themes/default-html-report/`。
- 本目录只记录适配协议，不复制私有设计 skill 的完整内容。

## 使用规则

当满足以下条件时才使用该可选主题：

1. 用户明确指定使用雾灯会、PigeonAI、PigeonAI-FF 或本机设计范式。
2. 本机可读取对应设计 skill。
3. 该主题不会改变内容主线，只改变呈现方式。

否则使用默认主题。
