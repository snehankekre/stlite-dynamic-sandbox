from __future__ import annotations

from typing import Sequence

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from streamlit_monaco import st_monaco

# Tell streamlit that there is a component called stlite_sandbox,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component("stlite_sandbox", path=str(frontend_dir))


# Create the python function that will be called
def stlite_sandbox(
    code: str,
    requirements: list[str] | None = None,
    key: str = "stlite_sandbox",
    height: int = 500,
    scrollable: bool = False,
    editor: bool = False,
    border: bool = True,
    requirements_picker: bool = False,
    layout: int | Sequence[int] | None = None,
) -> tuple[str, list[str]]:
    """
    Add a descriptive docstring
    """
    if requirements is None:
        requirements = []

    if layout is None:
        layout = [1, 1]

    if editor:
        col1, col2 = st.columns(layout)

        with col1:
            tab_vals = ["streamlit_app.py"]
            if requirements_picker:
                tab_vals.append("requirements.txt")
            with st.container(border=border):
                tabs = st.tabs(tab_vals)
                with tabs[0]:
                    code = st_monaco(
                        value=code, language="python", height=f"{height - 63}px"
                    )
                if requirements_picker:
                    with tabs[1]:
                        reqs_text = st_monaco(
                            value="\n".join(requirements),
                            language="text",
                            height=f"{height - 63}px",
                        )

                        if reqs_text:
                            requirements = [
                                x.strip() for x in reqs_text.splitlines() if x.strip()
                            ]

        with col2:
            with st.container(border=border):
                _stlite_sandbox(
                    code=code,
                    requirements=requirements,
                    key=key,
                    height=height + 15,
                    scrollable=scrollable,
                )
    else:
        with st.container(border=border):
            _stlite_sandbox(
                code=code,
                requirements=requirements,
                key=key,
                height=height + 15,
                scrollable=scrollable,
            )

    return code, requirements


def _stlite_sandbox(
    code: str,
    requirements: list[str] | None = None,
    key: str = "stlite_sandbox",
    height: int = 500,
    scrollable: bool = False,
):
    if requirements is None:
        requirements = []

    _component_func(
        key=key,
        code=code,
        requirements=requirements,
        height=height,
        scrollable=scrollable,
    )


def main():
    st.write("## Example")
    default_code = """
import streamlit as st

st.write("Hello world!")"""
    code = st.text_area("Code", value=default_code, height=200, key="code")
    stlite_sandbox(code=code, key="blah", height=500)


if __name__ == "__main__":
    main()
