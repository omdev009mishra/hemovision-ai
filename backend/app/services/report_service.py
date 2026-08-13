"""
HemoVision Backend Service — Research Summary Report Generator
"""

from typing import Dict, Any
from ml.src.inference.pipeline import InferenceResult


class ReportService:
    """Generates schema-aligned research summary reports."""

    @staticmethod
    def generate_markdown_report(session_id: str, result: InferenceResult) -> str:
        """Generate formatted Markdown research summary report."""
        report = []
        report.append("# HemoVision — Research Screening Summary Report")
        report.append(f"**Session ID:** `{session_id}`")
        report.append("")
        report.append("> [!CAUTION]")
        report.append("> **INVESTIGATIONAL RESEARCH NOTICE**")
        report.append("> HemoVision is strictly an ongoing research project and baseline prototype.")
        report.append("> This report is NOT a medical diagnosis, clinical laboratory report, or treatment advice.")
        report.append("")
        report.append("---")
        report.append("## 1. Image Quality Assessment")
        report.append(f"* **Usability Status:** {'USABLE' if result.is_usable else 'REJECTED'}")
        report.append(f"* **Composite Quality Score:** {result.quality_score:.2f} / 1.00")
        if result.rejection_reasons:
            report.append(f"* **Rejection Reasons:** {', '.join(result.rejection_reasons)}")
        report.append(f"* **Laplacian Focus Score:** {result.quality_details.get('focus_score', 0.0):.1f}")
        report.append(f"* **Mean Intensity:** {result.quality_details.get('mean_intensity', 0.0):.1f}")
        report.append(f"* **Overexposure Ratio:** {result.quality_details.get('overexposure_ratio', 0.0)*100:.1f}%")
        report.append(f"* **Underexposure Ratio:** {result.quality_details.get('underexposure_ratio', 0.0)*100:.1f}%")
        report.append("")

        if result.is_usable and result.estimated_hb_g_dl is not None:
            report.append("---")
            report.append("## 2. Research Model Prediction")
            report.append(f"* **Estimated Hb:** **{result.estimated_hb_g_dl:.1f} g/dL**")
            if result.prediction_interval:
                report.append(f"* **Conformal 95% Interval:** [{result.prediction_interval[0]:.1f} – {result.prediction_interval[1]:.1f}] g/dL")
            report.append(f"* **Reliability Score:** {result.reliability_score:.2f} / 1.00")
            report.append(f"* **Research Category:** {result.research_category}")
            report.append("")
            report.append("---")
            report.append("## 3. Extracted Chromatic Features")
            for k, v in result.feature_summary.items():
                report.append(f"* **{k}:** {v}")
            report.append("")

        report.append("---")
        report.append("## 4. Mandatory Disclaimer")
        report.append(f"_{result.disclaimer}_")
        return "\n".join(report)
