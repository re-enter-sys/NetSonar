#!/usr/bin/env python3

import json
import math
import os
import time

import plotly.graph_objects as go
import streamlit as st


# ============================================================
# NETSONAR
# Network Traffic Sonification & Security Monitoring Console
# ============================================================


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

STATS_FILE = os.path.join(
    DATA_DIR,
    "live_stats.json"
)

AUDIO_FILE = os.path.join(
    DATA_DIR,
    "live_audio.json"
)

LOG_FILE = os.path.join(
    LOG_DIR,
    "network_events.log"
)


# ============================================================
# DASHBOARD SETTINGS
# ============================================================

REFRESH_SECONDS = 2
MAX_WAVEFORM_EVENTS = 40
SAMPLES_PER_EVENT = 100


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NetSonar SOC",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DARK SOC THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL APPLICATION
       ====================================================== */

    .stApp {
        background-color: #050505 !important;
        color: #f8fafc !important;
    }

    .main {
        background-color: #050505 !important;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ======================================================
       TEXT
       ====================================================== */

    p {
        color: #cbd5e1 !important;
        font-size: 16px;
    }

    h1 {
        color: #ffffff !important;
        font-size: 44px !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        margin-bottom: 5px !important;
    }

    h2 {
        color: #ffffff !important;
        font-size: 30px !important;
        font-weight: 750 !important;
        margin-top: 32px !important;
    }

    h3 {
        color: #f8fafc !important;
        font-size: 23px !important;
        font-weight: 700 !important;
    }


    /* ======================================================
       CAPTIONS
       ====================================================== */

    [data-testid="stCaptionContainer"] {
        color: #94a3b8 !important;
        font-size: 14px !important;
    }


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    [data-testid="stMetric"] {
        background-color: #0d0d0d !important;

        border: 1px solid #292929 !important;
        border-radius: 16px !important;

        padding: 22px !important;

        min-height: 145px;

        box-shadow:
            0 6px 22px rgba(0, 0, 0, 0.45);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);

        border-color: #2563eb !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;

        font-size: 15px !important;

        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;

        font-size: 36px !important;

        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 14px !important;
    }


    /* ======================================================
       SUCCESS / WARNING / ERROR / INFO
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 13px !important;

        background-color: #0a0a0a !important;

        border: 1px solid #292929 !important;

        color: #ffffff !important;

        padding: 15px !important;
    }

    div[data-testid="stAlert"] p {
        color: #f8fafc !important;

        font-size: 15px !important;

        font-weight: 650 !important;
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {
        background-color: #0d0d0d !important;

        border: 1px solid #292929 !important;

        border-radius: 14px !important;

        overflow: hidden;

        box-shadow:
            0 5px 20px rgba(0, 0, 0, 0.35);
    }


    /* ======================================================
       PLOTLY CONTAINERS
       ====================================================== */

    [data-testid="stPlotlyChart"] {
        background-color: #0d0d0d !important;

        border: 1px solid #292929 !important;

        border-radius: 16px !important;

        padding: 8px !important;

        box-shadow:
            0 6px 22px rgba(0, 0, 0, 0.40);
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    [data-testid="stExpander"] {
        background-color: #0d0d0d !important;

        border: 1px solid #292929 !important;

        border-radius: 14px !important;
    }

    [data-testid="stExpander"] summary {
        color: #ffffff !important;

        font-size: 16px !important;

        font-weight: 700 !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton button {
        background-color: #111111 !important;

        color: #ffffff !important;

        border: 1px solid #333333 !important;

        border-radius: 10px !important;

        font-size: 15px !important;

        font-weight: 650 !important;
    }

    .stButton button:hover {
        background-color: #171717 !important;

        border-color: #2563eb !important;

        color: #60a5fa !important;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: #292929 !important;
    }


    /* ======================================================
       CODE BLOCK
       ====================================================== */

    pre {
        background-color: #050505 !important;

        border: 1px solid #292929 !important;

        border-radius: 12px !important;
    }


    /* ======================================================
       SCROLLBAR
       ====================================================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #050505;
    }

    ::-webkit-scrollbar-thumb {
        background: #333333;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }


    /* ======================================================
       STREAMLIT FOOTER
       ====================================================== */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA FUNCTIONS
# ============================================================

def read_json_file(path, default):

    try:

        if not os.path.exists(path):
            return default

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError,
        TypeError
    ):

        return default


def read_stats():

    default = {
        "total_packets": 0,
        "total_bytes": 0,
        "packets_per_second": 0,
        "protocols": {},
        "unique_source_ips": 0,
        "unique_destination_ips": 0,
        "destination_ports": {}
    }

    data = read_json_file(
        STATS_FILE,
        default
    )

    if not isinstance(data, dict):
        return default

    return data


def read_audio():

    data = read_json_file(
        AUDIO_FILE,
        {"events": []}
    )

    if not isinstance(data, dict):
        return []

    events = data.get(
        "events",
        []
    )

    if not isinstance(events, list):
        return []

    return events


def read_security_events():

    events = []

    try:

        if not os.path.exists(LOG_FILE):
            return events

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if line:
                    events.append(line)

    except OSError:

        pass

    return events


def format_bytes(value):

    try:
        value = float(value)

    except (
        TypeError,
        ValueError
    ):

        return "0 B"

    if value >= 1024 * 1024:

        return (
            f"{value / (1024 * 1024):.2f} MB"
        )

    if value >= 1024:

        return (
            f"{value / 1024:.2f} KB"
        )

    return f"{int(value)} B"


def count_event(
    events,
    event_type
):

    return sum(
        1
        for event in events
        if f"TYPE={event_type}" in event
    )


def count_severity(
    events,
    severity
):

    return sum(
        1
        for event in events
        if f"SEVERITY={severity}" in event
    )


# ============================================================
# WAVEFORM GENERATION
# ============================================================

def generate_waveform(events):

    events = events[
        -MAX_WAVEFORM_EVENTS:
    ]

    x_values = []
    y_values = []

    current_time = 0.0

    for event in events:

        try:

            frequency = float(
                event.get(
                    "frequency",
                    440
                )
            )

            duration = float(
                event.get(
                    "duration",
                    0.08
                )
            )

            volume = float(
                event.get(
                    "volume",
                    0.2
                )
            )

        except (
            TypeError,
            ValueError
        ):

            continue

        duration = max(
            0.03,
            min(duration, 0.5)
        )

        samples = max(
            40,
            int(
                SAMPLES_PER_EVENT
                * duration
                / 0.08
            )
        )

        for index in range(samples):

            normalized = (
                index /
                max(samples - 1, 1)
            )

            local_time = (
                normalized *
                duration
            )

            envelope = math.sin(
                math.pi *
                normalized
            )

            amplitude = (
                volume *
                envelope
            )

            sample = (
                amplitude *
                math.sin(
                    2 *
                    math.pi *
                    frequency *
                    local_time
                )
            )

            x_values.append(
                current_time +
                local_time
            )

            y_values.append(
                sample
            )

        current_time += duration

    return (
        x_values,
        y_values
    )


# ============================================================
# LOAD LIVE DATA
# ============================================================

stats = read_stats()

audio_events = read_audio()

security_events = read_security_events()

protocols = stats.get(
    "protocols",
    {}
)

ports = stats.get(
    "destination_ports",
    {}
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🔊 NetSonar"
)

st.markdown(
    "### Network Traffic Sonification & Security Monitoring Console"
)

st.caption(
    "Real-time network visibility  •  "
    "Packet analysis  •  "
    "Threat detection  •  "
    "Audio telemetry"
)


header_left, header_right = st.columns(
    [4, 1]
)


with header_left:

    st.success(
        "🟢  LIVE MONITORING  •  Interface: eth0"
    )


with header_right:

    st.metric(
        "Refresh",
        f"{REFRESH_SECONDS}s"
    )


st.divider()


# ============================================================
# SYSTEM STATUS
# ============================================================

st.header(
    "🛰️ System Status"
)

status1, status2, status3, status4 = st.columns(4)


with status1:

    st.metric(
        "🌐 Network Interface",
        "eth0",
        "UP"
    )


with status2:

    st.metric(
        "📡 Packet Capture",
        "ACTIVE",
        "Scapy"
    )


with status3:

    if audio_events:

        st.metric(
            "🔊 Audio Telemetry",
            "ACTIVE",
            "Live events"
        )

    else:

        st.metric(
            "🔊 Audio Telemetry",
            "WAITING"
        )


with status4:

    if security_events:

        st.metric(
            "🛡️ Security Events",
            len(security_events),
            "Logged"
        )

    else:

        st.metric(
            "🛡️ Security Events",
            "CLEAR",
            "No events"
        )


# ============================================================
# NETWORK TELEMETRY
# ============================================================

st.header(
    "📡 Network Telemetry"
)

metric1, metric2, metric3, metric4 = st.columns(4)


with metric1:

    st.metric(
        "📦 Total Packets",
        f"{stats.get('total_packets', 0):,}"
    )


with metric2:

    st.metric(
        "💾 Traffic Volume",
        format_bytes(
            stats.get(
                "total_bytes",
                0
            )
        )
    )


with metric3:

    st.metric(
        "⚡ Packets / Second",
        stats.get(
            "packets_per_second",
            0
        )
    )


with metric4:

    st.metric(
        "🌍 Unique Sources",
        stats.get(
            "unique_source_ips",
            0
        )
    )


# ============================================================
# AUDIO INTELLIGENCE
# ============================================================

st.header(
    "🎧 Audio Intelligence"
)

st.caption(
    "Network packets are converted into "
    "frequency, amplitude and duration."
)


if audio_events:

    waveform_x, waveform_y = generate_waveform(
        audio_events
    )

    if waveform_x:

        waveform = go.Figure()

        waveform.add_trace(
            go.Scatter(
                x=waveform_x,
                y=waveform_y,
                mode="lines",
                name="Network Waveform",

                line=dict(
                    color="#00d9ff",
                    width=2.5
                ),

                fill="tozeroy",

                fillcolor=(
                    "rgba(0, 217, 255, 0.12)"
                ),

                hovertemplate=(
                    "Time: %{x:.2f}s"
                    "<br>Amplitude: %{y:.3f}"
                    "<extra></extra>"
                )
            )
        )

        waveform.update_layout(

            height=450,

            margin=dict(
                l=60,
                r=30,
                t=25,
                b=60
            ),

            paper_bgcolor="#0d0d0d",

            plot_bgcolor="#0d0d0d",

            xaxis=dict(

                title="Sonification Timeline",

                title_font=dict(
                    size=16,
                    color="#94a3b8"
                ),

                tickfont=dict(
                    size=13,
                    color="#94a3b8"
                ),

                gridcolor="#252525",

                zeroline=False
            ),

            yaxis=dict(

                title="Amplitude",

                title_font=dict(
                    size=16,
                    color="#94a3b8"
                ),

                tickfont=dict(
                    size=13,
                    color="#94a3b8"
                ),

                gridcolor="#252525",

                zeroline=True,

                zerolinecolor="#475569"
            ),

            showlegend=False,

            hovermode="x"
        )

        st.plotly_chart(
            waveform,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True
            }
        )

