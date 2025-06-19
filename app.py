import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import time
import streamlit.components.v1 as components

# --- App Config ---
st.set_page_config(page_title="Giám sát WSN tua-bin gió", layout="wide")

_SCROLL_SCRIPT = """
<script>
// Khôi phục vị trí cuộn
const y = sessionStorage.getItem("scrollPos");
if (y !== null) window.scrollTo(0, parseInt(y));
// Lưu vị trí cuộn liên tục
window.addEventListener("scroll", () => {
    sessionStorage.setItem("scrollPos", window.scrollY);
});
</script>
"""
components.html(_SCROLL_SCRIPT, height=0)

OMEGA = 0.1

# --- Sidebar: Điều khiển chung ---
st.sidebar.title("Điều khiển chung")
n_turbines = st.sidebar.slider("Số tua-bin", 1, 20, 6)
seconds_per_step = st.sidebar.slider("Bước lặp (giây)", 0.1, 2.0, 0.5, 0.1)
noise_std = st.sidebar.slider("Độ nhiễu (σ)", 0.0, 1.0, 0.25, 0.05)
failure_thresh = st.sidebar.slider("Ngưỡng hỏng", 0.0, 10.0, 5.0, 0.1)
wind_speed = st.sidebar.slider("Tốc độ gió (m/s)", 3, 25, 12)
max_hist = st.sidebar.slider("Lưu tối đa điểm", 100, 5000, 2000, 100)

# --- Cấu hình tua-bin ---
def default_turbine_config(n):
    return pd.DataFrame({
        "Amplitude": np.round(np.random.uniform(0.2, 0.5, n), 2),
        "PhaseShift": np.round(np.random.uniform(0, 2*np.pi, n), 2),
        "Enable": [True]*n
    })

with st.sidebar.expander("Cấu hình tua-bin", expanded=False):
    if "turbine_config" not in st.session_state or len(st.session_state["turbine_config"]) != n_turbines:
        st.session_state["turbine_config"] = default_turbine_config(n_turbines)
    config_df = st.data_editor(
        st.session_state["turbine_config"],
        key="turbine_config_editor",
        num_rows="dynamic",
        use_container_width=True
    )
    st.session_state["turbine_config"] = config_df.copy()

# --- Gây nhiễu ---
with st.sidebar.expander("Gây nhiễu", expanded=False):
    turbine_options = [f"T{i+1}" for i in range(n_turbines)]
    target = st.selectbox("Chọn tua-bin", turbine_options + ["Tất cả"], key="fault_target")
    intensity = st.slider("Cường độ", 0, 5, 1, 1, key="fault_intensity")
    if st.button("💥 Kích hoạt", use_container_width=True, key="fault_btn"):
        end_time = time.time() + 10
        st.session_state["fault"] = {"target": target, "intensity": intensity, "end_time": end_time}
        st.toast(f"💥 Đã gây nhiễu {target} với cường độ {intensity}", icon="💥")

# --- Sidebar: Simulation Controls ---
c1, c2, c3, c4 = st.sidebar.columns([1,1,1,1])
if c1.button("▶ Bắt đầu", use_container_width=True):
    st.session_state["running"] = True
    if "prog" not in st.session_state:
        st.session_state["prog"] = st.progress(0)
if c2.button("⏸ Tạm dừng", use_container_width=True):
    st.session_state["running"] = False
    if "prog" in st.session_state:
        st.session_state["prog"].empty()
if c3.button("🛑 Dừng", use_container_width=True):
    st.session_state["running"] = False
    st.session_state["data_store"] = None
    st.session_state["alert_log"] = []
    st.session_state["selected"] = 0
if c4.button("⏹ Đặt lại", use_container_width=True):
    st.session_state["running"] = False
    st.session_state["data_store"] = None
    st.session_state["alert_log"] = []
    st.session_state["selected"] = 0

# --- Data store ---
def init_store(n):
    return {
        "vibration":   {f"T{i+1}": [] for i in range(n)},
        "temperature": {f"T{i+1}": [] for i in range(n)},
        "rpm":         {f"T{i+1}": [] for i in range(n)},
        "power_kw":    {f"T{i+1}": [] for i in range(n)},
        "prob_fail":   {f"T{i+1}": [] for i in range(n)}
    }

