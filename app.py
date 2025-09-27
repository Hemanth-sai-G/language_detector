'''import streamlit as st
import os
from language_detector import LanguageDetector
from config import SUPPORTED_LANGUAGES

# Initialize the language detector
@st.cache_resource
def load_detector():
    """Load the language detector (cached to avoid reloading)"""
    return LanguageDetector()

def main():
    # Page configuration
    st.set_page_config(
        page_title="Language Detection App",
        page_icon="🌍",
        layout="centered"
    )
    
    # App title and description
    st.title("🌍 Language Detection Application")
    st.markdown("**Detect languages from text input or file uploads using AI**")
    st.markdown("---")
    
    # Load the detector
    with st.spinner("Loading language detection models..."):
        detector = load_detector()
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📝 Text Input", "📁 File Upload"])
    
    # Tab 1: Manual text input
    with tab1:
        st.subheader("Type or paste your text")
        
        # Text input area
        user_text = st.text_area(
            "Enter text in any language:",
            height=150,
            placeholder="Type something here... For example: 'Hello, how are you?' or 'Bonjour, comment allez-vous?'"
        )
        
        # Detect button for text
        if st.button("🔍 Detect Language", key="text_detect"):
            if user_text.strip():
                with st.spinner("Analyzing text..."):
                    result = detector.detect_language(user_text)
                    display_results(result, user_text)
            else:
                st.warning("⚠️ Please enter some text to analyze.")
    
    # Tab 2: File upload
    with tab2:
        st.subheader("Upload a text file")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a text file (.txt)",
            type=['txt'],
            help="Upload a text file to detect its language"
        )
        
        if uploaded_file is not None:
            # Read file content
            try:
                # Read the file content
                file_content = uploaded_file.read().decode('utf-8')
                
                # Show preview of file content
                st.write("**File Preview:**")
                preview = file_content[:500] + ("..." if len(file_content) > 500 else "")
                st.text_area("Content preview:", preview, height=100, disabled=True)
                
                # Detect button for file
                if st.button("🔍 Detect Language from File", key="file_detect"):
                    with st.spinner("Analyzing file content..."):
                        result = detector.detect_language(file_content)
                        display_results(result, file_content, is_file=True, filename=uploaded_file.name)
                        
            except UnicodeDecodeError:
                st.error("❌ Error reading file. Please ensure the file is in UTF-8 encoding.")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    # Sidebar with information
    create_sidebar()

def display_results(result, text, is_file=False, filename=None):
    """Display the language detection results"""
    
    if result:
        st.success("✅ Language detected successfully!")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="🌍 Detected Language",
                value=result['language_name']
            )
        
        with col2:
            confidence_pct = round(result['confidence'] * 100, 1)
            st.metric(
                label="🎯 Confidence",
                value=f"{confidence_pct}%"
            )
        
        # Additional information
        st.write("**Details:**")
        info_text = f"- **Language Code:** {result['language_code']}"
        if is_file and filename:
            info_text += f"\n- **File:** {filename}"
        info_text += f"\n- **Text Length:** {len(text)} characters"
        st.markdown(info_text)
        
        # Show confidence interpretation
        if confidence_pct >= 90:
            st.info("🟢 Very high confidence - the detection is very reliable")
        elif confidence_pct >= 70:
            st.info("🟡 Good confidence - the detection is quite reliable")
        else:
            st.info("🟠 Moderate confidence - consider providing more text for better accuracy")
    
    else:
        st.error("❌ Could not detect the language. Try with different or longer text.")

def create_sidebar():
    """Create sidebar with app information"""
    
    st.sidebar.title("ℹ️ About")
    st.sidebar.markdown("""
    This app uses advanced AI models to detect languages from text.
    
    **Features:**
    - 🎯 High accuracy detection
    - 🌐 50+ languages supported
    - 📁 File upload capability
    - 🚀 Works offline
    
    **Supported Languages:**
    """)
    
    # Show some popular supported languages
    popular_langs = [
        "English", "Spanish", "French", "German", "Italian",
        "Portuguese", "Russian", "Chinese", "Japanese", "Korean",
        "Arabic", "Hindi", "Dutch", "Swedish", "Polish"
    ]
    
    for lang in popular_langs:
        st.sidebar.write(f"• {lang}")
    
    st.sidebar.write("• And 35+ more...")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Tips for better results:**")
    st.sidebar.markdown("""
    - Use at least 10-20 characters
    - Avoid mixing multiple languages
    - Ensure text is properly encoded
    """)

if __name__ == "__main__":
    main()
'''

