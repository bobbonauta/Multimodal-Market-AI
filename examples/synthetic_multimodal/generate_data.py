from pathlib import Path

from multimodal_market_ai.synthetic_demo import generate_synthetic_market

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    market = generate_synthetic_market()
    path = OUTPUT_DIR / "market.csv"
    market.to_csv(path, index=False)
    print(f"synthetic market data -> {path}")


if __name__ == "__main__":
    main()
