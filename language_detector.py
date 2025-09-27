'''import streamlit as st
from langdetect import detect, detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from config import LANGUAGE_NAMES
import re

# Set seed for consistent results
DetectorFactory.seed = 0

class LanguageDetector:
    """
    A language detection class that uses multiple methods for accurate detection
    """
    
    def __init__(self):
        """Initialize the language detector"""
        self.language_names = LANGUAGE_NAMES
        
    def detect_language(self, text):
        """
        Detect the language of input text
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Dictionary with language info or None if detection fails
        """
        
        if not text or not text.strip():
            return None
            
        # Clean the text
        cleaned_text = self._clean_text(text)
        
        if len(cleaned_text) < 3:
            return None
        
        try:
            # Primary detection method using langdetect
            result = self._detect_with_langdetect(cleaned_text)
            return result
            
        except Exception as e:
            st.error(f"Detection error: {str(e)}")
            return None
    
    def _detect_with_langdetect(self, text):
        """
        Detect language using langdetect library
        
        Args:
            text (str): Cleaned text to analyze
            
        Returns:
            dict: Language detection result
        """
        try:
            # Get the most probable language
            language_code = detect(text)
            
            # Get probability scores for all detected languages
            language_probabilities = detect_langs(text)
            
            # Find the confidence for the detected language
            confidence = 0.0
            for lang_prob in language_probabilities:
                if lang_prob.lang == language_code:
                    confidence = lang_prob.prob
                    break
            
            # Get the full language name
            language_name = self.language_names.get(language_code, language_code.upper())
            
            return {
                'language_code': language_code,
                'language_name': language_name,
                'confidence': confidence,
                'all_probabilities': [(lp.lang, lp.prob) for lp in language_probabilities]
            }
            
        except LangDetectException:
            # If langdetect fails, return None
            return None
    
    def _clean_text(self, text):
        """
        Clean text for better language detection
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove excessive punctuation (keep some for context)
        text = re.sub(r'[^\w\s.,!?;:()\-\'\"]+', ' ', text)
        
        # Remove numbers that are standalone (keep numbers in words)
        text = re.sub(r'\b\d+\b', ' ', text)
        
        # Clean up extra spaces again
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text
    
    def get_supported_languages(self):
        """
        Get list of supported languages
        
        Returns:
            dict: Dictionary of language codes and names
        """
        return self.language_names
    
    def detect_multiple_languages(self, text, top_n=3):
        """
        Detect multiple possible languages with their probabilities
        
        Args:
            text (str): Input text to analyze
            top_n (int): Number of top languages to return
            
        Returns:
            list: List of language detection results
        """
        if not text or not text.strip():
            return []
            
        cleaned_text = self._clean_text(text)
        
        if len(cleaned_text) < 3:
            return []
        
        try:
            # Get probability scores for all detected languages
            language_probabilities = detect_langs(cleaned_text)
            
            results = []
            for i, lang_prob in enumerate(language_probabilities[:top_n]):
                language_name = self.language_names.get(lang_prob.lang, lang_prob.lang.upper())
                results.append({
                    'language_code': lang_prob.lang,
                    'language_name': language_name,
                    'confidence': lang_prob.prob,
                    'rank': i + 1
                })
            
            return results
            
        except LangDetectException:
            return []
    
    def is_language_supported(self, language_code):
        """
        Check if a language is supported
        
        Args:
            language_code (str): Language code to check
            
        Returns:
            bool: True if supported, False otherwise
        """
        return language_code.lower() in self.language_names 
'''

