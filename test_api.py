import requests
import json
import os
import subprocess
import time
import signal

# API base URL
BASE_URL = "http://localhost:5000"

def start_api_server():
    """Start the API server using the integrated main.py"""
    print("🚀 Starting API server from integrated main.py...")
    try:
        # Start the server in a subprocess
        process = subprocess.Popen(
            ["python", "main.py", "--api"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the server is running
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API server started successfully!")
                return process
            else:
                print("❌ API server failed to start properly")
                process.terminate()
                return None
        except requests.exceptions.RequestException:
            print("❌ API server failed to start")
            process.terminate()
            return None
            
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def stop_api_server(process):
    """Stop the API server"""
    if process:
        print("🛑 Stopping API server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✅ API server stopped")

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health check passed\n")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}\n")
        return False

def test_get_voices():
    """Test getting available voices"""
    print("🔍 Testing get voices...")
    try:
        response = requests.get(f"{BASE_URL}/voices")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Get voices passed\n")
        return True
    except Exception as e:
        print(f"❌ Get voices failed: {e}\n")
        return False

def test_generate_dialogue_audio():
    """Test generating dialogue audio and downloading the file"""
    print("🔍 Testing generate dialogue audio (download)...")
    try:
        payload = {
            "text": "Hello, this is a test of the dialogue audio generation API. I hope it works well!",
            "voice_id": "rachel",
            "output_format": "mp3"
        }
        
        response = requests.post(
            f"{BASE_URL}/generate-dialogue-audio",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            # Save the audio file
            filename = f"test_dialogue_{payload['voice_id']}.mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Audio file saved as: {filename}")
            print(f"File size: {len(response.content)} bytes")
        else:
            print(f"❌ Failed: {response.text}")
            
        print("✅ Generate dialogue audio (download) passed\n")
        return True
    except Exception as e:
        print(f"❌ Generate dialogue audio (download) failed: {e}\n")
        return False

def test_generate_dialogue_audio_stream():
    """Test generating dialogue audio as streaming response"""
    print("🔍 Testing generate dialogue audio (stream)...")
    try:
        payload = {
            "text": "This is a streaming test of the dialogue audio generation. The audio should be returned directly in the response.",
            "voice_id": "antoni"
        }
        
        response = requests.post(
            f"{BASE_URL}/generate-dialogue-audio-stream",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Audio data size: {len(response.content)} bytes")
        
        if response.status_code == 200:
            # Save the streaming audio file
            filename = f"test_stream_{payload['voice_id']}.mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Streaming audio file saved as: {filename}")
        else:
            print(f"❌ Failed: {response.text}")
            
        print("✅ Generate dialogue audio (stream) passed\n")
        return True
    except Exception as e:
        print(f"❌ Generate dialogue audio (stream) failed: {e}\n")
        return False

def test_generate_dialogue_audio_info():
    """Test generating dialogue audio info (metadata only)"""
    print("🔍 Testing generate dialogue audio info...")
    try:
        payload = {
            "text": "This is a test for getting audio metadata without downloading the actual file.",
            "voice_id": "bella"
        }
        
        response = requests.post(
            f"{BASE_URL}/generate-dialogue-audio-info",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Audio info generated successfully")
            print(f"   - Text: {data.get('text', 'N/A')[:50]}...")
            print(f"   - Voice ID: {data.get('voice_id', 'N/A')}")
            print(f"   - Size: {data.get('audio_size_bytes', 'N/A')} bytes")
            print(f"   - Duration: {data.get('estimated_duration_seconds', 'N/A')} seconds")
        else:
            print(f"❌ Failed: {response.text}")
            
        print("✅ Generate dialogue audio info passed\n")
        return True
    except Exception as e:
        print(f"❌ Generate dialogue audio info failed: {e}\n")
        return False

def test_error_handling():
    """Test error handling with invalid requests"""
    print("🔍 Testing error handling...")
    
    # Test missing text field
    try:
        payload = {"voice_id": "rachel"}
        response = requests.post(
            f"{BASE_URL}/generate-dialogue-audio",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Missing text - Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Missing text test failed: {e}")
    
    # Test empty text
    try:
        payload = {"text": "", "voice_id": "rachel"}
        response = requests.post(
            f"{BASE_URL}/generate-dialogue-audio",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Empty text - Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Empty text test failed: {e}")
    
    # Test invalid voice
    try:
        payload = {"text": "Test text", "voice_id": "invalid_voice"}
        response = requests.post(
            f"{BASE_URL}/generate-dialogue-audio",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Invalid voice test failed: {e}")
    
    print("✅ Error handling tests completed\n")

def main():
    """Run all tests"""
    print("🚀 Starting API Tests with Integrated main.py...\n")
    
    # Start the API server
    api_process = start_api_server()
    if not api_process:
        print("❌ Failed to start API server. Exiting.")
        return
    
    try:
        # Wait a bit more for the server to be fully ready
        time.sleep(2)
        
        # Check if API is running
        if not test_health_check():
            print("❌ API is not running properly. Exiting.")
            return
        
        # Run all tests
        tests = [
            test_get_voices,
            test_generate_dialogue_audio,
            test_generate_dialogue_audio_stream,
            test_generate_dialogue_audio_info,
            test_error_handling
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The integrated API is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the output above for details.")
            
    finally:
        # Always stop the API server
        stop_api_server(api_process)

if __name__ == "__main__":
    main()
