import os
import httpx
import datetime
import json
from playwright.async_api import async_playwright
from utils.pdf_extractor import extract_text_from_pdf

async def scrape(config: dict, model_number: str, manufactuerer: str):
    os.makedirs("output", exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(config["url"])
        await page.wait_for_selector(config["search_input_selector"])

        await page.fill(config["search_input_selector"], model_number)
        await page.press(config["search_input_selector"], "Enter")

        await page.wait_for_selector(config["pdf_link_selector"])

        pdf_links = await page.query_selector_all(config["pdf_link_selector"])

        for link in pdf_links:
            pdf_url = await link.get_attribute("href")
            doc_type = await link.evaluate("el => el.closest('.product-document').getAttribute('data-name')")

            try:
                response = httpx.get(pdf_url)
                
                filename = pdf_url.split("/")[-1]
                filepath = os.path.join("output", filename)

                with open(filepath, "wb") as f:
                    f.write(response.content)

                extracted = extract_text_from_pdf(filepath)

                result = {
                    "manufacturer": manufactuerer,
                    "model_number": model_number,
                    "doc_type": doc_type,
                    "source_url": pdf_url,
                    "pages": extracted["pages"],
                    "text": extracted["text"],
                    "extraction_method": extracted["extraction_method"],
                    "success": extracted["success"],
                    "scraped_at": datetime.datetime.now().isoformat()
                }

                json_filename = f"carrier_{model_number}_{doc_type}.json"
                json_filepath = os.path.join("output", json_filename)

                with open(json_filepath, "w") as f:
                    json.dump(result, f, indent=4 )                    

            except httpx.HTTPStatusError as e:
                print("Error", e.response.status_code)

            except httpx.RequestError as e:
                print("Error", e)