'''import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from langdetect import detect, detect_langs, DetectorFactory
import langid
import re
import time
import numpy as np

class LanguageDetector:
    """
    Multi-method language detector with ensemble approach for higher accuracy
    """
    
    def __init__(self):
        """Initialize multiple detection methods"""
        self.methods = {
            'transformer': None,
            'langdetect': True,
            'langid': True
        }
        self.language_names = self._load_language_names()
        self._initialize_models()
        
        # Set seed for reproducible results
        DetectorFactory.seed = 0
    
    @st.cache_resource
    def _initialize_models(_self):
        """Initialize all available models"""
        try:
            # Load transformer model (most accurate)
            model_name = "papluca/xlm-roberta-base-language-detection"
            _self.methods['transformer'] = pipeline(
                "text-classification",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1,
                return_all_scores=True
            )
            st.success("🚀 Transformer model loaded successfully!")
        except Exception as e:
            st.warning(f"Transformer model failed to load: {e}")
            _self.methods['transformer'] = None
    
    def detect_language(self, text, use_ensemble=True):
        """
        Use ensemble of multiple methods for highest accuracy
        
        Args:
            text (str): Input text
            use_ensemble (bool): Whether to use multiple methods
            
        Returns:
            dict: Enhanced detection results
        """
        if not text or len(text.strip()) < 3:
            return None
        
        # Clean and preprocess text
        cleaned_text = self._advanced_text_cleaning(text)
        
        results = {}
        confidence_scores = []
        
        # Method 1: Transformer (highest accuracy)
        if self.methods['transformer']:
            try:
                transformer_result = self._detect_with_transformer(cleaned_text)
                results['transformer'] = transformer_result
                confidence_scores.append(transformer_result['confidence'])
            except Exception as e:
                st.warning(f"Transformer detection failed: {e}")
        
        # Method 2: LangDetect (good for statistical patterns)
        if self.methods['langdetect']:
            try:
                langdetect_result = self._detect_with_langdetect(cleaned_text)
                results['langdetect'] = langdetect_result
                confidence_scores.append(langdetect_result['confidence'])
            except:
                pass
        
        # Method 3: LangID (alternative statistical method)
        if self.methods['langid']:
            try:
                langid_result = self._detect_with_langid(cleaned_text)
                results['langid'] = langid_result
                confidence_scores.append(langid_result['confidence'])
            except:
                pass
        
        # Ensemble decision making
        if use_ensemble and len(results) > 1:
            final_result = self._ensemble_decision(results, text)
        else:
            # Use best single method
            final_result = self._get_best_single_result(results)
        
        # Add metadata
        final_result.update({
            'methods_used': list(results.keys()),
            'text_length': len(text),
            'cleaned_text_length': len(cleaned_text),
            'processing_methods': len(results)
        })
        
        return final_result
    
    def _detect_with_transformer(self, text):
        """Detect using transformer model"""
        start_time = time.time()
        
        # Truncate text if too long (transformer limits)
        if len(text) > 512:
            text = text[:512]
        
        results = self.methods['transformer'](text)
        top_result = max(results[0], key=lambda x: x['score'])
        
        processing_time = time.time() - start_time
        
        return {
            'language_code': top_result['label'],
            'language_name': self._code_to_name(top_result['label']),
            'confidence': top_result['score'],
            'method': 'transformer',
            'processing_time': processing_time,
            'all_scores': results[0][:5]  # Top 5 results
        }
    
    def _detect_with_langdetect(self, text):
        """Detect using langdetect"""
        start_time = time.time()
        
        language_code = detect(text)
        probabilities = detect_langs(text)
        confidence = probabilities[0].prob
        
        processing_time = time.time() - start_time
        
        return {
            'language_code': language_code,
            'language_name': self._code_to_name(language_code),
            'confidence': confidence,
            'method': 'langdetect',
            'processing_time': processing_time,
            'all_probabilities': [(lp.lang, lp.prob) for lp in probabilities[:5]]
        }
    
    def _detect_with_langid(self, text):
        """Detect using langid"""
        start_time = time.time()
        
        language_code, confidence = langid.classify(text)
        
        processing_time = time.time() - start_time
        
        return {
            'language_code': language_code,
            'language_name': self._code_to_name(language_code),
            'confidence': confidence,
            'method': 'langid',
            'processing_time': processing_time
        }
    
    def _ensemble_decision(self, results, original_text):
        """Make ensemble decision from multiple methods"""
        
        # Weight different methods based on reliability
        method_weights = {
            'transformer': 0.5,
            'langdetect': 0.3,
            'langid': 0.2
        }
        
        # Collect all predictions
        predictions = {}
        
        for method, result in results.items():
            lang = result['language_code']
            confidence = result['confidence']
            weight = method_weights.get(method, 0.1)
            
            if lang not in predictions:
                predictions[lang] = 0
            predictions[lang] += confidence * weight
        
        # Get the language with highest weighted score
        best_lang = max(predictions.keys(), key=lambda x: predictions[x])
        best_score = predictions[best_lang]
        
        # Get the best individual result for additional info
        best_method_result = max(results.values(), key=lambda x: x['confidence'])
        
        return {
            'language_code': best_lang,
            'language_name': self._code_to_name(best_lang),
            'confidence': best_score,
            'method': 'ensemble',
            'ensemble_scores': predictions,
            'best_individual_method': best_method_result['method'],
            'agreement_level': self._calculate_agreement(results)
        }
    
    def _get_best_single_result(self, results):
        """Get the result with highest confidence"""
        if not results:
            return None
        
        return max(results.values(), key=lambda x: x['confidence'])
    
    def _calculate_agreement(self, results):
        """Calculate agreement level between different methods"""
        if len(results) < 2:
            return 1.0
        
        languages = [r['language_code'] for r in results.values()]
        # Simple agreement: percentage of methods that agree with most common prediction
        most_common = max(set(languages), key=languages.count)
        agreement = languages.count(most_common) / len(languages)
        
        return agreement
    
    def _advanced_text_cleaning(self, text):
        """Advanced text cleaning for better accuracy"""
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'\"]+', ' ', text)
        
        # Remove standalone numbers but keep numbers in words
        text = re.sub(r'\b\d+\b', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove very short words (less than 2 characters) that might be noise
        words = text.split()
        words = [word for word in words if len(word) >= 2 or word.isalpha()]
        
        return ' '.join(words)
    
    def _code_to_name(self, code):
        """Convert language code to full name"""
        return self.language_names.get(code.lower(), code.upper())
    
    def _load_language_names(self):
        """Load comprehensive language names mapping"""
        return {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'zh': 'Chinese',
            'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi',
            'nl': 'Dutch', 'sv': 'Swedish', 'no': 'Norwegian', 'da': 'Danish',
            'fi': 'Finnish', 'pl': 'Polish', 'cs': 'Czech', 'sk': 'Slovak',
            'hu': 'Hungarian', 'ro': 'Romanian', 'bg': 'Bulgarian', 'hr': 'Croatian',
            'sl': 'Slovenian', 'et': 'Estonian', 'lv': 'Latvian', 'lt': 'Lithuanian',
            'el': 'Greek', 'tr': 'Turkish', 'he': 'Hebrew', 'th': 'Thai',
            'vi': 'Vietnamese', 'id': 'Indonesian', 'ms': 'Malay', 'tl': 'Tagalog',
            'sw': 'Swahili', 'af': 'Afrikaans', 'is': 'Icelandic', 'mt': 'Maltese',
            'cy': 'Welsh', 'ga': 'Irish', 'mk': 'Macedonian', 'be': 'Belarusian',
            'uk': 'Ukrainian', 'bn': 'Bengali', 'gu': 'Gujarati', 'pa': 'Punjabi',
            'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada', 'ml': 'Malayalam',
            'mr': 'Marathi', 'ur': 'Urdu', 'fa': 'Persian', 'ne': 'Nepali',
            'si': 'Sinhala', 'my': 'Burmese', 'km': 'Khmer', 'lo': 'Lao',
            'ka': 'Georgian', 'am': 'Amharic', 'so': 'Somali', 'sq': 'Albanian',
            'eu': 'Basque', 'ca': 'Catalan', 'gl': 'Galician'
        }
    
    def batch_detect(self, texts, use_ensemble=True):
        """Detect languages for multiple texts efficiently"""
        results = []
        
        with st.progress(0) as progress_bar:
            for i, text in enumerate(texts):
                result = self.detect_language_ensemble(text, use_ensemble)
                results.append(result)
                progress_bar.progress((i + 1) / len(texts))
        
        return results
    
    def get_detection_stats(self, result):
        """Get detailed statistics about the detection"""
        if not result:
            return None
        
        stats = {
            'confidence_level': 'High' if result['confidence'] > 0.9 else 'Medium' if result['confidence'] > 0.7 else 'Low',
            'text_analysis': {
                'original_length': result.get('text_length', 0),
                'processed_length': result.get('cleaned_text_length', 0),
                'reduction_ratio': 1 - (result.get('cleaned_text_length', 0) / max(result.get('text_length', 1), 1))
            },
            'performance': {
                'processing_time': result.get('processing_time', 0),
                'methods_used': result.get('methods_used', []),
                'agreement_level': result.get('agreement_level', 1.0)
            }
        }
        
        return stats
'''
'''import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import streamlit as st
from config import LANGUAGE_NAMES
import re

class LanguageDetector:
    """
    A language detection class that uses MultinomialNB for detection
    """
    
    def __init__(self, dataset_path):
        """Initialize the language detector and train the model"""
        self.language_names = LANGUAGE_NAMES
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
        self.train_on_dataset(dataset_path)
    
    def train_on_dataset(self, dataset_path):
        """Load and preprocess dataset, then train the model"""
        X, y = self.load_and_preprocess_data(dataset_path)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        self.train_model(X_train, y_train)
        # Optionally, evaluate the model on the test set
        accuracy = self.evaluate_model(X_test, y_test)
        st.info(f"Model trained with accuracy: {accuracy:.2f}")

    def load_and_preprocess_data(self, dataset_path):
        """Load and preprocess custom dataset"""
        data = pd.read_csv(dataset_path)
        if 'Text' not in data.columns or 'language' not in data.columns:
            raise KeyError('Text' if 'Text' not in data.columns else 'language')
        texts = data['Text']
        labels = data['language']
        X = self.vectorizer.fit_transform(texts)
        return X, labels

    def train_model(self, X, y):
        """Train MultinomialNB model"""
        self.model.fit(X, y)

    def evaluate_model(self, X_test, y_test):
        """Evaluate the model on the test set"""
        predictions = self.model.predict(X_test)
        accuracy = (predictions == y_test).mean()
        return accuracy

    def predict_language(self, text):
        """Predict language using trained MultinomialNB model"""
        X = self.vectorizer.transform([text])
        predicted_label = self.model.predict(X)
        return predicted_label[0]

    def _clean_text(self, text):
        """
        Clean text for better language detection
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove excessive punctuation (keep some for context)
        text = re.sub(r'[^\w\s.,!?;:()\-\'\"]+', ' ', text)
        
        # Remove numbers that are standalone (keep numbers in words)
        text = re.sub(r'\b\d+\b', ' ', text)
        
        # Clean up extra spaces again
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text
    
    def get_supported_languages(self):
        """
        Get list of supported languages
        
        Returns:
            dict: Dictionary of language codes and names
        """
        return self.language_names
'''

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, cross_val_score
import streamlit as st
from config import LANGUAGE_NAMES
import re

