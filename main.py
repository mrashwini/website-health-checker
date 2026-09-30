from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from html import escape
from datetime import datetime
import time


# =====================================
# GET WEBSITE URL
# =====================================

url = input("Enter website URL: ").strip()


with sync_playwright() as p:

    # =====================================
    # START BROWSER
    # =====================================

    browser = p.chromium.launch(
        headless=True,
        channel="chrome"
    )

    page = browser.new_page()

    # =====================================
    # HTTP ERROR MONITORING
    # =====================================

    http_errors = []

    def check_response(response):
        if response.status >= 400:
            http_errors.append(
                (response.status, response.url)
            )

    page.on("response", check_response)

    # =====================================
    # OPEN WEBSITE
    # =====================================

    start_time = time.time()

    response = page.goto(
        url,
        wait_until="load",
        timeout=30000
    )

    load_time = time.time() - start_time

    print("\n==============================")
    print("   WEBSITE HEALTH CHECKER")
    print("==============================")

    print("\nURL:", url)

    if response:
        print("HTTP Status:", response.status)
    else:
        print("HTTP Status: No response")

    print(f"Page Load Time: {load_time:.2f} seconds")

    # =====================================
    # PAGE TITLE CHECK
    # =====================================

    title = page.title()

    if title:
        print("Page Title: ✅", title)
    else:
        print("Page Title: ❌ Missing")

    # =====================================
    # BROKEN LINK CHECK
    # =====================================

    links = page.locator("a").all()

    print("\nChecking links...")

    broken_links = []
    working_links = []
    timeout_links = []

    total_links = len(links)

    for index, link in enumerate(links, start=1):

        print(f"Checking link {index}/{total_links}...")

        href = link.get_attribute("href")

        if not href:
            continue

        # Ignore anchor links
        if href.startswith("#"):
            continue

        # Ignore JavaScript links
        if href.startswith("javascript:"):
            continue

        # Convert relative URL to full URL
        full_url = urljoin(url, href)

        try:

            result = page.request.get(
                full_url,
                timeout=3000
            )

            if result.status >= 400:

                broken_links.append(
                    (full_url, result.status)
                )

            else:

                working_links.append(full_url)

        except Exception as e:

            error_message = str(e)

            if "Timeout" in error_message:

                timeout_links.append(full_url)

            else:

                broken_links.append(
                    (full_url, "Request Failed")
                )

    # =====================================
    # BROKEN LINK REPORT
    # =====================================

    print("\n==============================")
    print("BROKEN LINK REPORT")
    print("==============================")

    print("Total Links:", len(links))
    print("Working Links:", len(working_links))
    print("Broken Links:", len(broken_links))
    print("Timeout Links:", len(timeout_links))

    if broken_links:

        print("\nBroken Links:")

        for link, status in broken_links:

            print(
                f"❌ {status} - {link}"
            )

    if timeout_links:

        print("\nTimeout Links:")

        for link in timeout_links:

            print(
                f"⏱️ Timeout - {link}"
            )

    if not broken_links and not timeout_links:

        print("\n✅ No broken or timeout links found!")

    # =====================================
    # IMAGE CHECK
    # =====================================

    images = page.locator("img").all()

    print("\n==============================")
    print("IMAGE REPORT")
    print("==============================")

    print("Total Images:", len(images))

    missing_images = []

    for image in images:

        src = image.get_attribute("src")

        if not src:

            missing_images.append(
                "Image has no src"
            )

            continue

        full_image_url = urljoin(
            url,
            src
        )

        try:

            result = page.request.get(
                full_image_url,
                timeout=10000
            )

            if result.status >= 400:

                missing_images.append(
                    full_image_url
                )

        except Exception:

            missing_images.append(
                full_image_url
            )

    print(
        "Missing Images:",
        len(missing_images)
    )

    if missing_images:

        for image in missing_images:

            print(
                f"❌ {image}"
            )

    else:

        print(
            "✅ No missing images found!"
        )

    # =====================================
    # HTTP ERROR REPORT
    # =====================================

    print("\n==============================")
    print("HTTP ERROR REPORT")
    print("==============================")

    if http_errors:

        print(
            "HTTP Errors Found:",
            len(http_errors)
        )

        for status, error_url in http_errors:

            print(
                f"❌ {status} - {error_url}"
            )

    else:

        print(
            "HTTP Errors Found: 0"
        )

        print(
            "✅ No HTTP errors detected!"
        )

    # =====================================
    # DETERMINE OVERALL STATUS
    # =====================================

    if (
        broken_links
        or missing_images
        or http_errors
    ):

        overall_status = "FAIL"
        status_class = "error"

    elif timeout_links:

        overall_status = "WARNING"
        status_class = "warning"

    else:

        overall_status = "PASS"
        status_class = "success"

    # =====================================
    # CREATE HTML REPORT
    # =====================================

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_filename = (
        f"health_report_{timestamp}.html"
    )

    # =====================================
    # BROKEN LINK HTML
    # =====================================

    broken_links_html = ""

    if broken_links:

        for link, status in broken_links:

            broken_links_html += f"""
            <li>
                <span class="error">
                    ❌ {escape(str(status))}
                </span>
                <br>
                {escape(link)}
            </li>
            """

    else:

        broken_links_html = """
        <li class="success">
            ✅ No broken links
        </li>
        """

    # =====================================
    # TIMEOUT LINK HTML
    # =====================================

    timeout_links_html = ""

    if timeout_links:

        for link in timeout_links:

            timeout_links_html += f"""
            <li>
                <span class="warning">
                    ⏱️ Timeout
                </span>
                <br>
                {escape(link)}
            </li>
            """

    else:

        timeout_links_html = """
        <li class="success">
            ✅ No timeout links
        </li>
        """

    # =====================================
    # MISSING IMAGE HTML
    # =====================================

    missing_images_html = ""

    if missing_images:

        for image in missing_images:

            missing_images_html += f"""
            <li class="error">
                ❌ {escape(image)}
            </li>
            """

    else:

        missing_images_html = """
        <li class="success">
            ✅ No missing images
        </li>
        """

    # =====================================
    # HTTP ERROR HTML
    # =====================================

    http_errors_html = ""

    if http_errors:

        for status, error_url in http_errors:

            http_errors_html += f"""
            <li>
                <span class="error">
                    ❌ HTTP {status}
                </span>
                <br>
                {escape(error_url)}
            </li>
            """

    else:

        http_errors_html = """
        <li class="success">
            ✅ No HTTP errors
        </li>
        """

    # =====================================
    # HTML REPORT
    # =====================================

    report = f"""
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <title>
        Website Health Report
    </title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 40px;
        }}

        .container {{
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }}

        h1 {{
            margin-top: 0;
            color: #222;
        }}

        h2 {{
            margin-top: 30px;
            color: #333;
        }}

        .summary {{
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            background: #f8f8f8;
        }}

        .status {{
            font-size: 28px;
            font-weight: bold;
        }}

        .success {{
            color: green;
        }}

        .warning {{
            color: orange;
        }}

        .error {{
            color: red;
        }}

        .item {{
            padding: 14px;
            margin: 8px 0;
            border-bottom: 1px solid #ddd;
        }}

        ul {{
            line-height: 1.8;
        }}

        .url {{
            word-break: break-all;
        }}

        .footer {{
            margin-top: 30px;
            color: #777;
            font-size: 13px;
        }}

    </style>

</head>


<body>


<div class="container">


    <h1>
        🌐 Website Health Report
    </h1>


    <div class="summary">

        <div>
            Website:
        </div>

        <div class="url">
            <b>{escape(url)}</b>
        </div>

        <br>

        <div>
            Overall Status:
        </div>

        <div class="status {status_class}">
            {overall_status}
        </div>

    </div>


    <h2>
        📊 Summary
    </h2>


    <div class="item">

        <b>HTTP Status:</b>

        {
            response.status
            if response
            else "No response"
        }

    </div>


    <div class="item">

        <b>Page Load Time:</b>

        {load_time:.2f} seconds

    </div>


    <div class="item">

        <b>Page Title:</b>

        <span class="success">

            {
                "✅ Present"
                if title
                else "❌ Missing"
            }

        </span>

    </div>


    <div class="item">

        <b>Total Links:</b>

        {len(links)}

    </div>


    <div class="item">

        <b>Working Links:</b>

        {len(working_links)}

    </div>


    <div class="item">

        <b>Broken Links:</b>

        <span class="
        {"error" if broken_links else "success"}
        ">

            {len(broken_links)}

        </span>

    </div>


    <div class="item">

        <b>Timeout Links:</b>

        <span class="
        {"warning" if timeout_links else "success"}
        ">

            {len(timeout_links)}

        </span>

    </div>


    <div class="item">

        <b>Total Images:</b>

        {len(images)}

    </div>


    <div class="item">

        <b>Missing Images:</b>

        <span class="
        {"error" if missing_images else "success"}
        ">

            {len(missing_images)}

        </span>

    </div>


    <div class="item">

        <b>HTTP Errors:</b>

        <span class="
        {"error" if http_errors else "success"}
        ">

            {len(http_errors)}

        </span>

    </div>


    <h2>
        🔗 Broken Links
    </h2>

    <ul>

        {broken_links_html}

    </ul>


    <h2>
        ⏱️ Timeout Links
    </h2>

    <ul>

        {timeout_links_html}

    </ul>


    <h2>
        🖼️ Missing Images
    </h2>

    <ul>

        {missing_images_html}

    </ul>


    <h2>
        🚨 HTTP Errors
    </h2>

    <ul>

        {http_errors_html}

    </ul>


    <div class="footer">

        Generated automatically by
        Website Health Checker

    </div>


</div>


</body>

</html>
"""

    # =====================================
    # SAVE REPORT
    # =====================================

    with open(
        report_filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)


    print("\n==============================")
    print("HTML REPORT")
    print("==============================")

    print(
        "✅ Report generated:"
    )

    print(
        report_filename
    )


    # =====================================
    # CLOSE BROWSER
    # =====================================

    browser.close()