def append_point(t_id, vib, temp, rpm, power, p_fail):
    ds = st.session_state["data_store"]
    for arr, val in zip([
        ds["vibration"], ds["temperature"], ds["rpm"], ds["power_kw"], ds["prob_fail"]
    ], [vib, temp, rpm, power, p_fail]):
        arr[t_id].append(val)
    # Cap history
    for k in ds:
        if len(ds[k][t_id]) > max_hist:
            ds[k][t_id] = ds[k][t_id][-max_hist:]

# --- Session State Initialization ---
if (
    "data_store" not in st.session_state
    or st.session_state["data_store"] is None
    or len(st.session_state["data_store"]["vibration"]) != n_turbines
):
    st.session_state["data_store"] = init_store(n_turbines)
if "selected" not in st.session_state:
    st.session_state["selected"] = 0
if "alert_log" not in st.session_state:
    st.session_state["alert_log"] = []
if "running" not in st.session_state:
    st.session_state["running"] = True

# --- Simulation Step ---
def sim_step():
    ds = st.session_state["data_store"]
    t_now = time.time()
    fault = st.session_state.get("fault", None)
    for i in range(n_turbines):
        t_id = f"T{i+1}"
        enabled = bool(st.session_state["turbine_config"].iloc[i]["Enable"])
        A = float(st.session_state["turbine_config"].iloc[i]["Amplitude"])
        phi = float(st.session_state["turbine_config"].iloc[i]["PhaseShift"])
        if enabled:
            t = len(ds["vibration"][t_id]) * seconds_per_step
            baseline = 0.02 * t
            vib = baseline + A * np.sin(OMEGA * t + phi) + np.random.normal(0, noise_std)
            # Fault injection
            if fault and t_now < fault["end_time"]:
                if fault["target"] == t_id or fault["target"] == "Tất cả":
                    vib += fault["intensity"]
            temp = 25 + 0.4 * vib + np.random.normal(0, noise_std)
            rpm = wind_speed * 0.8 + 4 * np.sin(OMEGA * t + phi) + np.random.normal(0, noise_std)
            power_kw = rpm * 0.9
            p_fail = 1 / (1 + np.exp(-(vib - failure_thresh)))
        else:
            vib = temp = rpm = power_kw = p_fail = np.nan
        # Alert log + toast
        prev = ds["prob_fail"][t_id][-1] if ds["prob_fail"][t_id] else 0
        append_point(t_id, vib, temp, rpm, power_kw, p_fail)
        if p_fail > 0.5 and prev <= 0.5:
            msg = f"⚠ {t_id} vượt ngưỡng hỏng!"
            st.session_state["alert_log"].append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "turbine": t_id,
                "msg": msg
            })
            st.session_state["alert_log"] = st.session_state["alert_log"][-500:]
            st.toast(msg, icon="⚠")

# --- Data Extraction ---
def get_latest_metrics():
    ds = st.session_state["data_store"]
    rows = []
    for i in range(n_turbines):
        t_id = f"T{i+1}"
        enabled = bool(st.session_state["turbine_config"].iloc[i]["Enable"])
        def safe(arr):
            return arr[t_id][-1] if arr[t_id] and not np.isnan(arr[t_id][-1]) else np.nan
        rows.append({
            "Tua-bin": t_id,
            "Hoạt động": enabled,
            "Độ rung": safe(ds["vibration"]),
            "Nhiệt độ": safe(ds["temperature"]),
            "RPM": safe(ds["rpm"]),
            "Công suất (kW)": safe(ds["power_kw"]),
            "Xác suất hỏng": safe(ds["prob_fail"])
        })
    return pd.DataFrame(rows)

def get_log_df():
    ds = st.session_state["data_store"]
    if len(ds["vibration"]["T1"]) == 0:
        return pd.DataFrame()
    records = []
    for i in range(n_turbines):
        t_id = f"T{i+1}"
        n = len(ds["vibration"][t_id])
        for j in range(n):
            records.append({
                "Thời gian": j * seconds_per_step,
                "Tua-bin": t_id,
                "Độ rung": ds["vibration"][t_id][j],
                "Nhiệt độ": ds["temperature"][t_id][j],
                "RPM": ds["rpm"][t_id][j],
                "Công suất (kW)": ds["power_kw"][t_id][j],
                "Xác suất hỏng": ds["prob_fail"][t_id][j]
            })
    return pd.DataFrame(records)

