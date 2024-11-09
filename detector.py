# detector.py
import spacy
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, Tuple, Any
from utils.text_processor import TextProcessor
from utils.validators import TextValidator

class AdvancedAIContentDetector:
    def __init__(self):
        """Initialize the AI Content Detector with required models and processors"""
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load('en_core_web_sm')
            
        self.text_processor = TextProcessor()
        self.validator = TextValidator()
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        
        # Initialize feature extractors
        self._init_feature_extractors()
    
    def _init_feature_extractors(self):
        """Initialize various feature extractors and analyzers"""
        self.analyzers = {
            'semantic': self._analyze_semantic_features,
            'statistical': self._analyze_statistical_features,
            'stylometric': self._analyze_stylometric_features
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Main analysis pipeline for text content
        """
        # Validate and preprocess text
        cleaned_text = self.text_processor.clean_text(text)
        if not self.validator.validate_input(cleaned_text):
            raise ValueError("Invalid input text")
            
        # Process text with spaCy
        doc = self.nlp(cleaned_text)
        
        # Extract features
        features = {}
        for name, analyzer in self.analyzers.items():
            features[name] = analyzer(doc, cleaned_text)
        
        # Calculate final scores
        scores = self._calculate_scores(features)
        
        return {
            'features': features,
            'scores': scores,
            'summary': self._generate_summary(scores, features)
        }
    
    def _analyze_semantic_features(self, doc, text: str) -> Dict[str, float]:
        """Analyze semantic features of the text"""
        return {
            'coherence': self._calculate_coherence(doc),
            'complexity': self._calculate_complexity(doc),
            'diversity': self._calculate_vocabulary_diversity(doc)
        }
    
    def _analyze_statistical_features(self, doc, text: str) -> Dict[str, float]:
        """Analyze statistical features of the text"""
        return {
            'entropy': self._calculate_entropy(text),
            'word_distributions': self._analyze_word_distributions(doc),
            'sentence_patterns': self._analyze_sentence_patterns(doc)
        }
    
    def _analyze_stylometric_features(self, doc, text: str) -> Dict[str, float]:
        """Analyze stylometric features of the text"""
        return {
            'readability': self._calculate_readability(doc),
            'formality': self._calculate_formality(doc),
            'consistency': self._calculate_style_consistency(doc)
        }
    
    # Various helper methods for feature calculation
    def _calculate_coherence(self, doc) -> float:
        """Calculate semantic coherence score"""
        scores = []
        for sent1, sent2 in zip(doc.sents, list(doc.sents)[1:]):
            scores.append(sent1.similarity(sent2))
        return np.mean(scores) if scores else 0.0
    
    def _calculate_complexity(self, doc) -> float:
        """Calculate linguistic complexity score"""
        measures = []
        for sent in doc.sents:
            depth = len(list(sent.root.ancestors))
            length = len([token for token in sent])
            measures.append(depth * length)
        return np.mean(measures) if measures else 0.0
    
    def _calculate_vocabulary_diversity(self, doc) -> float:
        """Calculate vocabulary diversity score"""
        words = [token.text.lower() for token in doc if token.is_alpha]
        if not words:
            return 0.0
        return len(set(words)) / len(words)
    
    def _calculate_scores(self, features: Dict) -> Dict[str, float]:
        """Calculate final scores based on all features"""
        from config import settings
        
        scores = {}
        for category, weight in settings.MODEL_WEIGHTS.items():
            category_features = features.get(category, {})
            if category_features:
                scores[category] = weight * np.mean(list(category_features.values()))
        
        scores['overall'] = sum(scores.values())
        return scores
    
    def _generate_summary(self, scores: Dict[str, float], features: Dict) -> str:
        """Generate a human-readable summary of the analysis"""
        overall_score = scores['overall']
        confidence_level = self._get_confidence_level(overall_score)
        
        summary = [
            f"Analysis Summary:",
            f"Overall AI Probability: {overall_score:.2%} ({confidence_level})",
            "\nKey Indicators:",
        ]
        
        for category, score in scores.items():
            if category != 'overall':
                summary.append(f"- {category.title()}: {score:.2%}")
        
        return "\n".join(summary)
    
    def _get_confidence_level(self, score: float) -> str:
        """Convert score to confidence level"""
        if score >= 0.8: return "Very High Confidence"
        elif score >= 0.6: return "High Confidence"
        elif score >= 0.4: return "Moderate Confidence"
        elif score >= 0.2: return "Low Confidence"
        else: return "Very Low Confidence"