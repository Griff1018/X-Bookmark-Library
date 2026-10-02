# Privacy Policy for X Bookmark Library

**Last Updated:** OCT 2026

## 1. Overview
X Bookmark Library is a browser extension designed to help users locally save, search, tag, and export their X (Twitter) bookmarks and likes. We prioritize user privacy and operate under a strict zero-data-collection policy.

## 2. Information Collection and Storage
* **Local Storage Only:** All extracted tweet content, images, links, tags, and metadata are saved locally on your device using Chrome's local storage API (`chrome.storage.local`).
* **No Remote Servers:** We do not own, maintain, or transmit data to external databases, analytics platforms, or third-party servers.
* **No Telemetry or Tracking:** The extension does not collect web browsing history, IP addresses, credentials, or user interaction analytics.

## 3. Chrome Extension Permissions
The extension requests only necessary permissions to execute core functions:
* `storage` & `unlimitedStorage`: To store your saved archive on your local device without data loss.
* `sidePanel`: To display your searchable bookmark library alongside active browser tabs.
* `activeTab` & `scripting`: To read HTML elements on active X.com pages only when you trigger a scan.
* Host Permissions (`x.com`, `twitter.com`): Strictly required to read bookmarked post data on official X domains.

## 4. Third-Party Services
This extension interacts solely with X (Twitter) locally within your browser session. It does not send user data to any external APIs or service providers.

## 5. Data Deletion and Portability
Users maintain complete control over their saved data:
* You can export your data anytime as a `.json` backup file.
* Clicking "Clear Archive" inside the side panel immediately and permanently deletes all stored data from your local browser storage.

## 6. Contact & Source Code
X Bookmark Library is open-source. You can review the complete source code or raise issues on GitHub:
https://github.com/Griff1018/X-Bookmark-Library