# --- Tabs Layout ---
tabs = st.tabs(["Bảng điều khiển", "Mạng WSN", "Chi tiết tua-bin", "Bảng dữ liệu"])

# --- Dashboard Tab ---
with tabs[0]:
    st.subheader("Bảng điều khiển WSN tua-bin gió")
    ds = st.session_state["data_store"]
    # --- Progress bar động ---
    if "prog" not in st.session_state:
        st.session_state["prog"] = st.progress(0)
    else:
        total_steps = 1000
        curr = len(ds["vibration"]["T1"])
        st.session_state["prog"].progress(min(100, int(curr/total_steps*100)))
    if len(ds["vibration"]["T1"]) == 0:
        st.info("Chưa bắt đầu mô phỏng, hãy nhấn Bắt đầu.")
    else:
        df = get_latest_metrics()
        total_power = df["Công suất (kW)"].sum(skipna=True)
        turbines_online = df["Hoạt động"].sum()
        risk_count = df[(df["Xác suất hỏng"] > 0.5) & (df["Hoạt động"] == True)].shape[0]
        risk_pct = 100 * risk_count / turbines_online if turbines_online else 0
        if risk_count > 0:
            st.toast(f"⚠ Có {risk_count} tua-bin vượt ngưỡng hỏng!", icon="⚠")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Tổng công suất (kW)", f"{total_power:.1f}")
        k2.metric("Tua-bin hoạt động", f"{turbines_online}/{n_turbines}")
        k3.metric("Tua-bin rủi ro (%)", f"{risk_pct:.0f}%")
        sim_time = len(ds["vibration"]["T1"]) * seconds_per_step
        k4.metric("Thời gian mô phỏng", f"{sim_time:.1f} s")
        # Plotly Gauge
        avg_vib = df["Độ rung"].mean(skipna=True)
        gauge_color = "green" if avg_vib < 3 else ("orange" if avg_vib < 6 else "red")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_vib if not np.isnan(avg_vib) else 0,
            title={"text": "Độ rung trung bình"},
            gauge={
                "axis": {"range": [0, 10]},
                "bar": {"color": gauge_color}
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        # Tổng công suất theo thời gian
        t_arr = [j * seconds_per_step for j in range(len(ds["vibration"]["T1"]))]
        power_arr = [sum([ds["power_kw"][f"T{i+1}"][j] if j < len(ds["power_kw"][f"T{i+1}"]) and not np.isnan(ds["power_kw"][f"T{i+1}"][j]) else 0 for i in range(n_turbines)]) for j in range(len(t_arr))]
        fig_power = go.Figure()
        fig_power.add_trace(go.Scatter(
            x=t_arr, y=power_arr, mode="lines", fill="tozeroy",
            name="Tổng công suất"
        ))
        fig_power.update_layout(title="Tổng công suất theo thời gian", xaxis_title="Thời gian (s)", yaxis_title="Công suất (kW)")
        st.plotly_chart(fig_power, use_container_width=True)
        # Download log as CSV
        log_df = get_log_df()
        csv = log_df.to_csv(index=False).encode('utf-8')
        st.download_button("Tải log CSV", csv, "turbine_log.csv", "text/csv")

# --- Network View Tab ---
with tabs[1]:
    st.subheader("Mạng WSN - Topology")
    @st.cache_data(ttl=0, max_entries=3)
    def get_layout(n):
        G = nx.Graph()
        G.add_node("Gateway")
        for i in range(n):
            G.add_node(f"T{i+1}")
            G.add_edge("Gateway", f"T{i+1}")
        pos = nx.spring_layout(G, seed=42)
        return G, pos
    G, pos = get_layout(n_turbines)
    node_x, node_y, node_color, node_text = [], [], [], []
    for i, node in enumerate(G.nodes()):
        if node == "Gateway":
            node_x.append(pos[node][0]); node_y.append(pos[node][1])
            node_color.append("#636efa"); node_text.append("Gateway")
        else:
            idx = int(node[1:]) - 1
            enabled = bool(st.session_state["turbine_config"].iloc[idx]["Enable"])
            t_id = f"T{idx+1}"
            pf = ds["prob_fail"][t_id][-1] if ds["prob_fail"][t_id] else 0
            if not enabled:
                color = "#888"
            elif pf > 0.5:
                color = "#ef553b"
            else:
                color = "#00cc96"
            node_x.append(pos[node][0]); node_y.append(pos[node][1])
            node_color.append(color)
            node_text.append(node)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]; x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]; edge_y += [y0, y1, None]
    fig_net = go.Figure()
    fig_net.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1, color='#888'), hoverinfo='none'))
    fig_net.add_trace(go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        marker=dict(size=30, color=node_color),
        text=node_text, textposition="bottom center",
        hoverinfo='text',
        customdata=[n for n in G.nodes()],
    ))
    fig_net.update_layout(
        showlegend=False, margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        title="Mạng sao: Gateway & Tua-bin"
    )
    st.plotly_chart(fig_net, use_container_width=True, key="net")

