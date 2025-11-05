# Icons

Place platform-specific icons for the packaged application in this directory.

- `barcode-xpress.icns` – macOS app icon (512×512 multi-resolution).
- `barcode-xpress.ico` – Windows executable icon (256×256 multi-resolution).
- (Optional) `barcode-xpress.png` – Linux icon for one-file builds.

You can generate these from a high-resolution PNG using native tools:

```bash
# macOS: convert icon.png to .icns with all required resolutions
mkdir icon.iconset

# Generate all required sizes and their @2x Retina variants
sips -z 16 16 icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32 icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32 icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64 icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 64 64 icon.png --out icon.iconset/icon_64x64.png
sips -z 128 128 icon.png --out icon.iconset/icon_64x64@2x.png
sips -z 128 128 icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256 icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256 icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512 icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512 icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# Create .icns file
iconutil -c icns icon.iconset -o assets/icons/barcode-xpress.icns

# Clean up temporary files
rm -rf icon.iconset

# Windows (requires ImageMagick):
magick icon.png -resize 256x256 assets/icons/barcode-xpress.ico
```

After adding the icon files, rerun `./build.sh` (macOS/Linux) or
`pwsh -File build.ps1 -Clean` (Windows) to bake the icons into the bundles.
