# Icons

Place platform-specific icons for the packaged application in this directory.

- `barcode-xpress.icns` – macOS app icon (512×512 multi-resolution).
- `barcode-xpress.ico` – Windows executable icon (256×256 multi-resolution).
- (Optional) `barcode-xpress.png` – Linux icon for one-file builds.

You can generate these from a high-resolution PNG using native tools:

```bash
# macOS: convert icon.png to .icns
sips -z 256 256 icon.png --out icon-256.png
sips -z 512 512 icon.png --out icon-512.png
mkdir icon.iconset
cp icon-256.png icon.iconset/icon_256x256.png
cp icon-512.png icon.iconset/icon_512x512.png
iconutil -c icns icon.iconset -o assets/icons/barcode-xpress.icns

# Windows (requires ImageMagick):
magick icon.png -resize 256x256 assets/icons/barcode-xpress.ico
```

After adding the icon files, rerun `./build.sh` (macOS/Linux) or
`pwsh -File build.ps1 -Clean` (Windows) to bake the icons into the bundles.
