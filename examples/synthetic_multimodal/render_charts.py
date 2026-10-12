from pathlib import Path

from multimodal_market_ai.synthetic_demo import generate_synthetic_market, render_charts

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def main() -> None:
    market = generate_synthetic_market()
    paths = render_charts(market, OUTPUT_DIR / "images")
    for path in paths:
        print(f"chart -> {path}")


if __name__ == "__main__":
    main()
