"""Traceability: CO4031 assignment section 5.1 (what must be in the ZIP) and section 1.1 (what must
be built). Each test names the requirement it covers."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import RAW, REPO

NEEDED_CSV = ["olist_customers_dataset", "olist_orders_dataset", "olist_order_items_dataset",
              "olist_order_payments_dataset", "olist_order_reviews_dataset", "olist_products_dataset",
              "olist_sellers_dataset", "product_category_name_translation"]


# 1.1(2) star schema + ETL
def test_req_star_schema_ddl_present():
    sql = (REPO / "src/sql/01_schema.sql").read_text(encoding="utf-8")
    assert sql.count("CREATE TABLE") == 7 and "fact_sales" in sql


def test_req_etl_script_present():
    assert (REPO / "src/etl/run_etl.py").exists()


# 1.1(3) backend OLAP + frontend dashboard
def test_req_olap_script_and_sql_present():
    assert (REPO / "src/olap/olap_demo.py").exists() and (REPO / "src/sql/02_olap_queries.sql").exists()


def test_req_dashboard_present_with_5_pages():
    app = (REPO / "src/app/app.py").read_text(encoding="utf-8")
    assert len(re.findall(r'^\s+"[^"]+":\s*page_\w+,', app, flags=re.M)) == 5


# 1.1(4) DSS
@pytest.mark.parametrize("f", ["forecast", "rfm", "whatif"])
def test_req_dss_modules_present(f):
    assert (REPO / f"src/dss/{f}.py").exists()


# 5.1(1) report PDF
@pytest.mark.parametrize("f", ["part_A_dw", "part_B_dss"])
def test_req_report_sources_and_pdfs_present(f):
    assert (REPO / f"report/{f}.tex").exists()
    pdf = REPO / f"report/{f}.pdf"
    assert pdf.exists() and pdf.read_bytes()[:4] == b"%PDF"


def test_report_B_has_no_empty_screenshot_placeholders():
    """REVIEW_VY item 1."""
    tex = (REPO / "report/part_B_dss.tex").read_text(encoding="utf-8")
    assert "TODO" not in tex, "report B still has TODO placeholders (screenshots)"


def test_report_A_cover_has_real_student_name_and_id():
    """Cover must carry the student's id (MSSV, 7 digits at HCMUT)."""
    tex = (REPO / "report/part_A_dw.tex").read_text(encoding="utf-8")
    assert not re.search(r"\[(Họ tên|MSSV|Tên)[^\]]*\]|TODO", tex), "cover still has placeholders"
    assert re.search(r"\b\d{7}\b", tex), "no 7-digit MSSV on the report A cover"


# 5.1(2) source in src/
def test_req_src_has_sql_python_and_frontend():
    assert list((REPO / "src").rglob("*.sql")) and list((REPO / "src").rglob("*.py"))


# 5.1(3) sample data in data/
def test_req_sample_data_folder_and_readme_link():
    assert (REPO / "data").is_dir()
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert re.search(r"drive\.google|github\.com|kaggle", readme, re.I), "README has no data link"


def test_readme_documents_how_to_run():
    r = (REPO / "README.md").read_text(encoding="utf-8")
    for cmd in ["run_etl.py", "streamlit run"]:
        assert cmd in r


def test_requirements_pin_a_streamlit_that_supports_width_stretch():
    """REVIEW_VY item 5: app.py uses width='stretch' (Streamlit >= 1.67 in our tests)."""
    req = (REPO / "requirements.txt").read_text()
    m = re.search(r"streamlit\s*>=\s*(\d+)\.(\d+)", req)
    assert m and (int(m[1]), int(m[2])) >= (1, 67), req


# 5.1(4) slides as PDF (spec for A exists, PDFs are produced by the owner)
def test_slide_materials_exist():
    assert (REPO / "slides/part_A_slide_spec.md").exists()
    assert (REPO / "slides/part_B_outline.md").exists()


def test_slides_pdf_exported_for_submission():
    pdfs = list((REPO / "slides").glob("*.pdf"))
    assert pdfs, "no slide PDF in slides/ yet (assignment 5.1 requires the slide deck as PDF)"


# LO / quality
def test_data_contract_document_exists_and_names_the_db():
    assert "olist_dw.db" in (REPO / "docs/data_contract.md").read_text(encoding="utf-8")


def test_no_large_files_or_secrets_tracked():
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True).stdout.split()
    big = [f for f in out if (REPO / f).exists() and (REPO / f).stat().st_size > 20_000_000]
    assert not big, big
    assert not [f for f in out if f.endswith((".env", ".pem", ".key"))]


# reproducibility: full ETL on the real CSVs into a temp DB gives the same numbers
@pytest.mark.skipif(not all((RAW / f"{n}.csv").exists() for n in NEEDED_CSV), reason="raw CSVs missing")
def test_full_etl_from_scratch_is_reproducible(tmp_path):
    db = tmp_path / "fresh.db"
    p = subprocess.run([sys.executable, str(REPO / "src/etl/run_etl.py"), "--db", str(db)],
                       capture_output=True, text=True, timeout=300)
    assert p.returncode == 0, p.stderr[-800:]
    assert "FAIL" not in p.stdout
    import sqlite3
    con = sqlite3.connect(db)
    assert con.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0] == 112650
    assert con.execute("SELECT COUNT(*) FROM dim_customer").fetchone()[0] == 96096
    con.close()


@pytest.mark.skipif(not all((RAW / f"{n}.csv").exists() for n in NEEDED_CSV), reason="raw CSVs missing")
def test_olap_demo_cli_runs(tmp_path):
    p = subprocess.run([sys.executable, str(REPO / "src/olap/olap_demo.py")],
                       capture_output=True, text=True, timeout=120)
    assert p.returncode == 0, p.stderr[-800:]
    assert "rollup_year" in p.stdout


# ------------------------------------------------- follow-ups from docs/REVIEW_VY.md
def test_review_item3_slide_outline_explains_k_choice():
    t = (REPO / "slides/part_B_outline.md").read_text(encoding="utf-8")
    assert "0.681" in t or "0,681" in t, "slide 6 still says K chosen by silhouette without the K=2 caveat"


def test_review_item7_report_B_no_tet_in_brazilian_data():
    assert "sau Tết" not in (REPO / "report/part_B_dss.tex").read_text(encoding="utf-8")


def test_review_item7_report_B_no_hardcoded_table_reference():
    assert "Bảng~giao trễ" not in (REPO / "report/part_B_dss.tex").read_text(encoding="utf-8")


def test_review_item8_presentation_time_fits_the_limit():
    """Sum of the per-slide timings in B's outline headings must be <= 480 s (8 min)."""
    t = (REPO / "slides/part_B_outline.md").read_text(encoding="utf-8")
    secs = [int(x) for x in re.findall(r"(?m)^#{2,3} Slide[^\n]*\((\d+)s\)", t)]
    assert len(secs) >= 8, secs
    assert sum(secs) <= 480, f"B outline slides add up to {sum(secs)} s (> 8 min)"
