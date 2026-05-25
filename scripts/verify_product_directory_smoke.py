from __future__ import annotations

import argparse
import sys
from pathlib import Path


MIN_DELIVERY_CHARS = 1200


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_before_feedback(text: str) -> str:
    markers = [
        "## 发布前最后确认",
        "## 反馈入口",
        "## 反馈收集问题",
        "用户看完后只需要反馈",
    ]
    positions = [text.find(marker) for marker in markers if marker in text]
    if not positions:
        return text
    return text[: min(positions)]


def question_line_ratio(text: str) -> float:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return 1.0
    question_lines = [
        line
        for line in lines
        if line.endswith("?")
        or line.endswith("？")
        or "请补充" in line
        or "需要补充" in line
    ]
    return len(question_lines) / len(lines)


def find_workspace_root(run_dir: Path) -> Path | None:
    resolved = run_dir.resolve()
    if resolved.parent.name != "runs":
        return None
    return resolved.parent.parent


def require_file(path: Path, label: str, errors: list[str]) -> bool:
    if not path.exists():
        errors.append(f"missing {label}: {path}")
        return False
    if not path.is_file():
        errors.append(f"{label} is not a file: {path}")
        return False
    return True


def verify_product_dir_reference(
    run_dir: Path, product_dir: Path | None, errors: list[str]
) -> None:
    if product_dir is None:
        return
    if not product_dir.exists():
        errors.append(f"product dir does not exist: {product_dir}")
        return
    if not product_dir.is_dir():
        errors.append(f"product path is not a directory: {product_dir}")
        return

    normalized = str(product_dir).replace("\\", "/").rstrip("/")
    run_text = ""
    for file_name in ["run.md", "materials.md", "capture-report.md", "review-report.md"]:
        path = run_dir / file_name
        if path.exists():
            run_text += "\n" + read_text(path).replace("\\", "/")
    if normalized not in run_text:
        errors.append(
            f"product dir is not referenced in run evidence files: {normalized}"
        )


def verify_content_package(content_package: Path, errors: list[str]) -> None:
    if not require_file(content_package, "content-package.md", errors):
        return
    text = read_text(content_package)
    required_markers = [
        "## 产品目录交互顺序",
        "已扫描目录并提取事实层",
        "已生成完整内容框架初稿",
        "已生成用户可读 HTML",
        "已生成可编辑 Markdown",
        "已在框架稿末尾提出",
        "没有扫完目录后先问用户问题",
        "没有只输出问题清单而不输出完整内容框架",
        "## 事实锚定表",
        "用户提交了什么材料",
        "系统先交付了什么",
        "交付物有哪些格式",
        "用户看完后补充了什么",
    ]
    for marker in required_markers:
        if marker not in text:
            errors.append(f"{content_package}: missing marker: {marker}")


def verify_markdown_delivery(markdown_path: Path, errors: list[str]) -> None:
    if not require_file(markdown_path, "markdown delivery", errors):
        return
    text = read_text(markdown_path)
    if len(text) < MIN_DELIVERY_CHARS:
        errors.append(
            f"{markdown_path}: markdown delivery is too short to be a content framework"
        )

    framework_markers = [
        "## 正文草稿",
        "## 内容框架稿",
        "## 可发布内容草稿",
        "完整的内容框架初稿",
    ]
    if not any(marker in text for marker in framework_markers):
        errors.append(
            f"{markdown_path}: missing content framework/body marker before feedback"
        )

    before_feedback = section_before_feedback(text)
    if len(before_feedback) < MIN_DELIVERY_CHARS:
        errors.append(
            f"{markdown_path}: body before feedback is too short; smoke test suspects question-first output"
        )
    ratio = question_line_ratio(before_feedback)
    if ratio > 0.35:
        errors.append(
            f"{markdown_path}: too many question lines before feedback ({ratio:.0%}); smoke test suspects question-first output"
        )

    feedback_markers = [
        "## 发布前最后确认",
        "## 反馈入口",
        "你现在只需要",
    ]
    if not any(marker in text for marker in feedback_markers):
        errors.append(f"{markdown_path}: missing end-of-draft feedback entry")


def verify_html_delivery(html_path: Path, errors: list[str]) -> None:
    if not require_file(html_path, "HTML delivery", errors):
        return
    text = read_text(html_path)
    if len(text) < MIN_DELIVERY_CHARS:
        errors.append(f"{html_path}: HTML delivery is too short")
    if "<html" not in text.lower() or "</html>" not in text.lower():
        errors.append(f"{html_path}: does not look like a complete HTML file")


def verify_run(run_dir: Path, product_dir: Path | None) -> list[str]:
    errors: list[str] = []
    if not run_dir.exists():
        return [f"run dir does not exist: {run_dir}"]
    if not run_dir.is_dir():
        return [f"run path is not a directory: {run_dir}"]

    run_id = run_dir.name
    workspace_root = find_workspace_root(run_dir)
    if workspace_root is None:
        return [
            f"{run_dir}: cannot infer workspace root; expected workspace/{{user}}/runs/{{run_id}}"
        ]

    for file_name in ["run.md", "materials.md", "content-package.md"]:
        require_file(run_dir / file_name, file_name, errors)

    verify_product_dir_reference(run_dir, product_dir, errors)
    verify_content_package(run_dir / "content-package.md", errors)

    output_dir = workspace_root / "outputs" / run_id
    verify_markdown_delivery(output_dir / "content-flywheel-run.md", errors)
    verify_html_delivery(output_dir / "content-flywheel-run.html", errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Smoke test a product-directory content run: directory input must produce "
            "HTML/Markdown framework deliveries before asking follow-up questions."
        )
    )
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--product-dir", type=Path)
    args = parser.parse_args()

    errors = verify_run(args.run_dir, args.product_dir)
    if errors:
        print("Product directory smoke test failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Product directory smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
