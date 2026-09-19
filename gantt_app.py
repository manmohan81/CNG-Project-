import streamlit as st
import pandas as pd
import plotly.express as px
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
    {"Task": "Part Order from Vendor", "Start": datetime(2026, 6, 15), "End": datetime(2026,10, 5)},
    {"Task": "ECM import from China", "Start": datetime(2026, 6, 15), "End": datetime(2026,9, 30)},
    {"Task": "Tools Setup for Factory", "Start": datetime(2026, 6, 15), "End": datetime(2026, 6, 21)},
    {"Task": "Testing Equipment Setup", "Start": datetime(2026, 6, 21), "End": datetime(2026, 9, 30)},
    {"Task": "Safety Equipment", "Start": datetime(2026, 7, 24), "End": datetime(2026, 7, 26)},
    {"Task": "Dispenser Cabinet", "Start": datetime(2026, 8, 29), "End": datetime(2026, 9, 30)},
    {"Task": "Hose Testing Equipment", "Start": datetime(2026, 7, 26), "End": datetime(2026,10, 5)},     
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
    num_rows="dynamic"
)

# Convert to datetime
edited_df["Start"] = pd.to_datetime(edited_df["Start"])
edited_df["End"] = pd.to_datetime(edited_df["End"])

st.subheader("2. Project Schedule")

if not edited_df.empty:
    # REVERSE the task list for the chart
    # index 0 (2D/3D model) will be at the TOP
    tasks = edited_df["Task"].unique().tolist()

    fig = px.timeline(
        edited_df,
        x_start="Start",
        x_end="End",
        y="Task",
        color="Task",
        template="plotly_white",
        category_orders={"Task": tasks[::1]} # This puts the first item of 'tasks' at the TOP
    )

    # Add monthly vertical guide lines across the chart
    month_starts = pd.date_range(
        start=edited_df["Start"].min().to_period("M").to_timestamp(),
        end=edited_df["End"].max().to_period("M").to_timestamp(),
        freq="MS"
    )

    for month_start in month_starts:
        fig.add_vline(
            x=month_start,
            line_color="rgba(100, 100, 100, 0.35)",
            line_width=1,
            line_dash="dot"
        )

    # Add date labels at the start and end of each task bar
    for task in tasks:
        task_record = edited_df[edited_df["Task"] == task].iloc[0]
        start = pd.to_datetime(task_record["Start"])
        end = pd.to_datetime(task_record["End"])
        duration_days = (end - start).days

        # For very short tasks, place labels outside the bar to avoid overlap.
        if duration_days <= 7:
            start_x = start - pd.Timedelta(days=1)
            end_x = end + pd.Timedelta(days=1)
            start_anchor = "right"
            end_anchor = "left"
            start_shift = -4
            end_shift = 4
        else:
            start_x = start
            end_x = end
            start_anchor = "left"
            end_anchor = "right"
            start_shift = 4
            end_shift = -4

        fig.add_annotation(
            x=start_x,
            y=task,
            text=start.strftime("%d %b"),
            showarrow=False,
            font=dict(size=9, color="#333333"),
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor="rgba(0,0,0,0.15)",
            borderwidth=1,
            xref="x",
            yref="y",
            xanchor=start_anchor,
            yanchor="middle",
            xshift=start_shift,
            yshift=0
        )

        fig.add_annotation(
            x=end_x,
            y=task,
            text=end.strftime("%d %b"),
            showarrow=False,
            font=dict(size=9, color="#333333"),
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor="rgba(0,0,0,0.15)",
            borderwidth=1,
            xref="x",
            yref="y",
            xanchor=end_anchor,
            yanchor="middle",
            xshift=end_shift,
            yshift=0
        )

    fig.update_layout(
        showlegend=False,
        height=600,
        xaxis_title="Date",
        yaxis_title="",
        margin=dict(l=200),

        xaxis=dict(
            showline=True,
            linecolor="lightgray",
            linewidth=2,
            mirror=False,
            type="date",
            tickformat="%d %b %Y",
            tickangle=-30,
            showgrid=True,
            gridcolor="#e6e6e6",
            gridwidth=1
        ),
        yaxis=dict(
            showline=True,
            linecolor="lightgray",
            linewidth=2,
            showgrid=True,
            gridcolor="#e6e6e6",
            gridwidth=1,
            zeroline=False,
            mirror=False
        )
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please add tasks to see the chart.")

st.info("Tip: If you don't see the '11:10 AM' version, press 'Rerun' in the Streamlit menu.")
