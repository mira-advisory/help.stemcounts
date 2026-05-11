# Help-media upload checklist

Every `<HelpMedia>` reference across the StemCounts help site, listed by article. **50 files total** — 34 images + 16 short videos.

## How to upload

Every file goes into one S3 bucket, at the root level — no folders.

**Bucket name:**

```
help-media.stemcounts.com
```

### Step-by-step

1. Sign in to the AWS Console at <https://console.aws.amazon.com>.
2. In the top search bar, type **S3** and click the S3 service.
3. From the bucket list, click into **`help-media.stemcounts.com`**.
4. Click the orange **Upload** button (top-right).
5. Drag your captured files into the drop zone (or click **Add files** and pick them).
6. Leave all the default options as they are. Don't create folders.
7. Click **Upload** at the bottom.

Once a batch is uploaded, the images will appear on the live help site after the next docs rebuild (usually within a few hours, or sooner if you ping the dev team to trigger one).

### Filename rules

- Use the **exact filename** shown in each section below. Copy the code block — don't retype it.
- Extensions matter: `.png` for screenshots, `.mp4` for short videos.
- No spaces, no capitals, no folder paths.

### Capture guidelines

- **Screenshots**: capture at 2× (Retina) for crispness; aim for around 2400px wide max.
- **Videos**: MP4, H.264, max 1080p, ideally under 20 MB and under 30 seconds.
- **Redact**: blur or replace any real florist names, customer names, real prices, or addresses before saving.

If you don't have AWS access, send the captured files to whoever does — the upload step is just drag-and-drop and takes seconds.

## What to capture

Each section below is one article on the help site. The article link opens the live page so you can see the context the image / video sits in. The code block is the **exact filename** to save the captured file as — click the copy icon in the top-right of the block.

### [Creating your account](/getting-started/creating-your-account/)

- [ ] **🎥 video**

  ```
  signup-flow-overview.mp4
  ```

- [ ] image

  ```
  signup-role-selection.png
  ```

  *Shows:* Florist vs Wholesaler role picker

- [ ] image

  ```
  signup-otp-screen.png
  ```

  *Shows:* OTP entry — the code arrives by SMS to the phone you registered with


### [Finding your way around](/getting-started/finding-your-way-around/)

- [ ] **🎥 video**

  ```
  app-shell-overview.mp4
  ```

  *Shows:* A quick tour of the StemCounts header and navigation

- [ ] image

  ```
  user-menu-open.png
  ```


### [Forgot your password](/getting-started/forgot-password/)

- [ ] image

  ```
  login-forgot-password-link.png
  ```

- [ ] image

  ```
  reset-password-form.png
  ```


### [Welcome to StemCounts](/getting-started/welcome/)

- [ ] **🎥 video**

  ```
  welcome-platform-overview.mp4
  ```


### [Your first 10 minutes](/getting-started/your-first-10-minutes/)

- [ ] image

  ```
  florist-landing-new-order-cta.png
  ```

- [ ] image

  ```
  event-add-arrangement.png
  ```

- [ ] **🎥 video**

  ```
  flower-picker-quantity.mp4
  ```

- [ ] image

  ```
  order-send-confirmation.png
  ```


### [Browsing the flower catalog](/florists/browsing-the-catalog/)

- [ ] **🎥 video**

  ```
  flower-library-grid.mp4
  ```

  *Shows:* Browsing the Flower Library


### [Building an arrangement](/florists/building-an-arrangement/)

- [ ] **🎥 video**

  ```
  event-details-with-arrangements.mp4
  ```

  *Shows:* An event with three arrangements

- [ ] image

  ```
  add-arrangement-button.png
  ```


### [Cloning arrangements](/florists/cloning-arrangements/)

- [ ] image

  ```
  arrangement-3-dot-menu.png
  ```

  *Shows:* The 3-dot menu on an arrangement card

- [ ] **🎥 video**

  ```
  arrangement-clone-action.mp4
  ```


### [Creating your first event](/florists/creating-your-first-event/)

- [ ] **🎥 video**

  ```
  event-creation-overview.mp4
  ```

  *Shows:* An event being added to a weekly order

- [ ] image

  ```
  add-event-modal.png
  ```


### [Event details & printing](/florists/event-details-and-printing/)

- [ ] image

  ```
  event-printable-page.png
  ```

  *Shows:* A printable event sheet, ready to send to a printer or PDF

- [ ] image

  ```
  event-print-dialog.png
  ```


### [The florist landing page](/florists/florist-landing/)

- [ ] **🎥 video**

  ```
  florist-landing-overview.mp4
  ```

  *Shows:* A quick look at the florist home screen

- [ ] image

  ```
  florist-landing-primary-ctas.png
  ```


