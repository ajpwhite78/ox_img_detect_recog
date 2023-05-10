import cv2
import imutils
import numpy as np
from PIL import Image, ImageColor
from io import BytesIO
import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration

# Hide the footer and header
hide_st_style = """
                <style>
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to locate the face in the image and draw a rectangle around it
def locate_face(image):
    # To convert PIL Image to numpy array:
    image = np.array(image)
    # Convert the image from BGR to RGB color space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Resize the image to a width of 600 pixels
    image = imutils.resize(image, width=600)
    # Detect faces in the image using the face cascade classifier
    rects = face_cascade.detectMultiScale(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5,
                                          minSize=(30, 30))
    # Draw a rectangle around each face in the image
    for (x, y, w, h) in rects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (252, 188, 36, 0), 2)

    # Draw a large rectangle around the entire image
    cv2.rectangle(image, (0, 0), (image.shape[1], image.shape[0]), (0, 33, 71, 0), 30)

    # Return the image with the face and rectangle drawn on it
    return image

# Initialize variables for the video stream and camera
cap = None
run_camera = False

# Create a streamlit image widget to display the camera feed
col1, col2, col3 = st.columns([0.2, 5, 0.2])
with col2:
    text = '<p style="margin-bottom: 20px; margin-top: -50px; text-align: center;"><span style="font-family:sans-serif; color:#FAFAFA; font-size: 36px;">Image Object Detection & Identification</span></p>'
    st.markdown(text, unsafe_allow_html=True)
    frame_window = st.image([], use_column_width=True)

# Initialize the camera object and get its width and height
width = 600
height = 400
webrtc_streamer(key="key", rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
# Create a blank image with the same dimensions as the camera feed
blank_image = np.zeros((height, width, 3), dtype=np.uint8)
resized_blank_image = cv2.resize(blank_image, (600, int((height/width)*600)))

# Draw rectangle
cv2.rectangle(resized_blank_image, (0, 0), (resized_blank_image.shape[1], resized_blank_image.shape[0]), (0, 33, 71, 0), 30)

# Add text to the blank image to prompt the user to start the camera
text1 = "Start Camera to Run"
font = cv2.FONT_HERSHEY_DUPLEX
font_scale =1
thickness = 2
text_color = (250, 250, 250)
text_size1, _ = cv2.getTextSize(text1, font, font_scale, thickness)
text_x1 = int((resized_blank_image.shape[1] - text_size1[0]) / 2)
text_y1 = int((resized_blank_image.shape[0]) / 2)
cv2.putText(resized_blank_image, text1, (text_x1, text_y1), font, font_scale, text_color, thickness)
frame_window.image(resized_blank_image, use_column_width=True)

# Define the size of the columns in the Streamlit app
col1, col2, col3 = st.columns([0.2, 5, 0.2])
# Use the middle column to display the start/stop camera button and the camera's video feed
with col2:
    # Add custom styling for the start/stop button#6076CE
    st.markdown(
        """<style>div.stButton > button:first-child {background-color:#002147; color: #FAFAFA; border-color: #002147; border-width: 3px; font-size: 14px; width:100%; height:3em} div.stButton {margin-top: -20px;margin-bottom: -20px;} div.stButton > button:hover {background-color: rgba(60, 63, 65, 0.2); color: #FAFAFA; border-color: #002147}</style>""",
        unsafe_allow_html=True)
    # Add an empty text and the start/stop button to the Streamlit app
    if "start_stop_button_place" not in st.session_state:
        st.session_state.start_stop_button_place = st.empty()

    # If the start/stop button has not been clicked, initialize its state to False
    if "start_stop_button_state" not in st.session_state:
        st.session_state.start_stop_button_state = False
