#!/usr/bin/env python3
"""
Simple OpenBB Test - Check installation and available providers
"""

def test_openbb():
    try:
        import openbb
        print("✅ OpenBB imported successfully")
        print(f"Version: {openbb.__version__}")
        
        # Test the core API
        try:
            from openbb import obb
            print("✅ obb API available")
            
            # Test if options chains is available
            try:
                hasattr(obb, 'derivatives')
                print("✅ derivatives module available")
                
                # Test specific function
                try:
                    hasattr(obb.derivatives, 'options')
                    print("✅ options module available")
                    
                    # Test chains function
                    try:
                        hasattr(obb.derivatives.options, 'chains')
                        print("✅ chains function available")
                        return True
                    except Exception as e:
                        print(f"❌ chains function error: {e}")
                        return False
                        
                except Exception as e:
                    print(f"❌ options module error: {e}")
                    return False
                    
            except Exception as e:
                print(f"❌ derivatives module error: {e}")
                return False
                
        except ImportError as e:
            print(f"❌ OpenBB import failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ OpenBB test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_openbb()
    if success:
        print("\n🎉 OpenBB is ready for hybrid options fetcher!")
    else:
        print("\n❌ OpenBB installation needs troubleshooting")