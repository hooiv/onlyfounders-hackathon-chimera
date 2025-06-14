"""
Quick test script to verify Project Chimera setup
"""

import sys
import os

def test_project_structure():
    """Test that all required files and directories exist"""
    required_paths = [
        'app/__init__.py',
        'app/main.py',
        'app/model.py',
        'app/ml/train.py',
        'docs/architecture_diagram.md',
        'requirements.txt',
        'README.md'
    ]
    
    missing_paths = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        print("❌ Missing files/directories:")
        for path in missing_paths:
            print(f"  - {path}")
        return False
    else:
        print("✅ All required files and directories exist")
        return True

def test_imports():
    """Test that key modules can be imported"""
    try:
        sys.path.append('app')
        import main
        import model
        print("✅ Core modules can be imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Project Chimera setup...\n")
    
    structure_ok = test_project_structure()
    imports_ok = test_imports()
    
    if structure_ok and imports_ok:
        print("\n🎉 Project Chimera setup is complete and ready!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Train the model: python app/ml/train.py")
        print("3. Start the server: python app/main.py")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")

if __name__ == "__main__":
    main()
