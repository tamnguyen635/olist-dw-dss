"""Headless run of the Streamlit dashboard (streamlit.testing.v1.AppTest): every page must render
without an exception and show the key widgets."""
from __future__ import annotations

import pytest

from conftest import REPO, needs_dw

pytestmark = needs_dw
AppTest = pytest.importorskip("streamlit.testing.v1").AppTest

APP = str(REPO / "src" / "app" / "app.py")
PAGES = ["Tổng quan", "Phân tích đa chiều (OLAP)", "Địa lý & khách hàng",
         "Giao hàng & hài lòng", "Dự báo & DSS"]


def run_page(name):
    at = AppTest.from_file(APP, default_timeout=120)
    at.run()
    assert not at.exception, at.exception
    at.sidebar.radio[0].set_value(name).run()
    return at


def test_sidebar_lists_five_pages():
    at = AppTest.from_file(APP, default_timeout=120).run()
    assert list(at.sidebar.radio[0].options) == PAGES


@pytest.mark.parametrize("page", PAGES)
def test_page_renders_without_exception(page):
    at = run_page(page)
    assert not at.exception, [e.value for e in at.exception]
    assert not at.error, [e.value for e in at.error]


def test_overview_shows_kpi_metrics():
    at = run_page("Tổng quan")
    assert len(at.metric) >= 3


def test_olap_page_has_interactive_controls():
    at = run_page("Phân tích đa chiều (OLAP)")
    assert len(at.selectbox) >= 2          # drill-down year + slice year
    assert len(at.multiselect) >= 2        # dice: states + categories


def test_olap_dice_default_selection_is_not_nearly_empty():
    """Regression for REVIEW_VY item 4: default dice must pick big states/categories."""
    at = run_page("Phân tích đa chiều (OLAP)")
    states = at.multiselect[0].value
    assert {"SP"} & set(states), f"default states {states} do not include SP"


def test_olap_selects_all_years_without_error():
    at = run_page("Phân tích đa chiều (OLAP)")
    for opt in at.selectbox[0].options:
        at.selectbox[0].select(opt).run()
        assert not at.exception


def test_dss_page_has_forecast_and_whatif_controls():
    at = run_page("Dự báo & DSS")
    assert len(at.slider) >= 1 or len(at.number_input) >= 1
