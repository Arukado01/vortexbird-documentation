"""Compatibility entry point for the current professional PDF builder."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("build_professional_pdf.py")), run_name="__main__")