### [Pricing and budgets](/florists/pricing-and-budgets/)

- [ ] image

  ```
  pricing-overview.png
  ```

  *Shows:* The cost-vs-customer-price relationship


### [Sending your order](/florists/sending-your-order/)

- [ ] image

  ```
  send-order-button.png
  ```

  *Shows:* The Send Order action on a weekly order

- [ ] image

  ```
  order-status-sent.png
  ```


### [The Flower Picker](/florists/the-flower-picker/)

- [ ] **🎥 video**

  ```
  flower-picker-overview.mp4
  ```

  *Shows:* Walking through the Flower Picker

- [ ] image

  ```
  flower-picker-card-expanded.png
  ```


### [The Spares Bucket](/florists/the-spares-bucket/)

- [ ] image

  ```
  spares-bucket-on-event.png
  ```

  *Shows:* The Spares Bucket sits alongside arrangements on the event page


### [Tracking your order](/florists/tracking-your-order/)

- [ ] image

  ```
  order-status-flow.png
  ```

  *Shows:* The five stages florists see


### [Assign & Send](/wholesalers/assign-and-send/)

- [ ] **🎥 video**

  ```
  assign-and-send-overview.mp4
  ```

  *Shows:* Walking through Assign & Send end to end

- [ ] image

  ```
  assign-supplier-dropdown.png
  ```

  *Shows:* Selecting a supplier for an aggregated flower row

- [ ] image

  ```
  confirm-supplier-order.png
  ```

  *Shows:* Confirming a supplier order moves it to Confirmed & Ready


### [Confirmed & Ready](/wholesalers/confirmed-and-ready/)

- [ ] **🎥 video**

  ```
  confirmed-and-ready-overview.mp4
  ```

  *Shows:* Marking supplier-fulfilled items and then ready for florist

- [ ] image

  ```
  mark-supplier-fulfilled.png
  ```

- [ ] image

  ```
  ready-florist-view-toggle.png
  ```

  *Shows:* Toggle between List view and Florist view


### [Daily pick-lists](/wholesalers/daily-pick-lists/)

- [ ] image

  ```
  pick-list-printable.png
  ```

  *Shows:* A printable pick-list for one florist's order


### [Managing your inventory](/wholesalers/managing-inventory/)

- [ ] image

  ```
  inventory-management-page.png
  ```

  *Shows:* Inventory Management with selected flowers + price overrides


### [Multi-supplier orders](/wholesalers/multi-supplier-orders/)

- [ ] image

  ```
  multi-supplier-diagram.png
  ```

  *Shows:* One florist order → multiple supplier orders → reconstituted at handover


### [Receive & Accept](/wholesalers/receive-and-accept/)

- [ ] **🎥 video**

  ```
  receive-and-accept-view.mp4
  ```

  *Shows:* Reviewing an incoming order in Receive & Accept

- [ ] image

  ```
  accept-order-button.png
  ```


### [The Order Board](/wholesalers/the-order-board/)

- [ ] **🎥 video**

  ```
  order-board-overview.mp4
  ```

  *Shows:* The Order Board in action

- [ ] **🎥 video**

  ```
  order-board-drag.mp4
  ```

  *Shows:* Dragging an order from Sent to Accepted


### [The wholesaler landing page](/wholesalers/wholesaler-landing/)

- [ ] **🎥 video**

  ```
  wholesaler-landing-overview.mp4
  ```

  *Shows:* A quick look at the wholesaler home screen


### [Managing your subscription](/billing/managing-subscription/)

- [ ] image

  ```
  manage-subscription-button.png
  ```

  *Shows:* The Manage subscription button opens the Stripe portal


### [Profile and notifications](/billing/profile-and-notifications/)

- [ ] image

  ```
  settings-personal-tab.png
  ```

  *Shows:* Personal settings tab


### [Your StemCounts subscription](/billing/subscription/)

- [ ] image

  ```
  account-subscription-card.png
  ```

  *Shows:* The Subscription card on the Account page

- [ ] image

  ```
  subscribe-button.png
  ```


### [Trial and blocked access](/billing/trial-and-blocked-access/)

- [ ] image

  ```
  subscription-blocked-screen.png
  ```

  *Shows:* The Subscription Access Blocked screen


### [Your organisation](/billing/your-organisation/)

- [ ] image

  ```
  settings-organization-tab.png
  ```

  *Shows:* Organisation settings


---

## Quick alphabetical lookup

If you need to find a specific filename fast:

