@echo off
REM ============================================================================
REM  Word Z - make the Apple Distribution certificate (.p12) on Windows, no Mac.
REM  Needs OpenSSL. Git for Windows includes it: "C:\Program Files\Git\usr\bin\openssl.exe"
REM
REM  STEP 1:  make_ios_certificate.bat csr  you@email.com "Your Name"
REM           -> upload certs\wordz_dist.csr at developer.apple.com > Certificates > + > Apple Distribution
REM           -> download the certificate and save it as certs\distribution.cer
REM  STEP 2:  make_ios_certificate.bat p12  YourP12Password
REM           -> certs\wordz_dist.p12  (upload it + the password to Unity Build Automation)
REM  Keep the certs folder private and backed up. It is in .gitignore.
REM ============================================================================
setlocal
set OPENSSL=openssl
where openssl >nul 2>nul || set OPENSSL="C:\Program Files\Git\usr\bin\openssl.exe"
cd /d "%~dp0"
if not exist certs mkdir certs

if /i "%1"=="csr" (
  if "%~3"=="" ( echo Usage: make_ios_certificate.bat csr you@email.com "Your Name" & exit /b 1 )
  %OPENSSL% genrsa -out certs\wordz_dist.key 2048 || exit /b 1
  %OPENSSL% req -new -key certs\wordz_dist.key -out certs\wordz_dist.csr -subj "/emailAddress=%~2/CN=%~3/C=US" || exit /b 1
  echo.
  echo Done. Upload certs\wordz_dist.csr to Apple, then save the downloaded file as certs\distribution.cer
  exit /b 0
)

if /i "%1"=="p12" (
  if "%~2"=="" ( echo Usage: make_ios_certificate.bat p12 YourP12Password & exit /b 1 )
  if not exist certs\distribution.cer ( echo Put the certificate from Apple at certs\distribution.cer first & exit /b 1 )
  %OPENSSL% x509 -in certs\distribution.cer -inform DER -out certs\distribution.pem -outform PEM || exit /b 1
  REM SHA1/3DES packaging so the Mac build machines' keychain can import it
  %OPENSSL% pkcs12 -export -inkey certs\wordz_dist.key -in certs\distribution.pem -out certs\wordz_dist.p12 -passout pass:%~2 -certpbe PBE-SHA1-3DES -keypbe PBE-SHA1-3DES -macalg sha1 || exit /b 1
  echo.
  echo Done: certs\wordz_dist.p12  - upload it with the password to Build Automation.
  exit /b 0
)

echo Usage:
echo   make_ios_certificate.bat csr you@email.com "Your Name"
echo   make_ios_certificate.bat p12 YourP12Password
exit /b 1
