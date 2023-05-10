from streamlit_webrtc import webrtc_streamer, RTCConfiguration

webrtc_streamer(key="sample", rtc_configuration=RTCConfiguration(
                            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}))
