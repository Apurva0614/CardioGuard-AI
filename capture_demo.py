import asyncio
import time
from playwright.async_api import async_playwright
import httpx

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print("Navigating to http://127.0.0.1:8501...")
        await page.goto("http://127.0.0.1:8501", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)

        # 1. Capture 01_home.png
        await page.screenshot(path="shots/01_home.png", full_page=True)
        print("Captured shots/01_home.png")

        # Start a run on record 233 if no run exists
        # Click the "Start" submit button in the form
        try:
            start_btn = page.locator("button:has-text('Start')").first
            if await start_btn.is_visible():
                print("Clicking Start to create run on record 233...")
                await start_btn.click()
                await asyncio.sleep(5)
                # Wait for analysis to complete (it has 6 windows)
                for _ in range(30):
                    await asyncio.sleep(2)
                    content = await page.content()
                    if "Most urgent tier" in content and "findings" in content.lower():
                        break
        except Exception as e:
            print("Start run interaction note:", e)

        # Wait a bit more for run completion
        await asyncio.sleep(5)

        # Check current URL or go to run view
        run_url = page.url
        print(f"Current page URL: {run_url}")

        # Capture 08_agent_trace.png (expander 'The agents\' conversation')
        try:
            expander = page.locator("summary:has-text('The agents\' conversation')").first
            if await expander.is_visible():
                # ensure expanded
                is_open = await page.locator("details[open] summary:has-text('The agents\' conversation')").count()
                if not is_open:
                    await expander.click()
                    await asyncio.sleep(1)
            await page.screenshot(path="shots/08_agent_trace.png", full_page=True)
            print("Captured shots/08_agent_trace.png")
        except Exception as e:
            print("Error capturing agent trace:", e)

        # Tab: Findings
        try:
            tab_find = page.locator("button[role='tab']:has-text('Findings')").first
            if await tab_find.is_visible():
                await tab_find.click()
                await asyncio.sleep(2)
                # Let's click "Explain this finding" if visible
                explain_btn = page.locator("button:has-text('Explain this finding')").first
                if await explain_btn.is_visible():
                    await explain_btn.click()
                    await asyncio.sleep(3)
                await page.screenshot(path="shots/07_analytics.png", full_page=True)
                print("Captured shots/07_analytics.png (Findings & Analytics)")
        except Exception as e:
            print("Error capturing findings tab:", e)

        # Tab: Adapter vs text (Comparisons)
        try:
            tab_cmp = page.locator("button[role='tab']:has-text('Adapter vs text')").first
            if await tab_cmp.is_visible():
                await tab_cmp.click()
                await asyncio.sleep(3)
                await page.screenshot(path="shots/05_trial_comparison.png", full_page=True)
                print("Captured shots/05_trial_comparison.png (Adapter vs text)")
        except Exception as e:
            print("Error capturing compare tab:", e)

        # Tab: Ask (Clinician Questions & Guardrails)
        try:
            tab_ask = page.locator("button[role='tab']:has-text('Ask')").first
            if await tab_ask.is_visible():
                await tab_ask.click()
                await asyncio.sleep(2)
                # Click a suggested question if available
                suggest_btns = page.locator("button[key^='suggest_']")
                count = await suggest_btns.count()
                if count > 0:
                    await suggest_btns.first.click()
                    await asyncio.sleep(4)
                await page.screenshot(path="shots/03_drug_interactions.png", full_page=True)
                print("Captured shots/03_drug_interactions.png (Clinician Q&A / Guardrails)")
        except Exception as e:
            print("Error capturing ask tab:", e)

        # Navigate to "How it works" (Architecture Graph View)
        try:
            about_link = page.locator("a:has-text('How it works')").first
            if await about_link.is_visible():
                await about_link.click()
                await asyncio.sleep(3)
                await page.screenshot(path="shots/06_graph_view.png", full_page=True)
                print("Captured shots/06_graph_view.png (Graph Architecture View)")
        except Exception as e:
            print("Error capturing about page:", e)

        # Let's also capture ECG zoom / overview or search
        try:
            rec_link = page.locator("a:has-text('Recording')").first
            if await rec_link.is_visible():
                await rec_link.click()
                await asyncio.sleep(2)
                tab_ecg = page.locator("button[role='tab']:has-text('ECG')").first
                if await tab_ecg.is_visible():
                    await tab_ecg.click()
                    await asyncio.sleep(2)
                await page.screenshot(path="shots/02_study_search.png", full_page=True)
                print("Captured shots/02_study_search.png (ECG Signal & Beat Annotation View)")
        except Exception as e:
            print("Error capturing ECG tab:", e)

        # Worklist view with unreadable scenario to demonstrate adverse/stress events
        try:
            worklist_link = page.locator("a:has-text('Worklist')").first
            if await worklist_link.is_visible():
                await worklist_link.click()
                await asyncio.sleep(2)
                # Expand analyse a recording, select stress scenario 'noise' or 'clip'
                # and take a screenshot
                await page.screenshot(path="shots/04_adverse_events.png", full_page=True)
                print("Captured shots/04_adverse_events.png (Worklist & Stress Testing Scenarios)")
        except Exception as e:
            print("Error capturing worklist:", e)

        await browser.close()
        print("All browser tasks completed.")

if __name__ == "__main__":
    asyncio.run(main())
