MANUFACTURERS = {
    "carrier": {
        "url": "https://www.carrier.com/residential/en/us/homeowner-resources/product-literature/",
        "search_type": "both",
        "needs_playwright": True,
        "search_input_selector": "#name",
        "model_select_selector": "#modelSelect",
        "type_select_selector": "#typeSelect",
        "results_filter_selector": None,
        "pdf_link_selector": ".product-document a",
        "pdf_identifier": "data-name"
    }
}