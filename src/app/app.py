"""
Olist DW & DSS Streamlit dashboard.

UI-only layer: every piece of data comes from src/app/queries.py (SQL over the
processed SQLite DW) or the three DSS modules in src/dss/. This file never reads
a CSV or the database directly.
"""
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src" / "dss"))
sys.path.insert(0, str(REPO / "src" / "app"))

import queries as q  # noqa: E402
import forecast as fc  # noqa: E402
import rfm as rfm_mod  # noqa: E402
import whatif as wi  # noqa: E402


# --------------------------------------------------------------------------- cached wrappers
@st.cache_data
def _available_years():
    return q.available_years()


@st.cache_data
def _available_states():
    return q.available_states()


@st.cache_data
def _available_categories():
    return q.available_categories()


@st.cache_data
def _kpi_summary():
    return q.kpi_summary()


@st.cache_data
def _monthly_revenue():
    return q.monthly_revenue()


@st.cache_data
def _rollup_by_year():
    return q.rollup_by_year()


@st.cache_data
def _drilldown_by_month(year: int):
    return q.drilldown_by_month(year)


@st.cache_data
def _slice_by_category(year: int):
    return q.slice_by_category(year)


@st.cache_data
def _dice_states_categories(states, categories, year):
    return q.dice_states_categories(states, categories, year)


@st.cache_data
def _pivot_category_by_year():
    return q.pivot_category_by_year()


@st.cache_data
def _revenue_review_by_state():
    return q.revenue_review_by_state()


@st.cache_data
def _payment_mix():
    return q.payment_mix()


@st.cache_data
def _delivery_vs_review():
    return q.delivery_vs_review()


@st.cache_data
def _delivery_vs_review_by_state():
    return q.delivery_vs_review_by_state()


@st.cache_data
def _delivery_vs_review_by_category():
    return q.delivery_vs_review_by_category()


@st.cache_data
def _category_revenue_summary():
    return q.category_revenue_summary()


@st.cache_data
def _delivery_late_rate():
    return q.delivery_late_rate()


@st.cache_data(show_spinner=False)
def _run_forecast():
    return fc.run_forecast()


@st.cache_data(show_spinner=False)
def _run_rfm():
    return rfm_mod.run_rfm()


# --------------------------------------------------------------------------- page 1: Tổng quan
def page_overview():
    st.header("Tổng quan")

    kpi = _kpi_summary()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Doanh thu", f"{kpi['revenue']:,.0f}")
    c2.metric("Số đơn", f"{kpi['orders']:,.0f}")
    c3.metric("Giá trị đơn TB", f"{kpi['avg_order_value']:,.2f}")
    c4.metric("Điểm đánh giá TB", f"{kpi['avg_review']:,.2f}")
    c5.metric("% Giao trễ", f"{kpi['pct_late']:,.2f}%")

    st.subheader("Doanh thu theo tháng")
    mr = _monthly_revenue()
    fig = px.line(mr, x="year_month", y="revenue", markers=True,
                   labels={"year_month": "Tháng", "revenue": "Doanh thu"})
    st.plotly_chart(fig, width='stretch')


