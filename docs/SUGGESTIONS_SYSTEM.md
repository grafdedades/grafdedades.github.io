# Suggestions System Documentation

This document details the architecture and workflows for the **User Suggestions System** of the Graf de Dades project. This system allows authenticated users to propose new nodes and connections, and administrators to review and merge them into the dataset.

## 1. System Overview

The system operates on a **Serverless Hybrid Architecture**:

*   **Frontend**: Static HTML/JS pages hosted on GitHub Pages (`suggest.html`, `admin.html`).
*   **Backend / API**: A **Google Apps Script** deployment acts as the API and Authentication Proxy.
*   **Database**: A **Google Sheet** (in the same Drive account) acts as the persistence layer for pending/rejected suggestions.
*   **Authentication**: **GitHub OAuth 2.0** is used for identity verification.

---

## 2. Suggestion Flow (User)

**Entry Point**: `suggest.html`

1.  **Authentication**:
    *   The user must log in with GitHub (`read:user`, `user:email` scopes).
    *   This ensures every suggestion is linked to a verified real identity (GitHub username + real name provided in form).

2.  **Creation**:
    *   Users can create **Nodes** (People), **Edges** (Connections), or **Manual Requests** (Other).
    *   **Manual Requests**: Used for complex changes (e.g., deleting a node, merging duplicates) that require human intervention.
    *   The interface validates data (e.g., year ranges, duplicate checks against the live graph).
    *   Items are added to a temporary "Cart".

3.  **Submission**:
    *   The user provides their **Real Name** (confidential, for admin verification).
    *   The frontend sends a POST request with the cart payload to the **Apps Script**.
    *   **Apps Script Action**: Appends a new row to the Google Sheet with status `pending`.

---

## 3. Admin Review Flow (Contributor)

**Entry Point**: `admin.html`

1.  **Authentication (Admin)**:
    *   Admins must log in with **repo** scope.
    *   The frontend verifies the user has **Push permissions** to the `grafdedades.github.io` repository via the GitHub API.

2.  **Dashboard**:
    *   Displays all suggestions (`pending`, `accepted`, `rejected`) fetched from the Apps Script.
    *   Admins can expand bundles to see specific data (years, relationship types, comments).

3.  **Action - Rejection**:
    *   **Action**: Clicking "Reject" updates the status row in the Google Sheet to `rejected` via the Apps Script API.

4.  **Action - Acceptance (Merge)**:
    *   **Requirement**: The Admin must provide the current **Encryption Password**.
    *   **Process**:
        1.  **Fetch**: Frontend fetches the *latest* `data/graph_data.enc` from GitHub (Master/Testing branch).
        2.  **Decrypt**: Decrypts the data in the browser using the password.
        3.  **Merge**: 
            *   **Nodes/Edges**: Adds the new items to the in-memory graph.
            *   **Manual Requests**: These are *acknowledged* (counted) but **NOT added** to the graph automatically. The admin must apply these changes manually (e.g., by editing the JSON locally) if needed, or simply mark them as resolved.
        4.  **Encrypt**: Re-encrypts the updated graph (generating both `graph_data.enc` and the public `encrypted_data.txt`).
        5.  **Commit**: Uses the GitHub API to direct-commit/push the updated files to the repository.
        6.  **Close Loop**: Updates the Google Sheet status to `accepted` via Apps Script.

---

## 4. Managing Administrators

To add a new **Admin** to the system:

1.  Go to the GitHub Repository **Settings** > **Collaborators**.
2.  **Add People**: Invite the user by email or username.
3.  **Role**: Ensure they have **Write** (or Admin) access.
    *   *Read-only* users cannot accept suggestions (cannot push to the repo).
    *   Once added, they can log in at `admin.html` and will have full dashboard access.

---

## 5. Backend Maintenance (Apps Script)

The backend logic resides in a Google Apps Script project associated with the **Graf de Dades Google Account**.

### Script Location
*   **Google Drive**: Account `grafdedades@gmail.com` (or current owner).
*   **File**: `Backend Script` (or similar name).

### Updating the Backend (`code.js`)
If you need to change the API logic (e.g., add new fields to the Sheet):

1.  **Edit**: Modify the `code.js` file in the Google Apps Script editor.
2.  **Deploy**:
    *   Go to **Deploy** > **Manage Deployments**.
    *   Edit the "Active" deployment (usually "Web App").
    *   **IMPORTANT**: You MUST select **Version: New version** for changes to take effect.
    *   Click **Deploy**.
3.  **Update Frontend (If URL changed)**:
    *   If you created a fresh deployment instead of updating the existing one, the URL will change.
    *   Update `CONFIG.scriptUrl` in `js/auth.js`.

### Google Sheet Structure
The script expects a Sheet with columns roughly following:
*   `id` (UUID)
*   `timestamp`
*   `user` (GitHub Login)
*   `realName`
*   `payload` (JSON string of items)
*   `status` (`pending` | `accepted` | `rejected`)
*   `comment`
*   `processedBy`

---

## 5. Security Notes

*   **OAuth Scopes**:
    *   **Users**: Minimal access (`read:user`). Cannot modify code or data directly.
    *   **Admins**: Write access (`repo`). Can directly commit to the repo via the Dashboard.
*   **Encryption**:
    *   The encryption password is **never sent to the server**.
    *   Decryption and re-encryption happen entirely in the Admin's browser (`admin.html`).
