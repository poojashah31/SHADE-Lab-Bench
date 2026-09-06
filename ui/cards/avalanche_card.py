import math

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from core.sample_data import get_sample_report
from core.symmetric import compute_avalanche


def render_avalanche(ss):
    from ui.layout import explanation, zone_controls, zone_output
    plaintext = ss.get("aes_plaintext") or get_sample_report("default")
    key = ss.get("aes_key")
    iv = ss.get("aes_iv")

    col_controls, col_output = st.columns([1, 2])

    with col_controls:
        with zone_controls():
            st.markdown("#### Controls")
            st.caption(f"Plaintext: {len(plaintext)} bytes (from AES card if run, else sample)")
            byte_index = st.slider("Byte to flip", 0, min(len(plaintext) - 1, 63), 0)
            bit_index = st.slider("Bit within byte", 0, 7, 0)
            bit_mask = 1 << bit_index
            run = st.button("💥 Flip bit & measure avalanche", use_container_width=True)

    with col_output:
        with zone_output():
            st.markdown("#### Live output")
            if run:
                result = compute_avalanche(plaintext, key=key, iv=iv,
                                            byte_index=byte_index, bit_mask=bit_mask)
                ss["avalanche_result"] = result
                ss.setdefault("aes_key", result["key"])
                ss.setdefault("aes_iv", result["iv"])

                st.metric("Bits flipped", f"{result['bits_flipped']} / {result['total_bits']}",
                          f"{result['percentage']:.2f}%")
                st.caption("Optimal target: 45%–55% for good diffusion")

                fig = _render_bit_heatmap(result["total_bits"], result["diff_bits"])
                st.pyplot(fig, use_container_width=True)
            elif "avalanche_result" in ss:
                result = ss["avalanche_result"]
                st.metric("Bits flipped (last run)", f"{result['bits_flipped']} / {result['total_bits']}",
                          f"{result['percentage']:.2f}%")
                fig = _render_bit_heatmap(result["total_bits"], result["diff_bits"])
                st.pyplot(fig, use_container_width=True)
            else:
                st.caption("Click the button to flip a bit and see the ciphertext diff.")

    explanation(
        "Good ciphers exhibit the avalanche effect: changing a single input bit should "
        "flip roughly half of the output bits. This is what stops an attacker from "
        "learning anything from small, incremental changes to plaintext.",
        related_card_id="ecb_vs_cbc",
    )


def _render_bit_heatmap(total_bits: int, diff_bits: list):
    cols = 64
    rows = max(1, math.ceil(total_bits / cols))
    grid = np.zeros((rows, cols))
    for bit in diff_bits:
        r, c = divmod(bit, cols)
        grid[r, c] = 1

    from ui.theme import get_palette
    pal = get_palette()
    fig, ax = plt.subplots(figsize=(8, max(1.5, rows * 0.12)))
    fig.patch.set_facecolor(pal["bg_secondary"])
    ax.set_facecolor(pal["bg"])
    ax.imshow(grid, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Ciphertext bit differences (red = flipped)", fontsize=9,
                 color=pal["text_primary"])
    fig.tight_layout()
    return fig