# Define column layout
col1, col2, col3, col4 = st.columns([0.2, 1, 4, 0.2])
# In the second column, create a tooltip that explains facial recognition
with col2:
    # Add a markdown block that defines the tooltip's style using HTML and CSS
    st.markdown(
        """
        <style>
        /* Tooltip container */
        .tooltip {
            position: relative;
            display: inline-block;
    #        border-bottom: 1px dotted black;
        }

        /* Tooltip text */
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 640px;
            background-color: #222222;
            color: #FAFAFA;
            text-align: justify;
            font-family:sans-serif;
            font-size: 18px;
            border-radius: 6px;
            padding: 10px 15px;
            white-space: normal;
            padding: 10px 10px 10px 10px;
            border: 2px solid #FCBC24;

            /* Position the tooltip text */
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -620px;

            /* Fade in tooltip */
            opacity: 0;
            transition: opacity 0.5s;
        }

        /* Tooltip arrow */
        .tooltip .tooltiptext::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 97.25%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #FCBC24 transparent transparent transparent;
        }
        /* Show the tooltip text when you mouse over the tooltip container */
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        /* Change icon color on hover */
        .tooltip:hover i {
            color: #FCBC24;
        }   
        /* Set initial icon color */
        .tooltip i {
            color: #FAFAFA;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
with col3:
    text = '<p style="margin-top: -20px; margin-bottom: 10px; text-align: justify;"><span style="font-family:sans-serif; color:#FAFAFA; font-size: 18px;">Click on the info icon to learn more.</span></p>'
    st.markdown(text, unsafe_allow_html=True)
# Add the Font Awesome stylesheet to enable use of Font Awesome icons
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">',
        unsafe_allow_html=True)
# Create an icon with a tooltip that explains facial recognition
with col3:
    st.markdown(
        """
        <div class="tooltip">
        <i class="fas fa-info-circle fa-2x""></i>
        <span class="tooltiptext">Facial recognition software is a technology that can detect and recognize human faces in images or videos. In this playground tool, you can train a facial recognition model to recognize your face by capturing an image of yourself. The software then generates a unique code or "encoding" that represents your facial features. This encoding is saved and used by the model to recognize your face in real-time. By training the model on your image, it can learn to differentiate your face from others and identify you accurately.<br><br>Note: This playground tool is for educational purposes only. No images or data are being recorded or stored.</span>
        </div>
        """,
        unsafe_allow_html=True
    )


col1, col2, col3 = st.columns([0.2, 5, 0.2])
with col2:
    text = '<p style="margin-top: 20px; margin-bottom: 0px;"><span style="font-family:sans-serif; color:#FAFAFA; font-size: 18px;">This playground tool demonstrates the capabilities of AI and ML models to detect, locate and identify faces within images in real-time. This technology can be applied to various business applications to automate multiple tasks, improve customer experiences, reduce costs and increase efficiency.<br><br>oxbr</span><span style="font-family:sans-serif; color:#FCBC24; font-size: 18px">AI</span><span style="font-family:sans-serif; color:#FAFAFA; font-size: 18px;">n &apos;s expertise and experience can help your business maximize the benefits of image object detction and identification technology and stay ahead of the competition. So if you want to unlock the full potential of AI and stay ahead of the curve, partner with oxbr</span><span style="font-family:sans-serif; color:#FCBC24; font-size: 18px">AI</span><span style="font-family:sans-serif; color:#FAFAFA; font-size: 18px;">n today.<br><br>Note: This playground tool is for educational purposes only. No images or data are being recorded or stored.</span></p>'
    st.markdown(text, unsafe_allow_html=True)

# If the start/stop button is currently in the "start" state
if st.session_state.start_stop_button_state:
    # If the video stream has not yet been initialized, initialize it
    if not "cap" in st.session_state:
        st.markdown("""<style>button.css-r65s9h.ejtjsn20 {display: none;}</style>""", unsafe_allow_html=True)
        st.session_state.cap = frame_window.camera_input(label="", label_visibility="collapsed")

    # Remove the start/stop button from the Streamlit app and replace it with a "stop" button
    st.session_state.start_stop_button_place.empty()
    stop_button = st.session_state.start_stop_button_place.button("Stop Camera")

    # Continuously read frames from the video stream and display them in the Streamlit app
    while st.session_state.start_stop_button_state:
        st.markdown("""<style>button.css-r65s9h.ejtjsn20 {display: none;}</style>""", unsafe_allow_html=True)
        st.session_state.cap = frame_window.camera_input(label="", label_visibility="collapsed")
        # Read a frame from the video stream as a PIL Image:
        frame = Image.open(st.camera_input(label="", label_visibility="collapsed", key="cam1"))
        if not frame is None:
            break
        # Process the frame to locate the face in the video stream
        frame = locate_face(frame)
        # Display the processed frame in the Streamlit app
        frame_window.image(frame, use_column_width=True)

        # If the "stop" button is clicked, set the start/stop button state to False, release the video stream object, and exit the loop
        if stop_button:
            st.session_state.cap.release()
            del st.session_state.cap
            stop_button = False
            st.session_state.start_stop_button_state = False
            frame_window.empty()
            frame_window.image(resized_blank_image, use_column_width=True)
            st.session_state.start_stop_button_place.empty()
            start_button = st.session_state.start_stop_button_place.button("Start Camera")
            cv2.destroyAllWindows()
            break

    # If the "stop" button is clicked, set the start/stop button state to False
    if stop_button:
        st.session_state.start_stop_button_state = False
    # If the start/stop button is currently in the "stop" state
else:
    # Remove the start/stop button from the Streamlit app and replace it with a "start" button
    st.session_state.start_stop_button_place.empty()
    start_button = st.session_state.start_stop_button_place.button("Start Camera")

    # If the "start" button is clicked, set the start/stop button state to True
    if start_button:
        st.session_state.start_stop_button_state = True
        start_button = False
        frame_window.empty()
        # If the start/stop button is currently in the "start" state
        if st.session_state.start_stop_button_state:
            # If the video stream has not yet been initialized, initialize it
            if not "cap" in st.session_state:
                st.markdown("""<style>button.css-r65s9h.ejtjsn20 {display: none;}</style>""", unsafe_allow_html=True)
                st.session_state.cap = frame_window.camera_input(label="", label_visibility="collapsed")
            st.experimental_rerun()




