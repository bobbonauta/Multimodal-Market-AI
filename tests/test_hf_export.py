import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from multimodal_market_ai.synthetic_demo import write_demo

ROOT = Path(__file__).resolve().parents[1]
HF_DIR = ROOT / "huggingface"


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _Hub:
    """Stand-in for ``huggingface_hub`` that records every call; CI does not install it."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    @property
    def module(self) -> ModuleType:
        hub = self
        module = ModuleType("huggingface_hub")

        class HfApi:
            def __init__(self) -> None:
                hub.calls.append("HfApi")

            def __getattr__(self, name: str):
                def call(*args: object, **kwargs: object) -> None:
                    hub.calls.append(name)

                return call

        module.HfApi = HfApi  # type: ignore[attr-defined]
        return module


@pytest.fixture
def hub(monkeypatch: pytest.MonkeyPatch) -> _Hub:
    fake = _Hub()
    monkeypatch.setitem(sys.modules, "huggingface_hub", fake.module)
    monkeypatch.setitem(sys.modules, "static_page", _load("static_page", HF_DIR / "static_page.py"))
    return fake


def _export_on_branch(
    monkeypatch: pytest.MonkeyPatch, branch: str, *args: str
) -> ModuleType:
    """Load export_to_hub as if ``git`` reported ``branch``, and run it with ``args``."""
    module = _load("export_to_hub", HF_DIR / "export_to_hub.py")

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 0, stdout=f"{branch}\n", stderr="")

    monkeypatch.setattr(
        module,
        "subprocess",
        SimpleNamespace(run=fake_run, CalledProcessError=subprocess.CalledProcessError),
    )
    monkeypatch.setattr(sys, "argv", ["export_to_hub.py", "--namespace", "example", *args])
    return module


@pytest.mark.parametrize("branch", ["hf-readme-parity", ""])
def test_real_export_is_refused_off_main(
    hub: _Hub, monkeypatch: pytest.MonkeyPatch, branch: str
) -> None:
    module = _export_on_branch(monkeypatch, branch)

    with pytest.raises(SystemExit) as stopped:
        module.main()

    assert "Refusing Hugging Face publish: current Git branch is not main" in str(stopped.value)
    assert "Merge and verify main before publishing." in str(stopped.value)
    assert hub.calls == []


def test_dry_run_still_works_off_main(
    hub: _Hub, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    module = _export_on_branch(monkeypatch, "hf-readme-parity", "--dry-run")

    module.main()

    assert "nothing uploaded" in capsys.readouterr().out
    assert "create_repo" not in hub.calls
    assert "upload_folder" not in hub.calls


def test_real_export_runs_on_main(hub: _Hub, monkeypatch: pytest.MonkeyPatch) -> None:
    _export_on_branch(monkeypatch, "main").main()

    assert hub.calls.count("upload_folder") == 2


def _headings(markdown: str) -> set[str]:
    return set(re.findall(r"^##+ (.+)$", markdown, flags=re.MULTILINE))


def test_dataset_card_describes_the_dataset_not_the_whole_readme() -> None:
    card = (HF_DIR / "dataset" / "README.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert {"Schema", "How it is generated", "Limits", "License"} <= _headings(card)
    assert "https://github.com/bobbonauta/Multimodal-Market-AI" in card
    assert "mermaid" not in card
    # "License" is the one section both documents legitimately have.
    assert (_headings(card) & _headings(readme)) <= {"License"}
    assert len(card) < len(readme) / 2


def test_exported_files_carry_no_private_reference(tmp_path: Path) -> None:
    from_demo = tmp_path / "demo"
    write_demo(from_demo)
    space = tmp_path / "space"
    _load("static_page", HF_DIR / "static_page.py").build_static_space(
        from_demo, space, "https://huggingface.co/datasets/example/data"
    )

    exported = [*from_demo.rglob("*"), *space.rglob("*"), *HF_DIR.rglob("*")]
    texts = [
        path.read_text(encoding="utf-8", errors="ignore")
        for path in exported
        if path.is_file() and "__pycache__" not in path.parts
    ]

    assert texts
    assert not [text for text in texts if "bradipo" in text.lower()]
