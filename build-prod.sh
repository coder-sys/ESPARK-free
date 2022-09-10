#!/bin/bash
echo "Preparing to build."
rm -rf ./web-build > /dev/null 2>&l
echo "Installing dependencies."
npm install --force > /dev/null 2>&l
echo "Building production build into 'web-build' with expo."
npm run build-production > /dev/null 2>&l
echo "Installing vercel."
npm install vercel --force > /dev/null 2>&l
echo "Running vercel."
cd web-build
vercel --prod
echo "Operation successful."
cd ..
