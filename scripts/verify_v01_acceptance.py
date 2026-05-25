from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FIXED_STAGES = [
    "not_initialized",
    "initializing",
    "practice_design",
    "practice_execution_waiting",
    "practice_capture",
    "practice_review",
    "content_package",
    "feedback_waiting",
    "feedback_attribution",
    "learning_closure",
    "next_practice_ready",
    "blocked",
]

DEPRECATED_STAGE_VALUES = [
    "initialization_interview",
    "initialization_confirm",
    "content_decomposition",
    "content_ready",
    "content_iteration",
    "artifact_iteration",
    "artifact_design",
    "memory_update",
    "gatekeeping",
    "product_iteration",
    "practice_review_blocked",
]

REQUIRED_MARKERS = {
    "skills/ai-flywheel-builder/SKILL.md": [
        "Orchestrator Priority Rule",
        "Fixed State Rule",
        "missing_requirements",
        "content_package",
        "feedback_attribution",
        "Use simplified Chinese",
        "machine translation",
    ],
    "skills/flywheel-orchestrator/SKILL.md": [
        "Highest Priority",
        "Fixed State Values",
        "next_action",
        "missing_requirements",
    ],
    "templates/flywheel-state.md": [
        "## allowed_current_stage_values",
        "## next_action",
        "## missing_requirements",
    ],
    "templates/content-flywheel-run.md": [
        "HTML 优先",
        "HTML 主题",
        "## 当前稿件状态",
        "事实约束",
        "事实锚定表",
        "补采问题只能放在稿末",
        "## 信息增量",
        "## 内容框架稿",
        "读者层级与判断主线",
        "## 本轮实践一句话",
        "## 为什么值得讲",
        "## 可发布内容草稿",
        "## 配套可领取产物",
        "## 证据与边界",
        "## 反馈入口",
        "## 下一轮实践",
    ],
    "skills/content-decomposer/SKILL.md": [
        "workspace/{user}/outputs/{run_id}/content-flywheel-run.html",
        "workspace/{user}/outputs/{run_id}/content-flywheel-run.md",
        "J:/pigeonAI/AI-flywheel-Builder/themes/default-html-report/",
        "私有设计 skill 当作必装依赖",
        "产品目录材料分层",
        "外部读者视角",
        "对外稿默认结构",
        "产品发布长文协议",
        "信息增量协议",
        "框架先行协议",
        "事实锚定协议",
        "产品目录交互顺序硬规则",
        "先生成完整内容框架初稿",
        "公开稿与后台记录隔离",
        "判断优先规则",
        "实践细节补采",
        "发布稿自检",
        "外部语言闸门",
        "中文输出风格硬规则",
        "英文直译腔",
        "不要只有后台文件而没有用户可见主交付物",
    ],
    "templates/content-package.md": [
        "## 产品发布长文协议",
        "## 产品目录材料分层",
        "## 产品目录交互顺序",
        "## 事实锚定表",
        "站在外部读者视角提取到的信息",
        "## 信息增量自检",
        "## 内容框架稿",
        "## 读者层级",
        "## 判断机制",
        "## 外部语言闸门",
        "## 实践细节补采",
        "## 发布稿自检",
        "## 修订入口",
        "技术细节只在后半段作为可信度证据",
    ],
    "templates/memory-rules.md": [
        "对外内容避坑规则",
        "用户反馈可以改变产品规则，但不能原样进入对外内容",
        "自造术语、内部口径、项目黑话",
        "交付稿不是一次性终稿",
        "产品发布长文协议",
        "可读的产品介绍不等于可发布内容",
        "目录本身就是高密度材料",
        "外部读者视角",
        "英文直译腔",
    ],
    "scripts/verify_product_directory_smoke.py": [
        "Product directory smoke test",
        "question-first output",
        "已生成完整内容框架初稿",
        "content-flywheel-run.html",
        "content-flywheel-run.md",
    ],
    "docs/01_ARCHITECTURE.md": [
        "Fixed State Values",
        "Visible Delivery",
        "content-flywheel-run.html",
        "content-flywheel-run.md",
        "themes/default-html-report",
    ],
    "README.md": [
        "固定状态与中控规则",
        "用户可见主交付物",
        "themes/default-html-report",
        "V0.1 整体验收",
    ],
    "themes/default-html-report/README.md": [
        "开源默认主题",
        "单文件 HTML",
        "content-flywheel-run.html",
        "不显示后台运行信息",
    ],
    "themes/default-html-report/template.html": [
        "{{title}}",
        "本轮实践一句话",
        "信息增量",
        "内容框架稿",
        "下一轮实践",
    ],
    "themes/pigeonai-ff-optional/README.md": [
        "不是 AI Flywheel Builder 开源核心依赖",
        "回退到 `J:/pigeonAI/AI-flywheel-Builder/themes/default-html-report/`",
    ],
}

