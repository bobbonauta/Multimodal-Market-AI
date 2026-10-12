"""Export the public synthetic demo to Hugging Face Dataset and Space repos."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path

from huggingface_hub import HfApi
from static_page import build_static_space

from multimodal_market_ai.synthetic_demo import write_demo

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-name", default="multimodal-market-ai-synthetic")
    parser.add_argument("--space-name", default="multimodal-market-ai-demo")
    parser.add_argument(
        "--space-type",
        choices=("static", "gradio"),
        default="static",
        help=(
            "static: plain HTML page, free on every account. "
            "gradio: interactive app, needs a Hugging Face PRO subscription for CPU hosting."
        ),
    )
    parser.add_argument("--namespace")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def resolve_namespace(api: HfApi, requested: str | None) -> str:
    if requested:
        return requested
    identity = api.whoami()
    return str(identity["name"])


def prepare_dataset(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    write_demo(destination)
    shutil.copy2(ROOT / "huggingface" / "dataset" / "README.md", destination / "README.md")


def prepare_space(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for filename in ("README.md", "app.py", "requirements.txt"):
        shutil.copy2(
            ROOT / "huggingface" / "space" / filename,
            destination / filename,
        )
    shutil.copy2(
        ROOT / "src" / "multimodal_market_ai" / "synthetic_demo.py",
        destination / "synthetic_demo.py",
    )
    shutil.copy2(
        ROOT / "src" / "multimodal_market_ai" / "deterministic.py",
        destination / "deterministic.py",
    )

    synthetic_path = destination / "synthetic_demo.py"
    text = synthetic_path.read_text(encoding="utf-8")
    text = text.replace(
        "from .deterministic import combine_directional_signals",
        "from deterministic import combine_directional_signals",
    )
    synthetic_path.write_text(text, encoding="utf-8")


def prepare_static_space(destination: Path, dataset_id: str) -> None:
    """Build the HTML-only Space from a fresh run of the synthetic demo."""
    with tempfile.TemporaryDirectory(prefix="mma-hf-demo-") as demo:
        demo_dir = Path(demo)
        write_demo(demo_dir)
        build_static_space(
            demo_dir,
            destination,
            dataset_url=f"https://huggingface.co/datasets/{dataset_id}",
        )


def main() -> None:
    args = parse_args()
    api = HfApi()
    namespace = resolve_namespace(api, args.namespace)

    dataset_id = f"{namespace}/{args.dataset_name}"
    space_id = f"{namespace}/{args.space_name}"

    print(f"dataset -> {dataset_id}")
    print(f"space   -> {space_id}")

    with tempfile.TemporaryDirectory(prefix="mma-hf-") as temp:
        temp_root = Path(temp)
        dataset_dir = temp_root / "dataset"
        space_dir = temp_root / "space"

        prepare_dataset(dataset_dir)
        if args.space_type == "static":
            prepare_static_space(space_dir, dataset_id)
        else:
            prepare_space(space_dir)

        if args.dry_run:
            print("dry-run: export folders prepared; nothing uploaded")
            return

        api.create_repo(
            repo_id=dataset_id,
            repo_type="dataset",
            private=args.private,
            exist_ok=True,
        )
        api.upload_folder(
            repo_id=dataset_id,
            repo_type="dataset",
            folder_path=str(dataset_dir),
            commit_message="Sync synthetic multimodal demo",
        )

        api.create_repo(
            repo_id=space_id,
            repo_type="space",
            space_sdk=args.space_type,
            private=args.private,
            exist_ok=True,
        )
        api.upload_folder(
            repo_id=space_id,
            repo_type="space",
            folder_path=str(space_dir),
            commit_message=f"Sync {args.space_type} demo Space",
        )

    print("Hugging Face export complete")


if __name__ == "__main__":
    main()
