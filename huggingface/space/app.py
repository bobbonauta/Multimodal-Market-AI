from pathlib import Path

import gradio as gr

from synthetic_demo import write_demo

OUTPUT = Path("demo_output")


def regenerate():
    fusion = write_demo(OUTPUT)
    columns = [
        "case_id",
        "trend_signal",
        "momentum_signal",
        "structure_signal",
        "mock_visual_score",
        "visual_signal",
        "det_signal",
        "decision",
    ]
    table = fusion[columns]
    gallery = [
        (str(OUTPUT / "images" / f"{case_id}.svg"), case_id)
        for case_id in fusion["case_id"]
    ]
    return table, gallery


initial_table, initial_gallery = regenerate()

with gr.Blocks() as demo:
    gr.Markdown(
        """
# Multimodal Market AI — synthetic CPU demo

Fake data only. The visual feature is a deterministic mock adapter used to show the fusion
contract. Replace it with a real VLM in your own research.

**This is not a trading bot or signal service.**
"""
    )
    table = gr.Dataframe(value=initial_table, interactive=False)
    gallery = gr.Gallery(value=initial_gallery, label="Synthetic chart cases", columns=3)
    button = gr.Button("Regenerate deterministic demo")
    button.click(regenerate, outputs=[table, gallery])

demo.launch()
