from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time

def get_final_url_from_google(google_news_url: str) -> tuple[str | None, str | None]:
    """
    Navigates through Google's consent and redirect pages to find the final article URL.
    This version iteratively tries to click consent buttons and handles Yahoo Finance redirects.

    Args:
        google_news_url: The initial URL from the Google News RSS feed.

    Returns:
        A tuple containing the final destination URL and the page's HTML content,
        or (URL, None) on timeout, or (None, None) on other errors.
    """

    # Added 'guce.yahoo.com' to intermediary domains to handle Yahoo's consent/redirect pages.
    eval_correctness = lambda url: not any([part in url for part in ["google.com", "consent", "guce.yahoo.com"]])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        try:
            page.goto(google_news_url, wait_until='domcontentloaded', timeout=15000)

            # Iteratively try to handle consent and redirects up to 3 times.
            for i in range(4): # Increased attempts for multi-step redirects
                if eval_correctness(page.url):
                    print("Successfully redirected to a non-Google/intermediary URL. Grabbing content.")
                    return page.url, page.content()

                print(f"Attempt {i+1}: Checking for consent/redirect on {page.url[:80]}...")

                try:
                    # Look for a consent button directly on the page or in any iframe
                    button_found = False
                    
                    # Check for buttons in iframes first
                    for frame in page.frames:
                        accept_button = frame.get_by_role('button', name='Accept all').first
                        if accept_button.is_visible():
                            print("Found 'Accept all' button in an iframe. Clicking...")
                            accept_button.click(timeout=5000)
                            button_found = True
                            break
                    
                    if not button_found:
                        # If not in an iframe, check the main page
                        accept_button_main = page.get_by_role('button', name='Accept all').first
                        if accept_button_main.is_visible():
                            print("Found 'Accept all' button on the main page. Clicking...")
                            accept_button_main.click(timeout=5000)
                            button_found = True

                    if button_found:
                        print("Clicked consent button, waiting for page to settle...")
                        page.wait_for_load_state('domcontentloaded', timeout=7000)
                    
                    # After handling consent, check for Yahoo's "click here" redirect.
                    # This can appear on the same page after consent or on a new page.
                    if "guce.yahoo" in page.url:
                        print("On a Yahoo page, checking for a 'here' redirect link.")
                        redirect_link = page.get_by_role('link', name='here').first
                        if redirect_link.is_visible(timeout=1000):
                            print("Found 'here' link, clicking to proceed...")
                            redirect_link.click(timeout=5000)
                            page.wait_for_load_state('domcontentloaded', timeout=7000)
                            print("Clicked 'here' link. Re-evaluating page.")

                    if not button_found:
                        print("No consent button found on this iteration.")
                        time.sleep(2) # Wait a moment to see if a redirect happens anyway

                except PlaywrightTimeoutError as e:
                    print(f"A timeout occurred: {e}. The page might be slow or already redirecting.")
                    time.sleep(2)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    time.sleep(2)

            # After trying to click buttons, wait for the final redirection.
            print("Waiting for final redirection...")
            page.wait_for_url(
                eval_correctness,
                timeout=15000
            )
            
            final_url = page.url
            content = page.content()
            
        except PlaywrightTimeoutError:
            print(f"Final timeout occurred. The page did not redirect from: {page.url}")
            if eval_correctness(page.url):
                return page.url, page.content()
            return page.url, None # Return the current URL for debugging
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None, None
        finally:
            browser.close()
            
        return final_url, content

if __name__ == "__main__":
    # Test link that often redirects to Yahoo Finance
    test_link = "https://news.google.com/articles/CBMihAFBVV95cUxNeE5wck5ydGNxelZGSTMzVl9SMG0wQm1UTVZpTVRPeGxUMHlUcE11d3JfVFFCOUFwaXdtcjR2eTg4ejFrb1hKZVJzaVdkU3R4MEdLOHZGX19oWk1tUnMyWHN5eF8yZmwxa09zdENXOVc3MVR6QkxNakNYNG9MT0N3anJUWjI?oc=5&hl=en-US&gl=US&ceid=US:en"

    print(f"Resolving Google News URL: {test_link}")
    resolved_url, content = get_final_url_from_google(test_link)

    if resolved_url and content and not any(part in resolved_url for part in ["google.com", "guce.yahoo.com"]):
        print("\n" + "="*30)
        print(f"✅ Final Article URL Found:")
        print(resolved_url)
        print(f"Content length: {len(content)}")
        print("="*30)
    else:
        print("\n" + "="*30)
        print(f"❌ Could not resolve the final URL. Last known URL:")
        print(resolved_url)
        print("="*30)
