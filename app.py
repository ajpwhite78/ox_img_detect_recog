from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration 

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

webrtc_ctx = webrtc_streamer(
    key="WYH",
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": True},
)
