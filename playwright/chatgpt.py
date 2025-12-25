from playwright.sync_api import sync_playwright
from pathlib import Path
import time

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

USER_DATA_DIR = Path(r"D:\SourceCode\python\playwright\profiles\chrome_chatgpt")

USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

def wait_for_generation_done(page, stable_time=1.2, timeout=180):
    start = time.time()
    last_text = None
    stable_since = None

    while True:
        # Detect generating via Send button disabled
        send_btn = page.locator('button[data-testid="send-button"]')
        generating = send_btn.count() > 0 and send_btn.first.is_disabled()

        # Lấy markdown content của assistant cuối
        markdown_blocks = page.locator(
            'div[data-message-author-role="assistant"] .markdown'
        )

        if markdown_blocks.count() == 0:
            time.sleep(0.3)
            continue

        current_text = markdown_blocks.nth(
            markdown_blocks.count() - 1
        ).inner_text().strip()

        if current_text == last_text and not generating:
            if stable_since is None:
                stable_since = time.time()
            elif time.time() - stable_since >= stable_time:
                return current_text
        else:
            stable_since = None
            last_text = current_text

        if time.time() - start > timeout:
            raise TimeoutError("Generation timeout")

        time.sleep(0.4)


with sync_playwright() as p:
    """
    Chức năng playwright tự động vào web
    """
    context = p.chromium.launch_persistent_context(
        executable_path=CHROME_PATH,
        user_data_dir=str(USER_DATA_DIR),
        headless=False,
        slow_mo=80,
        args=["--disable-blink-features=AutomationControlled"]
    )

    page = context.new_page()

    page.goto("https://chatgpt.com/")

    prompt = "nói gì đó ngắn gọn"

    input_box = page.locator("#prompt-textarea")

    # Chờ input xuất hiện
    input_box.wait_for(timeout=60000)

    # Focus
    input_box.click()

    page.keyboard.press("Control+A")

    page.keyboard.press("Backspace")

    page.keyboard.type(prompt, delay=20)

    # Gửi (Enter, KHÔNG Shift)
    page.keyboard.press("Enter")

    response_text = wait_for_generation_done(page)

    print("Response: " + response_text)

    Path("chatgpt_response.txt").write_text(response_text, encoding="utf-8")

    page.pause()

