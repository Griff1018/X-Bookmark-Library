# X Bookmark Library

A privacy-focused Manifest V3 Chrome extension that indexes your X (Twitter) bookmarks and likes into a local, searchable archive with an integrated side panel, full-page visual showcase, and media recovery engine.

## Overview

X Bookmark Library allows users to scan their logged-in X bookmarks (`x.com/i/bookmarks`), history, and likes (`x.com/i/history/likes`) directly into browser local storage. It provides instant client-side full-text search, advanced query operators, custom tagging, high-resolution media recovery, and JSON backup/restore capabilities without relying on third-party servers.

## Features

### Fast Archiving and Deduplication
- Scans `x.com/i/history`, `x.com/i/bookmarks`, and `x.com/i/history/likes`.
- Automatically streams and saves posts during the scan process.
- Intelligently deduplicates by post ID while preserving multi-collection associations (bookmarked, liked, or both).
- Non-blocking DOM inspection and mutation observing for reliable image detection.

### Instant Client-Side Search
- Real-time full-text search with keyword highlighting.
- Exact phrase matching using quotes (`"..."`).
- Author filtering by handle (`from:username`).
- Tag-based filtering (`tag:name`).
- Media type filters (`has:image`, `has:multiple-images`, `has:video`, `has:link`, `has:text`).
- Date boundary filtering (`after:YYYY-MM-DD`, `before:YYYY-MM-DD`).
- Collection filtering (All Saved, Bookmarks, Likes).

### Full-Page Visual Showcase
- Responsive masonry grid layout.
- Adjustable card widths (slider control or `Ctrl` + mouse wheel).
- Sequential, lazy-loaded media rendering with retry fallbacks.
- Full-screen image preview modal.
- Video badges with quick-launch links to original posts.

### Media and Thumbnail Recovery
- Background inspection engine for posts lacking images or video previews.
- Automatically captures media posters, video player thumbnails, and GIF previews.
- Context-menu action to refetch individual post metadata and media on demand.

### Tag Management
- Directly add and remove custom tags on cards in both the Side Panel and Showcase.
- Centralized tag filtering with autocomplete suggestions.

### Data Ownership and Portability
- 100% offline and local storage (`chrome.storage.local`).
- One-click JSON backup export.
- Reliable chunked JSON import that merges into existing archives without overwriting custom tags or collection metadata.

## Search Syntax

| Operator | Description | Example |
| :--- | :--- | :--- |
| `"exact phrase"` | Matches posts containing the exact string | `"system design"` |
| `from:handle` | Filters posts by author username | `from:karpathy` |
| `tag:name` | Filters posts assigned a specific custom tag | `tag:ai` |
| `has:image` | Matches posts containing at least one image | `has:image` |
| `has:multiple-images` | Matches posts containing two or more images | `has:multiple-images` |
| `has:video` | Matches posts containing videos or GIFs | `has:video` |
| `has:link` | Matches posts containing external links | `has:link` |
| `has:text` | Matches text-only posts without media or links | `has:text` |
| `after:YYYY-MM-DD` | Matches posts published on or after the specified date | `after:2025-01-01` |
| `before:YYYY-MM-DD` | Matches posts published before the specified date | `before:2026-01-01` |

Multiple operators can be combined in a single query (for example: `from:jack has:image "announcement"`).

## Installation

1. Clone or download this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/x-bookmark-library.git
   ```
2. Open Google Chrome and navigate to `chrome://extensions/`.
3. Enable **Developer mode** using the toggle in the top-right corner.
4. Click **Load unpacked** and select the project directory.
5. The extension icon will appear in your Chrome toolbar.

## Usage

1. Open your browser and navigate to [X (Twitter)](https://x.com). Ensure you are logged into your account.
2. Go to any of the following supported pages:
   - Bookmarks: `https://x.com/i/bookmarks`
   - History: `https://x.com/i/history`
   - Likes: `https://x.com/i/history/likes`
3. Click the extension icon in the Chrome toolbar to open the **Side Panel**.
4. Click **Scan X Bookmarks** (or **Scan X Likes**) to initiate the indexing process.
5. Once indexed, search and tag posts directly within the Side Panel, or click **Showcase** to launch the full-screen visual library.

## Project Structure

```text
├── manifest.json       # Extension configuration (Manifest V3)
├── background.js       # Service worker managing storage synchronization and caching
├── content.js          # In-page script handling DOM extraction and feed scanning
├── sidepanel.html      # Side panel user interface markup
├── sidepanel.js        # Side panel controller, search indexer, and event handlers
├── sidepanel.css       # Side panel styling
├── showcase.html       # Full-page visual gallery markup
├── showcase.js         # Showcase controller, masonry grid, and media recovery engine
├── showcase.css        # Showcase styling
└── icons/              # Extension application icons
```

## JSON Data Specification

Exported JSON files adhere to the following schema:

```json
{
  "format": "x-bookmark-library",
  "version": 2,
  "exportedAt": "2026-10-02T00:00:00.000Z",
  "count": 1,
  "bookmarks": [
    {
      "tweetId": "1234567890123456789",
      "handle": "username",
      "displayName": "User Name",
      "text": "Post content...",
      "createdAt": "2026-01-01T12:00:00.000Z",
      "tweetUrl": "https://x.com/username/status/1234567890123456789",
      "avatar": "https://pbs.twimg.com/profile_images/...",
      "images": [
        "https://pbs.twimg.com/media/..."
      ],
      "hasVideo": false,
      "hasQuote": false,
      "externalLinks": [
        "https://example.com"
      ],
      "stats": {
        "replies": 12,
        "reposts": 45,
        "likes": 230,
        "bookmarks": 80,
        "views": 5200
      },
      "collections": [
        "bookmark",
        "like"
      ],
      "tags": [
        "reference",
        "tech"
      ],
      "importedAt": "2026-10-02T00:00:00.000Z"
    }
  ]
}
```

Older backup files lacking the `collections` property remain fully backward-compatible and will automatically default to `["bookmark"]`.

## Privacy and Security

- **Strictly Local**: All bookmark data, text, and media URLs are stored locally via `chrome.storage.local`.
- **Zero Remote Communication**: The extension makes no external network requests other than loading required page assets from X's official domain (`x.com`, `twitter.com`, and `pbs.twimg.com`).
- **No Analytics**: No user tracking, telemetry, or analytics scripts are bundled or loaded.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
