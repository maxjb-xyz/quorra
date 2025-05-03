import pveagle
from pvrecorder import PvRecorder
from config import DEFAULT_DEVICE_INDEX
import os

def enroll_speaker(access_key, name, profile_folder="eagle_profiles"):
    try:
        eagle_profiler = pveagle.create_profiler(access_key=access_key)
    except pveagle.EagleError as e:
        print(f"Error creating profiler: {e}")
        return None

    enroll_recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle_profiler.min_enroll_samples)

    enroll_recorder.start()

    enroll_percentage = 0.0
    while enroll_percentage < 100.0:
        audio_frame = enroll_recorder.read()
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
        print(f"Enrollment progress: {enroll_percentage:.2f}%")

    enroll_recorder.stop()

    speaker_profile = eagle_profiler.export()

    class EagleProfile(object):

        def to_bytes(self) -> bytes:
            return self._to_bytes(self.handle, self.size)

    # Construct file path
    file_path = os.path.join(profile_folder, f"{name}.bin")

    # Save profile bytes to a file
    with open(file_path, 'wb') as f:
        f.write(speaker_profile.to_bytes())

    enroll_recorder.delete()
    eagle_profiler.delete()

    return speaker_profile
