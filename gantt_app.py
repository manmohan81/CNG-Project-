import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Added a timestamp to help you verify the update
VERSION = "Updated: 12-June-2026 11:10 AM"

st.set_page_config(page_title="Dispenser Timeline - " + VERSION, layout="wide")

st.title("📊 Interactive Dispenser Gantt Chart")
st.caption(VERSION)
st.write("Adjust the **Start** and **End** dates below. The chart will update automatically.")

# Initial data
fixed_data = [
    {"Task": "Finalization of 2D/3D model", "Start": datetime(2026, 6, 11), "End": datetime(2026, 7, 29)},
    {"Task": "BOM Finalization", "Start": datetime(2026, 6, 11), "End": datetime(2026, 6, 14)},
    {"Task": "Part Order from Vendor", "Start": datetime(2026, 6, 15), "End": datetime(2026, 10, 5)},
    {"Task": "ECM import from China", "Start": datetime(2026, 6, 15), "End": datetime(2026, 9, 30)},
    {"Task": "Tools Setup for Factory", "Start": datetime(2026, 6, 15), "End": datetime(2026, 6, 21)},
    {"Task": "Testing Equipment Setup", "Start": datetime(2026, 6, 21), "End": datetime(2026, 7, 23)},
    {"Task": "Safety Equipment", "Start": datetime(2026, 7, 24), "End": datetime(2026, 7, 26)},
    {"Task": "Dispenser Cabinet", "Start": datetime(2026, 8, 29), "End": datetime(2026, 9, 24)},
    {"Task": "Hose Testing Equipment", "Start": datetime(2026, 7, 26), "End": datetime(2026, 9, 30)},
    {"Task": "Assembly", "Start": datetime(2026, 10, 10), "End": datetime(2026, 10, 15)},
    {"Task": "Dispenser Testing", "Start": datetime(2026, 10, 15), "End": datetime(2026, 10, 20)},
    {"Task": "Rain Testing Area", "Start": datetime(2026, 10, 25), "End": datetime(2026, 10, 30)},
    {"Task": "Dispenser Certification", "Start": datetime(2026, 8, 15), "End": datetime(2026, 12, 8)},
]

df_initial = pd.DataFrame(fixed_data)

st.subheader("1. Edit Timeline Dates")
edited_df = st.data_editor(
    df_initial,
    column_config={
        "Start": st.column_config.DateColumn("Start Date", format="DD-MM-YYYY", required=True),
        "End": st.column_config.DateColumn("End Date", format="DD-MM-YYYY", required=True),
    },
    hide_index=True,
    num_rows="dynamic",
)

# Convert to datetime
edited_df["Start"] = pd.to_datetime(edited_df["Start"], errors="coerce")
edited_df["End"] = pd.to_datetime(edited_df["End"], errors="coerce")

st.subheader("2. Project Schedule")

# Ignore incomplete rows added through the data editor.
chart_df = edited_df.dropna(subset=["Task", "Start", "End"]).copy()
chart_df = chart_df[chart_df["End"] >= chart_df["Start"]]

if not chart_df.empty:
    # Plotly graph_objects equivalent of plotly.express.timeline.
    # Durations are expressed in milliseconds because the x-axis is a date axis.
    tasks = chart_df["Task"].drop_duplicates().tolist()
    chart_df["Duration"] = (
        chart_df["End"] - chart_df["Start"]
    ).dt.total_seconds() * 1000

    fig = go.Figure(
        go.Bar(
            x=chart_df["Duration"],
            y=chart_df["Task"],
            base=chart_df["Start"],
            orientation="h",
            marker_color="#636EFA",
            customdata=chart_df[["Start", "End"]],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Start: %{customdata[0]|%d-%m-%Y}<br>"
                "End: %{customdata[1]|%d-%m-%Y}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        height=600,
        xaxis_title="Date",
        yaxis_title="",
        margin=dict(l=200),
        xaxis=dict(
            type="date",
            showline=True,
            linecolor="lightgray",
            linewidth=2,
            mirror=False,
        ),
        yaxis=dict(
            categoryorder="array",
            categoryarray=tasks,
            autorange="reversed",
            showline=True,
            linecolor="lightgray",
            linewidth=2,
            showgrid=True,
            gridcolor="#e6e6e6",
            gridwidth=1,
            zeroline=False,
            mirror=False,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please add tasks to see the chart.")

st.info("Tip: If you don't see the '11:10 AM' version, press 'Rerun' in the Streamlit menu.")
