import sys
from pathlib import Path

# Ensure streamlit_app is in sys.path for relative imports
_app_root = Path(__file__).parent.parent
if str(_app_root) not in sys.path:
    sys.path.insert(0, str(_app_root))