# --- Turbine Detail Tab ---
with tabs[2]:
    st.subheader("Chi tiết tua-bin")
    options = [f"T{i+1}" for i in range(n_turbines)]
    sel_idx = st.session_state.get("selected", 0)
    sel = st.selectbox("Chọn tua-bin", options, index=sel_idx)
    idx = options.index(sel)
    st.session_state["selected"] = idx
    t_id = options[idx]
    # Status badge
    pf = ds["prob_fail"][t_id][-1] if ds["prob_fail"][t_id] else 0
    enabled = bool(st.session_state["turbine_config"].iloc[idx]["Enable"])
    badge = "✅ Ổn định" if enabled and pf <= 0.5 else ("⚠ Rủi ro cao" if enabled else "Đã tắt")
    st.markdown(f"**Trạng thái:** {badge}")
    t_arr = [j * seconds_per_step for j in range(len(ds["vibration"][t_id]))]
    if len(t_arr) == 0:
        st.info("Chưa có dữ liệu cho tua-bin này.")
    else:
        fig = make_subplots(rows=2, cols=2, subplot_titles=("Độ rung", "Nhiệt độ", "RPM", "Công suất (kW)"))
        fig.add_trace(go.Scatter(x=t_arr, y=ds["vibration"][t_id], name="Độ rung"), row=1, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=ds["temperature"][t_id], name="Nhiệt độ"), row=1, col=2)
        fig.add_trace(go.Scatter(x=t_arr, y=ds["rpm"][t_id], name="RPM"), row=2, col=1)
        fig.add_trace(go.Scatter(x=t_arr, y=ds["power_kw"][t_id], name="Công suất (kW)"), row=2, col=2)
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# --- Data Table Tab ---
with tabs[3]:
    st.subheader("Bảng dữ liệu tua-bin")
    ds = st.session_state["data_store"]
    if len(ds["vibration"]["T1"]) == 0:
        st.info("Chưa có dữ liệu để hiển thị.")
    else:
        df = get_latest_metrics()
        show_alert = st.checkbox("Hiện lịch sử cảnh báo", value=False)
        if show_alert:
            st.dataframe(pd.DataFrame(st.session_state["alert_log"]), use_container_width=True)
        def highlight_risk_row(row):
            return ['background-color:#ffcccc' if row["Xác suất hỏng"] > 0.5 else '' ]*len(row)
        styled = df.style.apply(highlight_risk_row, axis=1)
        st.dataframe(styled, use_container_width=True, hide_index=True)

# --- Auto-refresh ---
if st.session_state.get("running", False):
    sim_step()
    # st.autorefresh(interval=int(seconds_per_step*1000), key="auto")

# --- Fallback refresh cho Streamlit < 1.25 ---
if st.session_state.get("running", False):
    try:
        st.autorefresh(interval=int(seconds_per_step*1000), key="auto")
    except AttributeError:
        import time
        time.sleep(seconds_per_step)
        st.rerun()

# Run: streamlit run app.py