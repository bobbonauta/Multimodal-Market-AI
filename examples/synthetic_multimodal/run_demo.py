from pathlib import Path

from multimodal_market_ai.synthetic_demo import write_demo

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def main() -> None:
    fusion = write_demo(OUTPUT_DIR)

    print("1. synthetic market data generated")
    print("2. 3 chart images rendered")
    print("3. deterministic features calculated")
    print("4. mock visual features produced")
    print("5. fusion table created")
    print("6. example decisions generated")
    print()
    print(fusion[["case_id", "det_signal", "visual_signal", "decision"]].to_string(index=False))


if __name__ == "__main__":
    main()