class LanguageDetector:
    """
    A language detection class that uses MultinomialNB for detection
    """
    
    def __init__(self, dataset_path):
        """Initialize the language detector and train the model"""
        self.language_names = LANGUAGE_NAMES
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Using bigrams
        self.model = MultinomialNB(alpha=0.1)  # Adjusted alpha for smoothing
        self.train_on_dataset(dataset_path)
    
    def train_on_dataset(self, dataset_path):
        """Load and preprocess dataset, then train the model"""
        X, y = self.load_and_preprocess_data(dataset_path)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        self.train_model(X_train, y_train)
        # Evaluate the model on the test set
        accuracy = self.evaluate_model(X_test, y_test)
        st.info(f"Model trained with accuracy: {accuracy:.2f}")
        # Cross-validation for robust evaluation
        cv_scores = cross_val_score(self.model, X, y, cv=5)
        st.info(f"Cross-validated accuracy: {cv_scores.mean():.2f} ± {cv_scores.std():.2f}")

    def load_and_preprocess_data(self, dataset_path):
        """Load and preprocess custom dataset"""
        data = pd.read_csv(dataset_path)
        if 'Text' not in data.columns or 'language' not in data.columns:
            raise KeyError('Text' if 'Text' not in data.columns else 'language')
        texts = data['Text']
        labels = data['language']
        X = self.vectorizer.fit_transform(texts)
        return X, labels

    def train_model(self, X, y):
        """Train MultinomialNB model"""
        self.model.fit(X, y)

    def evaluate_model(self, X_test, y_test):
        """Evaluate the model on the test set"""
        predictions = self.model.predict(X_test)
        accuracy = (predictions == y_test).mean()
        return accuracy

    def predict_language(self, text):
        """Predict language using trained MultinomialNB model"""
        X = self.vectorizer.transform([text])
        predicted_label = self.model.predict(X)
        return predicted_label[0]

    def _clean_text(self, text):
        """
        Clean text for better language detection
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove excessive punctuation (keep some for context)
        text = re.sub(r'[^\w\s.,!?;:()\-\'\"]+', ' ', text)
        
        # Remove numbers that are standalone (keep numbers in words)
        text = re.sub(r'\b\d+\b', ' ', text)
        
        # Clean up extra spaces again
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text
    
    def get_supported_languages(self):
        """
        Get list of supported languages
        
        Returns:
            dict: Dictionary of language codes and names
        """
        return self.language_names