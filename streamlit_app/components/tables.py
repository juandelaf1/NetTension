import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def render_aggrid(df, key="grid", height=400, editable=False, selection_mode="single"):
    """Render professional AgGrid table."""
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        filterable=True, sortable=True, resizable=True,
        wrapText=True, autoHeight=True
    )
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    gb.configure_side_bar()
    
    if selection_mode:
        gb.configure_selection(selection_mode=selection_mode, use_checkbox=True)
    
    if editable:
        gb.configure_columns(list(df.columns), editable=True)
    
    grid_options = gb.build()
    
    return AgGrid(
        df,
        gridOptions=grid_options,
        height=height,
        width="100%",
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        key=key,
        theme="streamlit"
    )

def render_governance_table(df):
    """Specialized table for governance data with conditional formatting."""
    from st_aggrid import JsCode
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filterable=True, sortable=True, resizable=True)
    
    # Conditional formatting for confidence
    confidence_style = JsCode("""
    function(params) {
        if (params.value === 'High') return {'color': '#2E7D32', 'fontWeight': '600'};
        if (params.value === 'Medium') return {'color': '#B8860B', 'fontWeight': '600'};
        if (params.value === 'Low') return {'color': '#C62828', 'fontWeight': '600'};
        return {};
    }
    """)
    
    if "confidence" in df.columns:
        gb.configure_column("confidence", cellStyle=confidence_style)
    if "Confidence" in df.columns:
        gb.configure_column("Confidence", cellStyle=confidence_style)
    
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)
    
    return AgGrid(
        df,
        gridOptions=gb.build(),
        height=500,
        width="100%",
        fit_columns_on_grid_load=True,
        theme="streamlit"
    )