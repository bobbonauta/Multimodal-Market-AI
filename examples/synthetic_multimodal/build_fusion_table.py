from pathlib import Path

from multimodal_market_ai.synthetic_demo import build_fusion_table, generate_synthetic_market

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fusion = build_fusion_table(generate_synthetic_market())
    path = OUTPUT_DIR / "fusion_table.csv"
    fusion.to_csv(path, index=False)
    print(fusion[["case_id", "det_signal", "visual_signal", "decision"]].to_string(index=False))
    print(f"fusion table -> {path}")


if __name__ == "__main__":
    main()
