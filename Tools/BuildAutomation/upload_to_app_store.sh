#!/bin/bash
# Unity Build Automation post-build script for the iOS target.
# Uploads the signed .ipa to App Store Connect; it then shows up in TestFlight after Apple's processing.
#
# Set these environment variables on the iOS build target (Advanced settings > Environment variables):
#   ASC_KEY_ID     App Store Connect API key id        (Users and Access > Integrations > App Store Connect API)
#   ASC_ISSUER_ID  issuer id shown on the same page
#   ASC_KEY_P8     the .p8 key file contents, base64-encoded (macOS: base64 -i AuthKey_XXXX.p8 | pbcopy)
# Without them the script does nothing, so the build still succeeds and you can upload the .ipa by hand.
set -e

if [ -z "$ASC_KEY_ID" ] || [ -z "$ASC_ISSUER_ID" ] || [ -z "$ASC_KEY_P8" ]; then
  echo "[WordZ] App Store Connect API key not set - skipping upload."
  exit 0
fi

IPA="$UNITY_PLAYER_PATH"
if [ ! -f "$IPA" ]; then
  echo "[WordZ] No .ipa found at '$IPA' - skipping upload."
  exit 0
fi

mkdir -p ~/private_keys
echo "$ASC_KEY_P8" | base64 --decode > ~/private_keys/AuthKey_${ASC_KEY_ID}.p8

echo "[WordZ] Uploading $IPA to App Store Connect..."
xcrun altool --upload-app --type ios --file "$IPA" --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER_ID"
echo "[WordZ] Upload finished."
