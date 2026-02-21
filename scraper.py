import os
import httpx
import datetime
import json
from playwright.async_api import async_playwright
from utils.pdf_extractor import extract_text_from_pdf
from utils.brave import search_pdf_manuals
from dotenv import load_dotenv


async def scrape(config: dict, model_number: str, manufacturer: str,):
    load_dotenv()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(config["url"])
        await page.wait_for_selector(config["search_input_selector"])

        await page.fill(config["search_input_selector"], model_number)
        await page.press(config["search_input_selector"], "Enter")

        try:
            await page.wait_for_selector(config["pdf_link_selector"], timeout=10000)
        except:
            pass

        pdf_links = await page.query_selector_all(config["pdf_link_selector"])

        pdf_saved = 0

        for link in pdf_links:
            pdf_url = await link.get_attribute("href")
            doc_type = await link.evaluate("el => el.closest('.product-document').getAttribute('data-name')")

            try:
                response = httpx.get(pdf_url)
                
                filename = pdf_url.split("/")[-1]
                
                pdf_dir = os.path.join("output", manufacturer, "pdf")
                json_dir = os.path.join("output", manufacturer, "json")
                os.makedirs(pdf_dir, exist_ok = True)
                os.makedirs(json_dir, exist_ok = True)

                json_filename = f"{manufacturer}_{model_number}_{doc_type}_{filename}.json"
                filepath = os.path.join(pdf_dir, filename)
                json_filepath = os.path.join(json_dir, json_filename)


                with open(filepath, "wb") as f:
                    f.write(response.content)

                extracted = extract_text_from_pdf(filepath)

                result = {
                    "manufacturer": manufacturer,
                    "model_number": model_number,
                    "doc_type": doc_type,
                    "source_url": pdf_url,
                    "pages": extracted["pages"],
                    "text": extracted["text"],
                    "extraction_method": extracted["extraction_method"],
                    "success": extracted["success"],
                    "scraped_at": datetime.datetime.now().isoformat()
                }


                with open(json_filepath, "w") as f:
                    json.dump(result, f, indent=4 )  

                pdf_saved += 1
                     
            except httpx.HTTPStatusError as e:
                print("Error", e.response.status_code)

            except httpx.RequestError as e:
                print("Error", e)

        if pdf_saved == 0:
            query = f"{model_number} {manufacturer} service manual filetype:pdf"
            candidates = await search_pdf_manuals(query)
            print(f"Brave found {len(candidates)} candidates")

            for candidate in candidates:
                try:
                    response = httpx.get(candidate.url, timeout = 30)
                    filename = candidate.url.split("/")[-1]
                    
                    pdf_dir = os.path.join("output", manufacturer, "pdf")
                    json_dir = os.path.join("output", manufacturer, "json")
                    os.makedirs(pdf_dir, exist_ok=True)
                    os.makedirs(json_dir, exist_ok=True)
                    
                    filepath = os.path.join(pdf_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                        
                    extracted = extract_text_from_pdf(filepath)
                    
                    result = {
                        "manufacturer": manufacturer,
                        "model_number": model_number,
                        "doc_type": candidate.title or "unknown",
                        "source_url": candidate.url,
                        "pages": extracted["pages"],
                        "text": extracted["text"],
                        "extraction_method": extracted["extraction_method"],
                        "success": extracted["success"],
                        "scraped_at": datetime.datetime.now().isoformat()
                    }
                    
                    json_filename = f"{manufacturer}_{model_number}_brave_{filename}.json"
                    json_filepath = os.path.join(json_dir, json_filename)
                    
                    with open(json_filepath, "w") as f:
                        json.dump(result, f, indent=4)
                        
                except Exception as e:
                    print(f"Brave download error: {e}")

