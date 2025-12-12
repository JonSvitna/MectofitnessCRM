#!/usr/bin/env python3
"""
Verification script for static homepage deployment.
Checks that all required files exist and are properly configured.
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists and report status."""
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"✅ {description}")
        print(f"   Path: {path}")
        print(f"   Size: {size:,} bytes")
        return True
    else:
        print(f"❌ {description} NOT FOUND")
        print(f"   Expected: {path}")
        return False

def check_directory(path, description):
    """Check if a directory exists and report contents."""
    if os.path.exists(path):
        file_count = sum([len(files) for r, d, files in os.walk(path)])
        print(f"✅ {description}")
        print(f"   Path: {path}")
        print(f"   Files: {file_count}")
        return True
    else:
        print(f"❌ {description} NOT FOUND")
        print(f"   Expected: {path}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Homepage Deployment Verification")
    print("=" * 60)
    print()
    
    checks_passed = 0
    checks_total = 0
    
    # Check Next.js source files
    print("1. Next.js Source Files")
    print("-" * 60)
    checks_total += 1
    if check_file('src/app/page.tsx', 'Homepage component'):
        checks_passed += 1
    print()
    
    checks_total += 1
    if check_file('src/lib/cn.ts', 'Tailwind utility'):
        checks_passed += 1
    print()
    
    # Check build configuration
    print("2. Build Configuration")
    print("-" * 60)
    checks_total += 1
    if check_file('next.config.mjs', 'Next.js config'):
        checks_passed += 1
        # Verify export mode with robust parsing
        try:
            with open('next.config.mjs') as f:
                config = f.read()
                # Check for various possible formats
                if any(pattern in config for pattern in [
                    "output: 'export'",
                    'output: "export"',
                    "output:'export'",
                    'output:"export"'
                ]):
                    print("   ✓ Static export enabled")
                else:
                    print("   ⚠ Static export may not be enabled")
        except Exception as e:
            print(f"   ⚠ Could not verify config: {e}")
    print()
    
    checks_total += 1
    if check_file('build.sh', 'Build script'):
        checks_passed += 1
    print()
    
    # Check static build output
    print("3. Static Build Output")
    print("-" * 60)
    checks_total += 1
    if check_file('app/static/homepage/index.html', 'Homepage HTML'):
        checks_passed += 1
    print()
    
    checks_total += 1
    if check_directory('app/static/homepage/_next', 'Next.js assets'):
        checks_passed += 1
    print()
    
    # Check Flask routing
    print("4. Flask Configuration")
    print("-" * 60)
    checks_total += 1
    if check_file('app/routes/main.py', 'Flask routes'):
        checks_passed += 1
        # Verify route configuration with error handling
        try:
            with open('app/routes/main.py') as f:
                routes = f.read()
                if 'send_from_directory' in routes:
                    print("   ✓ Static file serving configured")
                if "homepage/index.html" in routes:
                    print("   ✓ Homepage route configured")
                if "_next" in routes:
                    print("   ✓ Next.js assets route configured")
        except Exception as e:
            print(f"   ⚠ Could not verify routes: {e}")
    print()
    
    # Check documentation
    print("5. Documentation")
    print("-" * 60)
    checks_total += 1
    if check_file('STATIC_HOMEPAGE_GUIDE.md', 'Deployment guide'):
        checks_passed += 1
    print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Checks passed: {checks_passed}/{checks_total}")
    
    if checks_passed == checks_total:
        print()
        print("✅ All checks passed! Homepage is ready for deployment.")
        print()
        print("Next steps:")
        print("1. Commit and push changes to GitHub")
        print("2. Railway will automatically build and deploy")
        print("3. Visit your Railway domain to see the new homepage")
        return 0
    else:
        print()
        print("⚠️  Some checks failed. Review the issues above.")
        print()
        print("To fix:")
        print("1. Run ./build-homepage.sh to generate static files")
        print("2. Verify all source files are committed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
