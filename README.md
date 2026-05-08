<div align="center">

<h1><b>🎥 Motion Detector Security Camera</b></h1>

<p><em>Real-time intruder detection with automated snapshot capture and structured event logging — built with pure OpenCV</em></p>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Scientific-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

<br>

![Motion Detector Security Camera Demo](GIF.gif)

</div>

<br>
<hr>

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Development Phases](#development-phases)
4. [Capstone Highlight](#capstone-highlight)
5. [Getting Started](#getting-started)
6. [Usage](#usage)
7. [Testing](#testing)
8. [Engineering Notes](#engineering-notes)
9. [Roadmap](#roadmap)
10. [Contributing](#contributing)
11. [License](#license)

---

## Overview

A lightweight, zero-dependency security system that runs entirely on a local webcam feed. It uses OpenCV's MOG2 background subtraction algorithm to isolate moving foreground objects, draws bounding boxes around detected motion events, and automatically captures timestamped JPEG snapshots of intruders the moment a new motion event is triggered. Every event is logged with a precise timestamp to a CSV file for audit trails and downstream analysis.

The system distinguishes between persistent motion (already active) and new motion onset — writing to disk only once per event rather than flooding storage on every frame. Designed for a 90-day robotics challenge, it demonstrates core computer vision concepts with production-grade logging discipline.

*Built with: `Python 3.x, OpenCV 4.x, NumPy, csv (stdlib), datetime (stdlib)`.*

### Key Features

- [x] MOG2 background subtraction with configurable history and variance threshold
- [x] Per-event snapshot capture — one JPEG per intruder event, not per frame
- [x] Structured CSV audit log with ISO-formatted timestamps
- [x] Dual-window live display: annotated camera feed + binary motion mask
- [x] Contour filtering by area to suppress sensor noise and shadow artifacts
- [x] Shadow detection enabled via MOG2 `detectShadows=True`
- [x] Graceful release of camera and window resources on `q` key exit
- [x] Single-file, zero-external-service architecture — runs fully offline

---

## Architecture

<details>
<summary>📁 Repository structure</summary>

```text
Motion_Ditector_Security_camara/
├── motion_ditector_security_camara.py   # Core detection engine
├── security_log.csv                     # Auto-generated event audit log
├── GIF.gif                              # Demo recording of the system in action
├── intruder_<timestamp>.jpg             # Auto-generated intruder snapshots (runtime output)
└── README.md                            # This document
```

</details>

**Data flow:**

```text
Webcam Feed
    │
    ▼
MOG2 Background Subtractor  ──►  Binary Foreground Mask
    │                                    │
    │                              Threshold + Dilate
    │                                    │
    │                           Contour Detection (area > 1000 px²)
    │                                    │
    ├── Motion Onset? ──YES──►  Save JPEG snapshot
    │                           Append row to security_log.csv
    │                           Set motion_active = True
    │
    └── Draw bounding boxes on frame → Display both windows
```

---

## Development Phases

| Phase | Goal | Status | Outcome |
|-------|------|--------|---------|
| v0.1 | Live webcam feed with OpenCV | ✅ Done | Camera stream rendering at full framerate |
| v0.2 | MOG2 background subtraction integration | ✅ Done | Foreground mask isolation working |
| v0.3 | Contour detection and bounding box rendering | ✅ Done | Motion regions highlighted on live feed |
| v0.4 | Edge-triggered event logic (onset detection) | ✅ Done | Single log entry per event, not per frame |
| v0.5 | Automated JPEG snapshot capture on intrusion | ✅ Done | Timestamped intruder photos saved to disk |
| v0.6 | CSV audit logging with ISO timestamps | ✅ Done | `security_log.csv` captures all motion events |
| v0.7 | Dual-window display (feed + mask) | ✅ Done | Real-time visual debugging of detection pipeline |
| v1.0 | Stable single-script deployable system | ✅ Done | Runs offline, no external services required |

> **Note:** Status indicators follow the convention: ✅ Complete · 🔄 In Progress · 🗓 Planned.

---

## Capstone Highlight

- **Edge-triggered detection** — Logging fires only on motion *onset*, preventing log spam and redundant disk writes across continuous motion frames
- **MOG2 shadow suppression** — `detectShadows=True` + binary threshold at 254 eliminates shadow-induced false positives that plague simpler frame-difference approaches
- **Filename-safe timestamps** — ISO format used for CSV logs; colon-free `YYYY-MM-DD_HH-MM-SS` format used for filenames to ensure cross-platform file system compatibility
- **Contour area gating** — The 1000 px² minimum area filter discards small sensor noise and minor lighting fluctuations without requiring any machine learning
- **Dual-window pipeline visibility** — Exposes both the annotated camera feed and the raw binary mask simultaneously, enabling real-time tuning of detection thresholds during development
- **Stateful motion tracking** — The `motion_active` flag decouples event detection from per-frame rendering, keeping the main loop lean and the CSV log clean

---

## Getting Started

### Prerequisites

- Python ≥ 3.8
- A connected webcam (device index `0` by default)
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Relvixx/Motion_Detector_Security_Camera.git
cd Motion_Detector_Security_Camera

# 2. (Recommended) Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install opencv-python numpy
```

### Environment Variables

This project requires no environment variables. All configuration (camera index, MOG2 parameters, contour area threshold) is set directly in the script constants.

| Variable | Description | Required |
|----------|-------------|----------|
| — | No env vars required | — |

---

## Usage

```bash
# Run the motion detector (webcam index 0 is used by default)
python motion_ditector_security_camara.py

# Two windows will open:
#   "Security Camera"   — Live annotated feed with bounding boxes
#   "Clean Solid Mask"  — Binary foreground mask from MOG2

# Press 'q' in either window to stop the process cleanly.
# Intruder snapshots are saved as: intruder_YYYY-MM-DD_HH-MM-SS.jpg
# Event log is written to:         security_log.csv
```

> [!TIP]
> Allow 2–3 seconds after launch for MOG2 to establish a stable background model before moving in front of the camera. Motion detected during the warm-up period may produce false positives as the algorithm has not yet converged on the scene background.

---

## Testing

```bash
# Verify dependencies are importable and the camera index is accessible
python -c "import cv2; import numpy as np; cap = cv2.VideoCapture(0); print('Camera OK:', cap.isOpened()); cap.release()"
```

> [!NOTE]
> No automated test suite exists yet — this is a single-script computer vision tool where correctness is validated empirically by observing live detection accuracy, snapshot quality, and CSV log integrity. The verification checklist is: (1) both windows open without error, (2) bounding boxes appear on movement, (3) `security_log.csv` gains exactly one new row per motion event, and (4) JPEG snapshots are written with correct filenames.

---

## Engineering Notes

> [!NOTE]
> MOG2's `history=100` parameter means the background model adapts to scene changes over approximately 100 frames (~3 seconds at 30 fps). Increasing this value improves stability in scenes with gradual lighting changes (e.g., clouds moving past a window) but slows adaptation to permanent scene changes like furniture being moved.

> [!IMPORTANT]
> The script overwrites `security_log.csv` on every launch — the file is re-created with fresh headers at startup. If you need persistent logs across sessions, remove the `open('security_log.csv', 'w', ...)` block at the top and let the append-mode writes accumulate across runs.

> [!WARNING]
> JPEG snapshots are written to the current working directory with no deduplication or storage cap. On a busy scene, long unattended runs can fill disk storage. Implement a snapshot directory with a file count or size limit before deploying in a production environment.

### Known Limitations

- Single-camera support only — no multi-feed aggregation
- No motion-end event logging (`Motion Stopped` is never written to CSV)
- `motion_active` flag never resets to `False` — once triggered, subsequent motion onset events in the same session are not re-logged
- No alerting mechanism (email, SMS, webhook) — detection is local-only
- Detection performance degrades under significant lighting changes (e.g., lights turning on/off) until MOG2 re-converges

---

## Roadmap

- [ ] Reset `motion_active` flag after configurable inactivity timeout (e.g., 5 seconds of no contours)
- [ ] Log `Motion Stopped` events with duration to CSV
- [ ] Add email/webhook alert on first motion detection
- [ ] Configurable camera index and threshold values via CLI arguments (`argparse`)
- [ ] Multi-camera support with per-feed log files
- [ ] Web dashboard to view live feed and browse snapshot gallery
- [ ] Docker container for headless deployment (no display server required)
- [ ] Frame rate throttle option to reduce CPU load on low-power hardware

---

## Contributing

Fork the repository, create a feature branch (`git checkout -b feat/your-feature`), commit your changes, and open a pull request against `main`. Keep changes focused — one concern per PR. Match the existing code style: inline comments in English, descriptive variable names, and no external dependencies beyond `opencv-python` and `numpy` unless thoroughly justified in the PR description.

> [!IMPORTANT]
> Before opening a PR, manually verify the full pipeline end-to-end: camera opens, motion detection triggers, a JPEG snapshot is saved, and the CSV log receives exactly one new row per event. Include a brief description of your test conditions (lighting, distance, camera model) in the PR body.

---

## License

[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](./LICENSE)

Distributed under the MIT License. See `LICENSE` for full terms.

---

<div align="center">
<sub>Built with ♥ by <a href="https://github.com/Relvixx">Relvixx</a> &nbsp;·&nbsp; Motion Detector Security Camera &nbsp;·&nbsp; 2026</sub>
</div>
