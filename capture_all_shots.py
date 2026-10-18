import asyncio
from playwright.async_api import async_playwright
import httpx

async def main():
    r = httpx.get("http://127.0.0.1:8000/v1/runs").json()
    run_id = r[0]["id"]
    print(f"Using run_id: {run_id}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # 1. 01_home.png: Worklist homepage
        print("Navigating to Worklist homepage...")
        await page.goto("http://127.0.0.1:8501", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        await page.screenshot(path="shots/01_home.png", full_page=True)
        print("Captured shots/01_home.png")

        # Navigate to recording view
        print(f"Navigating to recording view for run {run_id}...")
        await page.goto(f"http://127.0.0.1:8501/run?run={run_id}", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)

        # 2. 08_agent_trace.png: Agent conversation trace
        print("Capturing agent trace...")
        trace_expander = page.get_by_text("The agents' conversation").first
        try:
            if await trace_expander.is_visible():
                await trace_expander.click()
                await asyncio.sleep(2)
        except Exception as e:
            print("Expander click note:", e)
        await page.screenshot(path="shots/08_agent_trace.png", full_page=True)
        print("Captured shots/08_agent_trace.png")

        # 3. 02_study_search.png: ECG Signal & Beat annotation view
        print("Capturing ECG tab...")
        tab_ecg = page.get_by_role("tab", name="ECG")
        if await tab_ecg.is_visible():
            await tab_ecg.click()
            await asyncio.sleep(2)
        await page.screenshot(path="shots/02_study_search.png", full_page=True)
        print("Captured shots/02_study_search.png")

        # 4. 07_analytics.png: Findings tab & justifications
        print("Capturing Findings tab...")
        tab_find = page.get_by_role("tab", name="Findings")
        if await tab_find.is_visible():
            await tab_find.click()
            await asyncio.sleep(2)
        await page.screenshot(path="shots/07_analytics.png", full_page=True)
        print("Captured shots/07_analytics.png")

        # 5. 05_trial_comparison.png: Adapter vs Text comparison tab
        print("Capturing Adapter vs text comparison tab...")
        tab_cmp = page.get_by_role("tab", name="Adapter vs text")
        if await tab_cmp.is_visible():
            await tab_cmp.click()
            await asyncio.sleep(2)
        await page.screenshot(path="shots/05_trial_comparison.png", full_page=True)
        print("Captured shots/05_trial_comparison.png")

        # 6. 03_drug_interactions.png: Ask tab with questions & guardrail refusals
        print("Capturing Ask tab with clinical questions & guardrail refusals...")
        tab_ask = page.get_by_role("tab", name="Ask")
        if await tab_ask.is_visible():
            await tab_ask.click()
            await asyncio.sleep(2)
        await page.screenshot(path="shots/03_drug_interactions.png", full_page=True)
        print("Captured shots/03_drug_interactions.png")

        # 7. 06_graph_view.png: Audit Trail (replacing removed How it works)
        print("Capturing Audit trail tab...")
        tab_audit = page.get_by_role("tab", name="Audit trail")
        if await tab_audit.is_visible():
            await tab_audit.click()
            await asyncio.sleep(2)
        await page.screenshot(path="shots/06_graph_view.png", full_page=True)
        print("Captured shots/06_graph_view.png (Audit Trail View)")

        # 8. 04_adverse_events.png: Stress Scenarios & Adverse Events on worklist
        print("Capturing Stress scenario / adverse events on worklist...")
        await page.goto("http://127.0.0.1:8501/", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        an_expander = page.get_by_text("Analyse a recording").first
        try:
            if await an_expander.is_visible():
                await an_expander.click()
                await asyncio.sleep(1)
        except Exception as e:
            print("Analyse expander click note:", e)
        await page.screenshot(path="shots/04_adverse_events.png", full_page=True)
        print("Captured shots/04_adverse_events.png")

        await browser.close()
        print("All refreshed screenshots successfully captured!")

if __name__ == "__main__":
    asyncio.run(main())