- `accept-order-button.png` → [Receive & Accept](/wholesalers/receive-and-accept/)
- `account-subscription-card.png` → [Your StemCounts subscription](/billing/subscription/)
- `add-arrangement-button.png` → [Building an arrangement](/florists/building-an-arrangement/)
- `add-event-modal.png` → [Creating your first event](/florists/creating-your-first-event/)
- `app-shell-overview.mp4` → [Finding your way around](/getting-started/finding-your-way-around/)
- `arrangement-3-dot-menu.png` → [Cloning arrangements](/florists/cloning-arrangements/)
- `arrangement-clone-action.mp4` → [Cloning arrangements](/florists/cloning-arrangements/)
- `assign-and-send-overview.mp4` → [Assign & Send](/wholesalers/assign-and-send/)
- `assign-supplier-dropdown.png` → [Assign & Send](/wholesalers/assign-and-send/)
- `confirm-supplier-order.png` → [Assign & Send](/wholesalers/assign-and-send/)
- `confirmed-and-ready-overview.mp4` → [Confirmed & Ready](/wholesalers/confirmed-and-ready/)
- `event-add-arrangement.png` → [Your first 10 minutes](/getting-started/your-first-10-minutes/)
- `event-creation-overview.mp4` → [Creating your first event](/florists/creating-your-first-event/)
- `event-details-with-arrangements.mp4` → [Building an arrangement](/florists/building-an-arrangement/)
- `event-print-dialog.png` → [Event details & printing](/florists/event-details-and-printing/)
- `event-printable-page.png` → [Event details & printing](/florists/event-details-and-printing/)
- `florist-landing-new-order-cta.png` → [Your first 10 minutes](/getting-started/your-first-10-minutes/)
- `florist-landing-overview.mp4` → [The florist landing page](/florists/florist-landing/)
- `florist-landing-primary-ctas.png` → [The florist landing page](/florists/florist-landing/)
- `flower-library-grid.mp4` → [Browsing the flower catalog](/florists/browsing-the-catalog/)
- `flower-picker-card-expanded.png` → [The Flower Picker](/florists/the-flower-picker/)
- `flower-picker-overview.mp4` → [The Flower Picker](/florists/the-flower-picker/)
- `flower-picker-quantity.mp4` → [Your first 10 minutes](/getting-started/your-first-10-minutes/)
- `inventory-management-page.png` → [Managing your inventory](/wholesalers/managing-inventory/)
- `login-forgot-password-link.png` → [Forgot your password](/getting-started/forgot-password/)
- `manage-subscription-button.png` → [Managing your subscription](/billing/managing-subscription/)
- `mark-supplier-fulfilled.png` → [Confirmed & Ready](/wholesalers/confirmed-and-ready/)
- `multi-supplier-diagram.png` → [Multi-supplier orders](/wholesalers/multi-supplier-orders/)
- `order-board-drag.mp4` → [The Order Board](/wholesalers/the-order-board/)
- `order-board-overview.mp4` → [The Order Board](/wholesalers/the-order-board/)
- `order-send-confirmation.png` → [Your first 10 minutes](/getting-started/your-first-10-minutes/)
- `order-status-flow.png` → [Tracking your order](/florists/tracking-your-order/)
- `order-status-sent.png` → [Sending your order](/florists/sending-your-order/)
- `pick-list-printable.png` → [Daily pick-lists](/wholesalers/daily-pick-lists/)
- `pricing-overview.png` → [Pricing and budgets](/florists/pricing-and-budgets/)
- `ready-florist-view-toggle.png` → [Confirmed & Ready](/wholesalers/confirmed-and-ready/)
- `receive-and-accept-view.mp4` → [Receive & Accept](/wholesalers/receive-and-accept/)
- `reset-password-form.png` → [Forgot your password](/getting-started/forgot-password/)
- `send-order-button.png` → [Sending your order](/florists/sending-your-order/)
- `settings-organization-tab.png` → [Your organisation](/billing/your-organisation/)
- `settings-personal-tab.png` → [Profile and notifications](/billing/profile-and-notifications/)
- `signup-flow-overview.mp4` → [Creating your account](/getting-started/creating-your-account/)
- `signup-otp-screen.png` → [Creating your account](/getting-started/creating-your-account/)
- `signup-role-selection.png` → [Creating your account](/getting-started/creating-your-account/)
- `spares-bucket-on-event.png` → [The Spares Bucket](/florists/the-spares-bucket/)
- `subscribe-button.png` → [Your StemCounts subscription](/billing/subscription/)
- `subscription-blocked-screen.png` → [Trial and blocked access](/billing/trial-and-blocked-access/)
- `user-menu-open.png` → [Finding your way around](/getting-started/finding-your-way-around/)
- `welcome-platform-overview.mp4` → [Welcome to StemCounts](/getting-started/welcome/)
- `wholesaler-landing-overview.mp4` → [The wholesaler landing page](/wholesalers/wholesaler-landing/)
