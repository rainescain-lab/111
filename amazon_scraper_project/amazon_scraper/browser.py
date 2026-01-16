# test commit
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from playwright.sync_api import Error as PlaywrightError, Page, sync_playwright


@dataclass(frozen=True)
class BrowserSession:
    user_data_dir: str
    headless: bool
    slow_mo_ms: int
    nav_timeout_ms: int
    action_timeout_ms: int

    def run(self, handler: Callable[[Page], None]) -> None:
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=self.headless,
                slow_mo=self.slow_mo_ms,
            )
            context.set_default_timeout(self.action_timeout_ms)
            page = context.pages[0] if context.pages else context.new_page()
            try:
                handler(page)
            finally:
                try:
                    context.close()
                except PlaywrightError:
                    pass


def detect_captcha(page: Page) -> bool:
    try:
        content = page.content()
    except PlaywrightError:
        return False
    lower = content.lower()
    return any(
        token in lower
        for token in (
            "captcha",
            "robot check",
            "unusual traffic",
            "enter the characters you see below",
            "validatecaptcha",
        )
    )


def wait_for_manual_resolution() -> None:
    print(
        "[WARN] Captcha detected. Please solve in the browser, then press Enter.",
        flush=True,
    )
    try:
        input()
    except EOFError:
        time.sleep(3)
