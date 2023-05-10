from streamlit_webrtc import webrtc_streamer, RTCConfiguration

webrtc_streamer(key="sample", rtc_configuration={"iceServers": [{"urls": ["stun:stun-eu.3cx.com:3478"]}]})
