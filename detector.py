# detector.py
import spacy
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, Any
import re
from utils.text_processor import TextProcessor
from utils.validators import TextValidator

class AdvancedAIContentDetector:
    def __init__(self):
        """Initialize the AI Content Detector"""
        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load('en_core_web_sm')
        
        self.text_processor = TextProcessor()
        self.validator = TextValidator()
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Main analysis pipeline"""
        # Clean and validate text
        cleaned_text = self.text_processor.clean_text(text)
        if not self.validator.validate_input(cleaned_text):
            raise ValueError("Invalid input text")
        
        # Process with spaCy
        doc = self.nlp(cleaned_text)
        
        # Extract features
        features = {
            'semantic': self._analyze_semantic_features(doc),
            'statistical': self._analyze_statistical_features(doc, cleaned_text),
            'stylometric': self._analyze_stylometric_features(doc)
        }
        
        # Calculate scores
        scores = self._calculate_scores(features)
        
        return {
            'scores': scores,
            'features': features,
            'summary': self._generate_summary(scores, features)
        }
    
    def _analyze_semantic_features(self, doc) -> Dict[str, float]:
        """Analyze semantic features"""
        return {
            'coherence': self._calculate_coherence(doc),
            'complexity': self._calculate_complexity(doc),
            'diversity': self._calculate_vocabulary_diversity(doc)
        }
    
    def _analyze_statistical_features(self, doc, text: str) -> Dict[str, float]:
        """Analyze statistical features"""
        sentences = [sent.text for sent in doc.sents]
        return {
            'avg_sentence_length': np.mean([len(sent.split()) for sent in sentences]) if sentences else 0,
            'punctuation_ratio': len(re.findall(r'[.,!?;:]', text)) / len(text) if text else 0,
            'stopword_ratio': len([token for token in doc if token.is_stop]) / len(doc) if len(doc) > 0 else 0
        }
    
    def _analyze_stylometric_features(self, doc) -> Dict[str, float]:
        """Analyze stylometric features"""
        return {
            'formality': self._calculate_formality(doc),
            'readability': self._calculate_readability(doc),
            'vocabulary_richness': len(set([token.text.lower() for token in doc])) / len(doc) if len(doc) > 0 else 0
        }
    
    def _calculate_coherence(self, doc) -> float:
        """Calculate text coherence"""
        sentences = list(doc.sents)
        if len(sentences) < 2:
            return 0.0
        
        similarities = []
        for i in range(len(sentences)-1):
            similarity = sentences[i].similarity(sentences[i+1])
            similarities.append(similarity)
        
        return np.mean(similarities)
    
    def _calculate_complexity(self, doc) -> float:
        """Calculate linguistic complexity"""
        if len(doc) == 0:
            return 0.0
            
        word_lengths = [len(token.text) for token in doc if token.is_alpha]
        return np.mean(word_lengths) if word_lengths else 0.0
    
    def _calculate_vocabulary_diversity(self, doc) -> float:
        """Calculate vocabulary diversity"""
        words = [token.text.lower() for token in doc if token.is_alpha]
        if not words:
            return 0.0
        return len(set(words)) / len(words)
    
    def _calculate_formality(self, doc) -> float:
        """Calculate text formality"""
        if len(doc) == 0:
            return 0.0
            
        formal_pos = ['NOUN', 'ADJ', 'ADP', 'DET']
        informal_pos = ['PRON', 'VERB', 'ADV', 'INTJ']
        
        formal_count = len([token for token in doc if token.pos_ in formal_pos])
        informal_count = len([token for token in doc if token.pos_ in informal_pos])
        
        total = formal_count + informal_count
        return formal_count / total if total > 0 else 0.0
    
    def _calculate_readability(self, doc) -> float:
        """Calculate text readability"""
        sentences = list(doc.sents)
        if not sentences:
            return 0.0
            
        words_per_sent = [len([token for token in sent if token.is_alpha]) for sent in sentences]
        avg_words_per_sent = np.mean(words_per_sent) if words_per_sent else 0
        
        return 1.0 - min(avg_words_per_sent / 20.0, 1.0)
    
    def _calculate_scores(self, features: Dict) -> Dict[str, float]:
        """Calculate final scores"""
        scores = {}
        
        # Calculate category scores
        for category, metrics in features.items():
            scores[category] = np.mean(list(metrics.values()))
        
        # Calculate overall score
        weights = {'semantic': 0.4, 'statistical': 0.3, 'stylometric': 0.3}
        scores['overall'] = sum(scores[cat] * weights[cat] for cat in weights)
        
        return {k: float(v) for k, v in scores.items()}
    
    def _generate_summary(self, scores: Dict[str, float], features: Dict) -> str:
        """Generate analysis summary"""
        confidence_levels = {
            0.8: "Very High",
            0.6: "High",
            0.4: "Moderate",
            0.2: "Low"
        }
        
        overall_score = scores['overall']
        confidence = next((level for threshold, level in sorted(confidence_levels.items(), reverse=True)
                         if overall_score >= threshold), "Very Low")
        
        summary = [
            f"AI Content Analysis Report",
            f"Overall AI Probability: {overall_score:.2%} ({confidence} Confidence)",
            "\nDetailed Scores:"
        ]
        
        for category, score in scores.items():
            if category != 'overall':
                summary.append(f"- {category.title()}: {score:.2%}")
        
        return "\n".join(summary)