import streamlit as st
import os
from language_detector import LanguageDetector
from config import SUPPORTED_LANGUAGES

# Initialize the language detector with a predefined dataset path
@st.cache_resource
def load_detector():
    """Load the language detector (cached to avoid reloading)"""
    dataset_path = "language.csv"  # Use the relative path to your dataset
    return LanguageDetector(dataset_path)

def main():
    # Page configuration
    st.set_page_config(
        page_title="Language Detection App",
        page_icon="🌍",
        layout="centered"
    )
    
    # App title and description
    st.title("🌍 Language Detection Application")
    st.markdown("**Detect languages from text input or file uploads using AI**")
    st.markdown("---")
    
    # Load the detector
    with st.spinner("Loading language detection models..."):
        detector = load_detector()
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📝 Text Input", "📁 File Upload"])
    
    # Tab 1: Manual text input
    with tab1:
        st.subheader("Type or paste your text")
        
        # Text input area
        user_text = st.text_area(
            "Enter text in any language:",
            height=150,
            placeholder="Type something here... For example: 'Hello, how are you?' or 'Bonjour, comment allez-vous?'"
        )
        
        # Detect button for text
        if st.button("🔍 Detect Language", key="text_detect"):
            if user_text.strip():
                with st.spinner("Analyzing text..."):
                    result = detector.predict_language(user_text)
                    st.success(f"✅ Detected Language: {result}")
            else:
                st.warning("⚠️ Please enter some text to analyze.")
    
    # Tab 2: File upload
    with tab2:
        st.subheader("Upload a text file")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a text file (.txt)",
            type=['txt'],
            help="Upload a text file to detect its language"
        )
        
        if uploaded_file is not None:
            # Read file content
            try:
                # Read the file content
                file_content = uploaded_file.read().decode('utf-8')
                
                # Show preview of file content
                st.write("**File Preview:**")
                preview = file_content[:500] + ("..." if len(file_content) > 500 else "")
                st.text_area("Content preview:", preview, height=100, disabled=True)
                
                # Detect button for file
                if st.button("🔍 Detect Language from File", key="file_detect"):
                    with st.spinner("Analyzing file content..."):
                        result = detector.predict_language(file_content)
                        st.success(f"✅ Detected Language: {result}")
                        
            except UnicodeDecodeError:
                st.error("❌ Error reading file. Please ensure the file is in UTF-8 encoding.")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    # Sidebar with information
    create_sidebar()

def create_sidebar():
    """Create sidebar with app information"""
    
    st.sidebar.title("ℹ️ About")
    st.sidebar.markdown("""
    This app uses advanced AI models to detect languages from text.
    
    **Features:**
    - 🎯 High accuracy detection
    - 🌐 50+ languages supported
    - 📁 File upload capability
    - 🚀 Works offline
    
    **Supported Languages:**
    """)
    
    # Show some popular supported languages
    popular_langs = [
        "English", "Spanish", "French", "German", "Italian",
        "Portuguese", "Russian", "Chinese", "Japanese", "Korean",
        "Arabic", "Hindi", "Dutch", "Swedish", "Polish"
    ]
    
    for lang in popular_langs:
        st.sidebar.write(f"• {lang}")
    
    st.sidebar.write("• And 35+ more...")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Tips for better results:**")
    st.sidebar.markdown("""
    - Use at least 10-20 characters
    - Avoid mixing multiple languages
    - Ensure text is properly encoded
    """)

if __name__ == "__main__":
    main()