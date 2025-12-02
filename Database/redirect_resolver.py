from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time

def get_final_url_from_google(google_news_url: str) -> str | None:
    """
    Navigates through Google's consent and redirect pages to find the final article URL.
    This version iteratively tries to click consent buttons.

    Args:
        google_news_url: The initial URL from the Google News RSS feed.

    Returns:
        The final destination URL, or None if it cannot be found.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        try:
            page.goto(google_news_url, wait_until='domcontentloaded', timeout=15000)

            # Iteratively try to find and click a consent button up to 3 times.
            for i in range(3):
                # If we've successfully redirected, break the loop.
                if "google.com" not in page.url:
                    print("Successfully redirected to a non-Google URL.")
                    break

                print(f"Attempt {i+1}: Checking for consent buttons on {page.url[:80]}...")

                try:
                    # Look for a consent button directly on the page or in any iframe
                    # This is a more robust way to handle different consent UI versions
                    button_found = False
                    
                    # Check for buttons in iframes first, as that's the most common pattern
                    for frame in page.frames:
                        # Common consent texts. Playwright performs a case-insensitive search.
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
                         # Wait for potential navigation or content loading
                        page.wait_for_load_state('networkidle', timeout=7000)
                    else:
                        print("No consent button found on this page. Assuming consent is handled.")
                        # If no button is found, we might be on the final redirect step
                        break 
                
                except PlaywrightTimeoutError:
                    print("Timed out while trying to click a button or wait for navigation.")
                    # Continue to the next check, maybe the page will redirect anyway
                    time.sleep(2)
                except Exception as e:
                    print(f"An error occurred while trying to click consent button: {e}")
                    time.sleep(2)


            # After trying to click buttons, wait for the final redirection.
            print("Waiting for final redirection...")
            page.wait_for_url(
                lambda url: "google.com" not in url,
                timeout=15000
            )
            
            final_url = page.url
            
        except PlaywrightTimeoutError:
            print(f"Final timeout occurred. The page did not redirect from: {page.url}")
            return page.url # Return the current URL for debugging
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        finally:
            browser.close()
            
        return final_url

if __name__ == "__main__":
    test_link = "https://news.google.com/articles/CBMihAFBVV95cUxNeE5wck5ydGNxelZGSTMzVl9SMG0wQm1UTVZpTVRPeGxUMHlUcE11d3JfVFFCOUFwaXdtcjR2eTg4ejFrb1hKZVJzaVdkU3R4MEdLOHZGX19oWk1tUnMyWHN5eF8yZmwxa09zdENXOVc3MVR6QkxNakNYNG9MT0N3anJUWjI?oc=5&hl=en-US&gl=US&ceid=US:en"

    print(f"Resolving Google News URL: {test_link}")
    resolved_url = get_final_url_from_google(test_link)

    if resolved_url and "google.com" not in resolved_url:
        print("\n" + "="*30)
        print(f"✅ Final Article URL Found:")
        print(resolved_url)
        print("="*30)
    else:
        print("\n" + "="*30)
        print(f"❌ Could not resolve the final URL. Last known URL:")
        print(resolved_url)
        print("="*30)