# --------------------------------------------------------------------------- page 2: OLAP
def page_olap():
    st.header("Phân tích đa chiều (OLAP)")
    years = _available_years()

    # --- Roll-up ---
    st.subheader("Roll-up")
    st.caption("Roll-up: tổng hợp doanh thu từ mức tháng lên mức năm.")
    ry = _rollup_by_year()
    fig = px.bar(ry, x="year", y="revenue", text_auto=".2s",
                 labels={"year": "Năm", "revenue": "Doanh thu"})
    st.plotly_chart(fig, width='stretch')
    st.dataframe(ry, width='stretch')

    # --- Drill-down ---
    st.subheader("Drill-down")
    st.caption("Drill-down: chọn một năm, xem chi tiết theo quý và tháng.")
    dd_year = st.selectbox("Chọn năm để drill-down", years,
                            index=len(years) - 1 if years else 0, key="dd_year")
    dd = _drilldown_by_month(dd_year)
    fig = px.bar(dd, x="year_month", y="revenue", color="quarter",
                 labels={"year_month": "Tháng", "revenue": "Doanh thu", "quarter": "Quý"})
    st.plotly_chart(fig, width='stretch')

    # --- Slice ---
    st.subheader("Slice")
    slice_year = st.selectbox("Chọn năm", years,
                               index=len(years) - 1 if years else 0, key="slice_year")
    st.caption(f"Slice: cố định năm = {slice_year}, xem doanh thu theo danh mục sản phẩm.")
    sl = _slice_by_category(slice_year)
    fig = px.bar(sl, x="category_en", y="revenue",
                 labels={"category_en": "Danh mục", "revenue": "Doanh thu"})
    st.plotly_chart(fig, width='stretch')

    # --- Dice ---
    st.subheader("Dice")
    st.caption("Dice: cắt một khối con theo nhiều bang và nhiều danh mục được chọn.")
    states = _available_states()
    categories = _available_categories()
    sel_states = st.multiselect("Chọn bang (state)", states,
                                 default=states[:3] if len(states) >= 3 else states)
    sel_categories = st.multiselect("Chọn danh mục", categories,
                                     default=categories[:3] if len(categories) >= 3 else categories)
    year_options = ["Tất cả"] + years
    dice_year_choice = st.selectbox("Chọn năm (tùy chọn)", year_options, key="dice_year")
    dice_year = None if dice_year_choice == "Tất cả" else dice_year_choice

    if sel_states and sel_categories:
        dc = _dice_states_categories(tuple(sel_states), tuple(sel_categories), dice_year)
        fig = px.bar(dc, x="customer_state", y="revenue", color="category_en", barmode="group",
                     labels={"customer_state": "Bang", "revenue": "Doanh thu", "category_en": "Danh mục"})
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Chọn ít nhất một bang và một danh mục để xem kết quả dice.")

    # --- Pivot ---
    st.subheader("Pivot")
    st.caption("Pivot: danh mục x năm.")
    pv = _pivot_category_by_year()
    st.dataframe(pv, width='stretch')


# --------------------------------------------------------------------------- page 3: Địa lý & khách hàng
def page_geo_customer():
    st.header("Địa lý & khách hàng")

    st.subheader("Doanh thu & điểm đánh giá theo bang")
    rrs = _revenue_review_by_state().sort_values("revenue", ascending=False)
    fig = px.bar(rrs, x="customer_state", y="revenue", color="avg_review",
                 color_continuous_scale="RdYlGn",
                 labels={"customer_state": "Bang", "revenue": "Doanh thu", "avg_review": "Điểm đánh giá TB"})
    st.plotly_chart(fig, width='stretch')
    st.dataframe(rrs, width='stretch')

    st.subheader("Cơ cấu phương thức thanh toán")
    pm = _payment_mix()
    fig = px.pie(pm, names="payment_type", values="revenue",
                  labels={"payment_type": "Phương thức", "revenue": "Doanh thu"})
    st.plotly_chart(fig, width='stretch')


# --------------------------------------------------------------------------- page 4: Giao hàng & hài lòng
def page_delivery():
    st.header("Giao hàng & hài lòng")

    st.subheader("Giao trễ vs. đúng hạn")
    dvr = _delivery_vs_review()
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(dvr, x="delivery", y="avg_review",
                     labels={"delivery": "Tình trạng giao hàng", "avg_review": "Điểm đánh giá TB"})
        st.plotly_chart(fig, width='stretch')
    with c2:
        fig = px.bar(dvr, x="delivery", y="avg_delivery_days",
                     labels={"delivery": "Tình trạng giao hàng", "avg_delivery_days": "Số ngày giao TB"})
        st.plotly_chart(fig, width='stretch')

    st.subheader("Theo bang (top 10 bang theo số lượng)")
    dvs = _delivery_vs_review_by_state()
    top_states = dvs.groupby("customer_state")["items"].sum().sort_values(ascending=False).head(10).index
    dvs_top = dvs[dvs.customer_state.isin(top_states)]
    fig = px.bar(dvs_top, x="customer_state", y="avg_review", color="delivery", barmode="group",
                 labels={"customer_state": "Bang", "avg_review": "Điểm đánh giá TB", "delivery": "Tình trạng"})
    st.plotly_chart(fig, width='stretch')

    st.subheader("Theo danh mục (top 10 danh mục)")
    dvc = _delivery_vs_review_by_category()
    fig = px.bar(dvc, x="category_en", y="avg_review", color="delivery", barmode="group",
                 labels={"category_en": "Danh mục", "avg_review": "Điểm đánh giá TB", "delivery": "Tình trạng"})
    st.plotly_chart(fig, width='stretch')


