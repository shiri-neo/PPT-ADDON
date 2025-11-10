#!/usr/bin/env python3
"""
Test script to verify backend setup is correct
"""

import sys

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('pydantic', 'Pydantic'),
        ('jwt', 'PyJWT'),
        ('passlib', 'Passlib'),
    ]

    failed = []
    for package, name in packages:
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError as e:
            print(f"  ✗ {name}: {e}")
            failed.append(name)

    if failed:
        print(f"\n❌ Failed to import: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("\n✓ All imports successful!")
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    try:
        from app.core.config import get_settings
        settings = get_settings()
        print(f"  ✓ Config loaded")
        print(f"    Database: {settings.database_url}")
        print(f"    CORS origins: {settings.cors_allowed_origins}")
        return True
    except Exception as e:
        print(f"  ✗ Config failed: {e}")
        return False

def test_database():
    """Test database connection and table creation"""
    print("\nTesting database...")
    try:
        from app.core.database import Base, engine
        from app.models import user, organization, document, presentation

        # Create tables
        Base.metadata.create_all(bind=engine)
        print(f"  ✓ Database tables created")

        # Test connection
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"  ✓ Database connection successful")

        return True
    except Exception as e:
        print(f"  ✗ Database failed: {e}")
        return False

def test_auth():
    """Test authentication functions"""
    print("\nTesting authentication...")
    try:
        from app.core.security import get_password_hash, verify_password, create_access_token

        # Test password hashing
        password = "test123"
        hashed = get_password_hash(password)
        if verify_password(password, hashed):
            print(f"  ✓ Password hashing works")
        else:
            print(f"  ✗ Password verification failed")
            return False

        # Test JWT creation
        token = create_access_token({"sub": "1"})
        if token:
            print(f"  ✓ JWT token creation works")
        else:
            print(f"  ✗ JWT token creation failed")
            return False

        return True
    except Exception as e:
        print(f"  ✗ Auth failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Backend Setup Test")
    print("=" * 50)

    tests = [
        test_imports,
        test_config,
        test_database,
        test_auth,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    if passed == len(tests):
        print(f"✓ All {passed}/{len(tests)} tests passed!")
        print("\nBackend is ready to use!")
        sys.exit(0)
    else:
        print(f"✗ {passed}/{len(tests)} tests passed")
        print("\nPlease fix the errors above before starting the backend")
        sys.exit(1)