TEXT_EXTENSIONS = {".md", ".py", ".html"}


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        raise AssertionError(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def require_markers(relative_path: str, markers: list[str]) -> list[str]:
    text = read_text(relative_path)
    return [
        f"{relative_path}: missing marker: {marker}"
        for marker in markers
        if marker not in text
    ]


def verify_project_rules() -> list[str]:
    errors: list[str] = []

    for relative_path, markers in REQUIRED_MARKERS.items():
        errors.extend(require_markers(relative_path, markers))

    public_template = read_text("templates/content-flywheel-run.md")
    forbidden_public_template_markers = [
        "## run_id",
        "## run_uuid",
        "## 后台记录",
        "## 已更新文件",
        "## 验收结论",
    ]
    for marker in forbidden_public_template_markers:
        if marker in public_template:
            errors.append(
                f"templates/content-flywheel-run.md: public delivery template still contains backend marker: {marker}"
            )

    html_theme_template = read_text("themes/default-html-report/template.html")
    forbidden_html_theme_markers = [
        "{{run_id}}",
        "{{backstage_records}}",
        "<summary>后台记录</summary>",
    ]
    for marker in forbidden_html_theme_markers:
        if marker in html_theme_template:
            errors.append(
                f"themes/default-html-report/template.html: HTML theme still renders backend marker: {marker}"
            )

    hard_dependency_phrases = [
        "必须使用雾灯会",
        "必须使用 PigeonAI-FF-design-spec",
        "必须安装 PigeonAI-FF-design-spec",
        "应使用雾灯会精装年报",
    ]
    for relative_path in [
        "README.md",
        "docs/00_PRODUCT_BRIEF.md",
        "docs/01_ARCHITECTURE.md",
        "skills/content-decomposer/SKILL.md",
    ]:
        text = read_text(relative_path)
        for phrase in hard_dependency_phrases:
            if phrase in text:
                errors.append(
                    f"{relative_path}: hard private theme dependency phrase still present: {phrase}"
                )

    state_template = read_text("templates/flywheel-state.md")
    for stage in FIXED_STAGES:
        if stage not in state_template:
            errors.append(f"templates/flywheel-state.md: missing fixed stage: {stage}")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.name == "verify_v01_acceptance.py":
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8")
        for deprecated in DEPRECATED_STAGE_VALUES:
            if deprecated in text:
                errors.append(f"{path}: deprecated stage value still present: {deprecated}")

    return errors


def extract_section_value(text: str, heading: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == heading:
            values: list[str] = []
            for next_line in lines[index + 1 :]:
                if next_line.startswith("## "):
                    break
                stripped = next_line.strip()
                if stripped:
                    values.append(stripped)
            return "\n".join(values).strip()
    return ""


def find_workspace_root(run_dir: Path) -> Path | None:
    resolved = run_dir.resolve()
    if resolved.parent.name != "runs":
        return None
    return resolved.parent.parent


def verify_run_dir(run_dir: Path) -> list[str]:
    errors: list[str] = []
    if not run_dir.exists():
        return [f"run dir does not exist: {run_dir}"]

    required_run_files = [
        "run.md",
        "materials.md",
        "capture-report.md",
        "review-report.md",
        "content-package.md",
        "learning-closure.md",
    ]
    for file_name in required_run_files:
        if not (run_dir / file_name).exists():
            errors.append(f"{run_dir}: missing run file: {file_name}")

    closure_path = run_dir / "learning-closure.md"
    if closure_path.exists():
        closure_text = closure_path.read_text(encoding="utf-8")
        run_id = extract_section_value(closure_text, "## run_id")
    else:
        run_id = run_dir.name

    content_package_path = run_dir / "content-package.md"
    if content_package_path.exists():
        content_package_text = content_package_path.read_text(encoding="utf-8")
        required_content_package_markers = [
            "## 产品目录交互顺序",
            "已生成完整内容框架初稿",
            "已生成用户可读 HTML",
            "已生成可编辑 Markdown",
            "没有扫完目录后先问用户问题",
            "## 事实锚定表",
            "用户提交了什么材料",
            "系统先交付了什么",
            "交付物有哪些格式",
            "用户看完后补充了什么",
            "未锚定事实",
        ]
        for marker in required_content_package_markers:
            if marker not in content_package_text:
                errors.append(
                    f"{content_package_path}: missing fact anchoring marker: {marker}"
                )

    workspace_root = find_workspace_root(run_dir)
    if workspace_root is None:
        errors.append(
            f"{run_dir}: cannot infer workspace root; expected workspace/{{user}}/runs/{{run_id}}"
        )
        return errors

    html_output_path = workspace_root / "outputs" / run_id / "content-flywheel-run.html"
    if not html_output_path.exists():
        errors.append(f"{html_output_path}: missing HTML visible main delivery")

    markdown_output_path = workspace_root / "outputs" / run_id / "content-flywheel-run.md"
    if not markdown_output_path.exists():
        errors.append(f"{markdown_output_path}: missing markdown source delivery")

    index_path = workspace_root / "indexes" / "learning-index.md"
    if not index_path.exists():
        errors.append(f"{index_path}: missing learning index")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify AI Flywheel Builder V0.1 rules.")
    parser.add_argument(
        "--run-dir",
        type=Path,
        help="Optional run directory to verify for a closed V0.1 practice run.",
    )
    args = parser.parse_args()

    errors = verify_project_rules()
    if args.run_dir:
        errors.extend(verify_run_dir(args.run_dir))

    if errors:
        print("V0.1 acceptance verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.run_dir:
        print("V0.1 acceptance verification passed for project rules and run dir.")
    else:
        print("V0.1 acceptance verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