# --------------------------------------------------------------------------- page 5: Dự báo & DSS
def page_dss():
    st.header("Dự báo & DSS")

    # --- Forecast ---
    st.subheader("Dự báo doanh thu")
    with st.spinner("Đang chạy mô hình dự báo..."):
        fr = _run_forecast()

    hist = fr.history.copy()
    test_df = pd.DataFrame({
        "year_month": fr.test_months,
        "actual": hist.set_index("year_month").loc[fr.test_months, "revenue"].values,
        "naive_pred": fr.naive_pred,
        "holt_pred": fr.holt_pred,
    })

    plot_df = hist.rename(columns={"revenue": "Thực tế"})[["year_month", "Thực tế"]]
    plot_df = plot_df.merge(
        test_df[["year_month", "naive_pred", "holt_pred"]].rename(
            columns={"naive_pred": "Baseline (TB trượt)", "holt_pred": "Holt (xu hướng)"}),
        on="year_month", how="left")
    plot_long = plot_df.melt(id_vars="year_month", var_name="series", value_name="revenue").dropna()
    fig = px.line(plot_long, x="year_month", y="revenue", color="series", markers=True,
                   labels={"year_month": "Tháng", "revenue": "Doanh thu", "series": "Chuỗi"})
    st.plotly_chart(fig, width='stretch')

    mae_table = pd.DataFrame({
        "model": ["Baseline (trung bình trượt)", "Holt (xu hướng tuyến tính)"],
        "MAE": [fr.naive_mae, fr.holt_mae],
        "MAPE (%)": [fr.naive_mape, fr.holt_mape],
    })
    st.dataframe(mae_table, width='stretch')

    st.write(
        f"**Dự báo tháng kế tiếp (Holt):** {fr.holt_forecast_next:,.2f} "
        f"(khoảng tin cậy 95%: {fr.holt_forecast_ci[0]:,.2f} .. {fr.holt_forecast_ci[1]:,.2f})"
    )
    st.warning(
        "Chuỗi dữ liệu chỉ có 20 tháng, chưa đủ 2 chu kỳ mùa vụ nên không thể áp dụng mô hình "
        "mùa vụ một cách đáng tin cậy. Trên dữ liệu hiện tại, mô hình Holt (xu hướng) đang có sai số "
        "(MAE/MAPE) CAO HƠN baseline đơn giản, vì tăng trưởng doanh thu chững lại/giảm sau đỉnh "
        "Black Friday tháng 11/2017 khiến mô hình xu hướng dự báo vượt quá thực tế. Vì vậy không nên "
        "quảng cáo quá mức độ chính xác của mô hình Holt ở giai đoạn này."
    )

    st.divider()

    # --- RFM ---
    st.subheader("Phân khúc khách hàng (RFM + K-Means)")
    with st.spinner("Đang chạy phân cụm K-Means (có thể mất 10-20 giây)..."):
        rr = _run_rfm()

    st.write(f"Số cụm K đã chọn: **{rr.k}** (silhouette = {rr.silhouette:.3f})")
    st.dataframe(rr.segment_profile, width='stretch')

    fig = px.bar(rr.segment_profile, x="segment_name", y="size",
                 labels={"segment_name": "Phân khúc", "size": "Số khách hàng"})
    st.plotly_chart(fig, width='stretch')

    st.markdown("**Hành động đề xuất theo phân khúc:**")
    for seg in rr.segment_profile["segment_name"]:
        action = rr.segment_actions.get(seg)
        if action:
            st.write(f"- **{seg}**: {action}")

    st.markdown("**Căn cứ chọn K (elbow & silhouette):**")
    k_df = pd.DataFrame({
        "k": list(rr.elbow_inertias.keys()),
        "inertia": list(rr.elbow_inertias.values()),
        "silhouette": [rr.silhouette_scores[k] for k in rr.elbow_inertias.keys()],
    })
    st.dataframe(k_df, width='stretch')
    fig = px.line(k_df, x="k", y="inertia", markers=True,
                   labels={"k": "K", "inertia": "Inertia"})
    st.plotly_chart(fig, width='stretch')

    st.divider()

    # --- What-if: delivery ---
    st.subheader("What-if: Giảm tỷ lệ giao trễ")
    current_late = _delivery_late_rate()
    target_late = st.slider("Tỷ lệ giao trễ mục tiêu (%)", 0.0, 100.0,
                             value=float(current_late), step=0.5)
    wd = wi.whatif_delivery(target_late, current_late_rate_pct=current_late)
    c1, c2, c3 = st.columns(3)
    c1.metric("Điểm đánh giá TB hiện tại", f"{wd.current_avg_review:.3f}")
    c2.metric("Điểm đánh giá TB dự kiến", f"{wd.projected_avg_review:.3f}")
    c3.metric("Thay đổi", f"{wd.delta_avg_review:+.3f}")
    st.caption(
        "Dựa trên điểm đánh giá trung bình đo được của nhóm giao trễ (2.55) và nhóm đúng hạn (4.21), "
        "mô hình chỉ là phép nội suy trung bình có trọng số đơn giản, không phải mô hình nhân quả đầy đủ."
    )

    st.divider()

    # --- What-if: promotion ---
    st.subheader("What-if: Khuyến mãi theo danh mục")
    cat_summary = _category_revenue_summary()
    categories = cat_summary["category_en"].tolist()
    promo_cat = st.selectbox("Chọn danh mục", categories)
    discount = st.slider("Mức giảm giá (%)", 0, 50, value=10)
    elasticity = st.slider("Độ co giãn cầu theo giá", 0.0, 3.0, value=1.0, step=0.1)
    wp = wi.whatif_promotion(promo_cat, discount, elasticity)
    c1, c2, c3 = st.columns(3)
    c1.metric("Doanh thu hiện tại", f"{wp.base_revenue:,.2f}")
    c2.metric("Doanh thu dự kiến", f"{wp.projected_revenue:,.2f}")
    c3.metric("Thay đổi", f"{wp.delta_revenue:+,.2f} ({wp.delta_revenue_pct:+.2f}%)")
    st.warning(
        "Đây là GIẢ ĐỊNH do người dùng tự nhập (độ co giãn cầu theo giá), KHÔNG phải số đo thực tế "
        "hay dự báo chắc chắn. Kết quả chỉ mang tính minh họa để thử các kịch bản khác nhau."
    )


# --------------------------------------------------------------------------- dispatch
PAGES = {
    "Tổng quan": page_overview,
    "Phân tích đa chiều (OLAP)": page_olap,
    "Địa lý & khách hàng": page_geo_customer,
    "Giao hàng & hài lòng": page_delivery,
    "Dự báo & DSS": page_dss,
}


def main():
    st.set_page_config(page_title="Olist DW & DSS", layout="wide")
    st.sidebar.title("Olist DW & DSS Dashboard")
    choice = st.sidebar.radio("Chọn trang", list(PAGES.keys()))

    try:
        PAGES[choice]()
    except FileNotFoundError as e:
        st.error(str(e))


if __name__ == "__main__":
    main()
