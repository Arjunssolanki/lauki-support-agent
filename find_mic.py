import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    print("\n=== AVAILABLE AUDIO INPUT DEVICES ===")
    
    # Scan through every audio interface reported by the OS
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        # Check if the device supports audio input channels
        if dev_info.get('maxInputChannels', 0) > 0:
            print(f"Index {i}: {dev_info.get('name')} (Channels: {dev_info.get('maxInputChannels')})")
            
    p.terminate()

if __name__ == "__main__":
    list_audio_devices()
