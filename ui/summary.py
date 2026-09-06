import streamlit as st

from ui.registry import CARDS, LAYER_LABELS, LAYER_ORDER, cards_in_layer
from ui.state import card_status, open_dashboard


def render_summary():
    if st.button("← Back to bench"):
        open_dashboard()
        st.rerun()

    st.title("📋 Results Summary")
    st.caption("Mirrors the CLI's option 16 -- a pass/fail snapshot across every card.")

    done = sum(1 for c in CARDS if card_status(c) == "done")
    implemented = sum(1 for c in CARDS if c.render is not None)
    st.metric("Cards completed", f"{done} / {len(CARDS)}",
              f"{implemented} implemented so far")

    for layer in LAYER_ORDER:
        st.markdown(f"### {LAYER_LABELS[layer]}")
        for card in cards_in_layer(layer):
            status = card_status(card)
            icon = {"done": "✅", "locked": "🔒", "not_started": "⬜"}[status]
            note = "" if card.render is not None else "  _(coming soon)_"
            st.markdown(f"{icon} **{card.title}**{note}")
