#!/bin/bash

# LLM Council - MacOS App Generator
# This script creates a .app bundle that can be placed in the Dock.

APP_NAME="LLM Council"
APP_DIR="${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

echo "Creating ${APP_NAME}.app..."

# 1. Create Directory Structure
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

# 2. Create Info.plist
cat > "${CONTENTS_DIR}/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>LLM Council Launcher</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.llmcouncil.app</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.10</string>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF

# 3. Create the Launcher Script
# This script runs inside the .app and handles starting the server
cat > "${MACOS_DIR}/LLM Council Launcher" <<EOF
#!/bin/bash

# Get the directory where the script is located
DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="\$(dirname "\$(dirname "\$(dirname "\$DIR")")")"

# Navigate to project root
cd "\$PROJECT_ROOT"

# Open Terminal to show server logs and keep process alive
osascript <<END
tell application "Terminal"
    do script "cd '$PROJECT_ROOT' && ./run_portable.sh; exit"
end tell
END

# Wait a moment for server to start, then open browser
sleep 3
open "http://localhost:8010"
EOF

# Make the launcher executable
chmod +x "${MACOS_DIR}/LLM Council Launcher"

echo "✓ Created ${APP_NAME}.app"
echo "You can drag '${APP_NAME}.app' to your Dock or Applications folder."
