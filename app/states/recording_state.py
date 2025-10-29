import reflex as rx
import asyncio
import logging
import base64
import uuid
from app.states.dashboard_state import DashboardState


class RecordingState(rx.State):
    is_recording: bool = False
    camera_ready: bool = False
    show_confirmation: bool = False
    start_recording_script = """
    if (window.localStream) {
        window.mediaRecorder = new MediaRecorder(window.localStream);
        window.recordedChunks = [];
        window.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                window.recordedChunks.push(event.data);
            }
        };
        window.mediaRecorder.onstop = () => {
            const blob = new Blob(window.recordedChunks, { type: 'video/webm' });
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => {
                const base64data = reader.result;
                const event = {
                    name: 'recording_state.RecordingState.handle_recording_data',
                    payload: { data: base64data }
                };
                _sendEvent(event);
            }
        };
        window.mediaRecorder.start();
        _sendEvent(JSON.parse('{"name": "recording_state.RecordingState.set_is_recording", "payload": {"value": true}}'));
    }
    """
    stop_recording_script = """
    if (window.mediaRecorder && window.mediaRecorder.state === 'recording') {
        window.mediaRecorder.stop();
        _sendEvent(JSON.parse('{"name": "recording_state.RecordingState.set_is_recording", "payload": {"value": false}}'));
        _sendEvent(JSON.parse('{"name": "recording_state.RecordingState.set_show_confirmation", "payload": {"value": true}}'));
    }
    """

    @rx.event
    def initialize_camera(self):
        return rx.call_script("""(async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: true });
        const videoElement = document.getElementById('video-player');
        if (videoElement) {
            videoElement.srcObject = stream;
            window.localStream = stream;
            const event = {
                name: 'recording_state.set_camera_ready',
                payload: {value: true}
            };
            _sendEvent(event);
        }
    } catch (err) {
        console.error('Error accessing camera:', err);
        const event = {
            name: 'recording_state.set_camera_ready',
            payload: {value: false}
        };
        _sendEvent(event);
    }
})()""")

    @rx.event
    def handle_recording_data(self, data: str):
        return rx.call_script(f"_setLocalStorage('recorded_video_data', '{data}')")

    @rx.event
    async def upload_recorded_video(self):
        self.show_confirmation = False
        yield rx.toast.info("Preparing to upload...")
        recorded_video_data_b64 = await self.get_local_storage("recorded_video_data")
        if not recorded_video_data_b64:
            yield rx.toast.error("No recording data found.")
            return
        try:
            header, encoded = recorded_video_data_b64.split(",", 1)
            video_data = base64.b64decode(encoded)
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            filename = f"recording_{uuid.uuid4()}.webm"
            file_path = upload_dir / filename
            with file_path.open("wb") as f:
                f.write(video_data)
            dashboard_state = await self.get_state(DashboardState)
            dashboard_state.uploaded_files.append(filename)
            yield rx.toast.success(f"'{filename}' uploaded successfully!")
            yield rx.remove_local_storage("recorded_video_data")
            yield rx.redirect("/library")
        except Exception as e:
            logging.exception(f"Failed to upload recorded video: {e}")
            yield rx.toast.error("Upload failed.")

    @rx.event
    def reset_recording(self):
        self.show_confirmation = False
        return rx.remove_local_storage("recorded_video_data")