else:

    st.info(
        "🎧 Waiting for audio telemetry. "
        "Start NetSonar packet capture to generate waveform data."
    )


# ============================================================
# CURRENT AUDIO EVENT
# ============================================================

if audio_events:

    latest = audio_events[-1]

    st.subheader(
        "🔊 Latest Sound Event"
    )

    audio1, audio2, audio3, audio4, audio5 = st.columns(5)


    with audio1:

        st.metric(
            "Protocol",
            latest.get(
                "protocol",
                "UNKNOWN"
            )
        )


    with audio2:

        st.metric(
            "Frequency",
            f"{latest.get('frequency', 0)} Hz"
        )


    with audio3:

        st.metric(
            "Duration",
            f"{latest.get('duration', 0)} s"
        )


    with audio4:

        st.metric(
            "Volume",
            latest.get(
                "volume",
                0
            )
        )


    with audio5:

        st.metric(
            "Packet Size",
            f"{latest.get('packet_size', 0)} B"
        )


# ============================================================
# RECENT AUDIO EVENTS
# ============================================================

if audio_events:

    st.subheader(
        "🎚️ Recent Sonification Events"
    )

    audio_rows = []

    for event in reversed(
        audio_events[-15:]
    ):

        audio_rows.append(
            {
                "Time": event.get(
                    "timestamp",
                    ""
                ),

                "Protocol": event.get(
                    "protocol",
                    ""
                ),

                "Frequency": (
                    f"{event.get('frequency', 0)} Hz"
                ),

                "Duration": (
                    f"{event.get('duration', 0)} s"
                ),

                "Volume": event.get(
                    "volume",
                    0
                ),

                "Packet": (
                    f"{event.get('packet_size', 0)} B"
                ),

                "Status": (
                    "🚨 SECURITY"
                    if event.get("alert")
                    else "✓ NORMAL"
                )
            }
        )

    st.dataframe(
        audio_rows,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# NETWORK ANALYTICS
# ============================================================

st.header(
    "🌐 Network Analytics"
)

analytics_left, analytics_right = st.columns(2)


# ============================================================
# PROTOCOL ACTIVITY
# ============================================================

with analytics_left:

    st.subheader(
        "📊 Protocol Activity"
    )

    if protocols:

        protocol_items = sorted(
            protocols.items(),
            key=lambda item: item[1],
            reverse=True
        )

        protocol_names = [
            item[0]
            for item in protocol_items
        ]

        protocol_counts = [
            item[1]
            for item in protocol_items
        ]

        protocol_chart = go.Figure()

        protocol_chart.add_trace(
            go.Bar(

                x=protocol_names,

                y=protocol_counts,

                text=protocol_counts,

                textposition="outside",

                marker=dict(
                    color="#2563eb"
                ),

                hovertemplate=(
                    "%{x}"
                    "<br>Packets: %{y}"
                    "<extra></extra>"
                )
            )
        )

        protocol_chart.update_layout(

            height=400,

            margin=dict(
                l=55,
                r=30,
                t=30,
                b=65
            ),

            paper_bgcolor="#0d0d0d",

            plot_bgcolor="#0d0d0d",

            font=dict(
                color="#ffffff"
            ),

            xaxis=dict(

                title="Protocol",

                title_font=dict(
                    size=15,
                    color="#94a3b8"
                ),

                tickfont=dict(
                    size=13,
                    color="#cbd5e1"
                ),

                showgrid=False
            ),

            yaxis=dict(

                title="Packets",

                title_font=dict(
                    size=15,
                    color="#94a3b8"
                ),

                tickfont=dict(
                    size=13,
                    color="#cbd5e1"
                ),

                gridcolor="#252525"
            ),

            showlegend=False
        )

        st.plotly_chart(
            protocol_chart,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "No protocol telemetry available yet."
        )


# ============================================================
# DESTINATION PORTS
# ============================================================

with analytics_right:

    st.subheader(
        "🔌 Destination Port Activity"
    )

    if ports:

        port_items = sorted(
            ports.items(),
            key=lambda item: item[1],
            reverse=True
        )[:10]

        port_names = [
            str(item[0])
            for item in port_items
        ]

        port_counts = [
            item[1]
            for item in port_items
        ]

        port_chart = go.Figure()

        port_chart.add_trace(
            go.Bar(

                x=port_names,

                y=port_counts,

                text=port_counts,

                textposition="outside",

                marker=dict(
                    color="#00a8cc"
                ),

                hovertemplate=(
                    "Port %{x}"
                    "<br>Packets: %{y}"
                    "<extra></extra>"
                )
            )
        )

        port_chart.update_layout(

            height=400,

            margin=dict(
                l=55,
                r=30,
                t=30,
                b=65
            ),

            paper_bgcolor="#0d0d0d",

            plot_bgcolor="#0d0d0d",

            font=dict(
                color="#ffffff"
            ),

            xaxis=dict(

                title="Destination Port",

                title_font=dict(
                    size=15,
                    color="#94a3b8"
                ),

                tickfont=dict(
                    size=13,
                    color="#cbd5e1"
                ),

                showgrid=False
            ),

            yaxis=dict(

                title="Packets",

                title_font=dict(
                    size=15,
                    color="#94a3b8"
                ),

                tickfont=dict(
                    size=13,
                    color="#cbd5e1"
                ),

                gridcolor="#252525"
            ),

            showlegend=False
        )

        st.plotly_chart(
            port_chart,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "No destination-port telemetry available yet."
        )


# ============================================================
# SECURITY OPERATIONS CENTER
# ============================================================

st.header(
    "🛡️ Security Operations Center"
)

total_security_events = len(
    security_events
)

high_events = count_severity(
    security_events,
    "HIGH"
)

port_scans = count_event(
    security_events,
    "PORT_SCAN"
)

traffic_spikes = count_event(
    security_events,
    "TRAFFIC_SPIKE"
)


sec1, sec2, sec3, sec4 = st.columns(4)


with sec1:

    st.metric(
        "🚨 Security Events",
        total_security_events
    )


with sec2:

    st.metric(
        "🔴 High Severity",
        high_events
    )


with sec3:

    st.metric(
        "🔎 Port Scans",
        port_scans
    )


with sec4:

    st.metric(
        "📈 Traffic Spikes",
        traffic_spikes
    )


# ============================================================
# SECURITY STATE
# ============================================================

if high_events > 0:

    st.error(
        "🚨 SECURITY SIGNALS DETECTED — "
        "High-severity events have been recorded."
    )

elif total_security_events > 0:

    st.warning(
        "⚠️ SECURITY EVENTS LOGGED — "
        "Review the event history below."
    )

else:

    st.success(
        "🟢 SECURITY STATUS CLEAR — "
        "No security alerts have been logged."
    )


# ============================================================
# SECURITY EVENT FEED
# ============================================================

st.subheader(
    "🚨 Recent Security Events"
)

if security_events:

    for event in reversed(
        security_events[-10:]
    ):

        if "SEVERITY=HIGH" in event:

            st.error(
                f"🔴 {event}"
            )

        elif "SEVERITY=MEDIUM" in event:

            st.warning(
                f"🟠 {event}"
            )

        else:

            st.info(
                f"🔵 {event}"
            )

else:

    st.success(
        "✓ No security events recorded."
    )


# ============================================================
# RAW SECURITY LOG
# ============================================================

with st.expander(
    "📄 Open Raw Security Log"
):

    if security_events:

        st.code(
            "\n".join(
                security_events[-50:]
            ),
            language="text"
        )

    else:

        st.write(
            "Security log is empty."
        )


# ============================================================
# NETWORK SNAPSHOT
# ============================================================

st.header(
    "📋 Network Snapshot"
)

snapshot_left, snapshot_right = st.columns(2)


with snapshot_left:

    st.subheader(
        "🌍 Address Visibility"
    )

    st.metric(
        "Source IPs",
        stats.get(
            "unique_source_ips",
            0
        )
    )

    st.metric(
        "Destination IPs",
        stats.get(
            "unique_destination_ips",
            0
        )
    )


with snapshot_right:

    st.subheader(
        "🔌 Port Visibility"
    )

    st.metric(
        "Observed Ports",
        len(ports)
    )

    if ports:

        top_port = max(
            ports,
            key=ports.get
        )

        st.metric(
            "Most Active Port",
            str(top_port),
            f"{ports[top_port]} packets"
        )

    else:

        st.metric(
            "Most Active Port",
            "None"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🔊 NetSonar  •  "
    "Scapy + Streamlit + Plotly + ALSA  •  "
    "Network Traffic Sonification & Security Monitor"
)


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(
    REFRESH_SECONDS
)

st.rerun()
