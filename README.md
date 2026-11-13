# Sunshine OS — website

### 🌐 **[Open the live page → tak0dan.github.io/sunshineos-site](https://tak0dan.github.io/sunshineos-site/)**

The site of [Sunshine OS](https://github.com/tak0dan/SunshineOS), an Arch-based distribution with a carefully configured
desktop, a unified software store and a complete set of tools for maintenance and recovery. It is one static page served by
GitHub Pages: no build step, no framework.

![Sunshine OS home page](assets/screenshots/hero.png)

## A beautiful desktop. A system built to work.

Sunshine OS combines the freedom and freshness of Arch Linux with the convenience of a carefully configured desktop
experience. Get the latest packages, a unified software store, an intuitive Hyprland desktop and a complete set of tools for
system maintenance and recovery.

**Beautiful on the surface. Thoughtfully engineered underneath.**

![Introduction](assets/screenshots/intro.png)

## Install

The download button reads `release.json`, so the file name, version, architecture and size on the button always match the
newest published ISO. The page also shows the USB command with the real file name, and the SHA-256 of the image.

![Install section](assets/screenshots/install.png)

## What is included

Two desktop environments (KDE Plasma and Hyprland), Btrfs snapshots, the Sunshine Store, wallpaper-derived colours, boot and
package-manager repair, disk encryption, and more.

![Features](assets/screenshots/features.png)

## System tools

Commands for checking and repairing the system: `sunshine-doctor`, `sunshine-snapshot`, `sunshine-identity`,
`sunshine-boot-repair`, `sunshine-fix-pacman`, `sunshine-cleanup`, `sunshine-update`.

![System tools](assets/screenshots/tools.png)

## Specifications

![Specifications](assets/screenshots/specs.png)

## Themes

The page takes its colours from the same palette as the desktop. Press `T` to switch between Sunrise, Noon, Ember, Dusk
and Midnight.

![Themes](assets/screenshots/themes.png)

## Repository layout

| Path | Purpose |
| --- | --- |
| `index.html` | The whole page: markup, styles and scripts |
| `release.json` | Published releases; the download button and the Releases list are generated from it |
| `assets/` | Pixel logo sprite sheets, wallpapers and screenshots |

## Releasing

`tools/release-github.sh` in the [Sunshine OS repository](https://github.com/tak0dan/SunshineOS) uploads the ISO and adds an
entry to `release.json`. Push that file and the page shows the new version without any edit to `index.html`.

## Run locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```
