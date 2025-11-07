import re
from collections import Counter, defaultdict
import spacy
from typing import List, Dict, Tuple

class DataAnalyzer:
    """Analyzes calendar and email data to extract top topics, customers, and projects"""
    
    def __init__(self):
        # Load spaCy model for NLP
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Downloading spaCy model...")
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
            self.nlp = spacy.load('en_core_web_sm')
        
        # Common tech/business terms to look for
        self.tech_keywords = {
            'poc', 'pov', 'proof of concept', 'proof of value', 'pilot',
            'kubernetes', 'k8s', 'gpu', 'inference', 'training', 'ml', 'ai',
            'deployment', 'integration', 'testing', 'validation', 'demo',
            'ebc', 'technical review', 'architecture', 'platform', 'scheduler',
            'workload', 'cluster', 'node', 'container', 'docker', 'ray',
            'distributed', 'optimization', 'efficiency', 'performance'
        }
        
    def analyze_data(self, calendar_events: List[Dict], sent_emails: List[Dict]) -> Dict:
        """
        Analyze calendar and email data to extract insights
        
        Args:
            calendar_events: List of calendar event dictionaries
            sent_emails: List of sent email dictionaries
            
        Returns:
            Dictionary containing analyzed data with top entities
        """
        # Extract entities from calendar
        calendar_entities = self._extract_calendar_entities(calendar_events)
        
        # Extract entities from emails
        email_entities = self._extract_email_entities(sent_emails)
        
        # Combine and rank entities
        combined_entities = self._combine_entities(calendar_entities, email_entities)
        
        # Extract top items with context
        top_items = self._extract_top_items(combined_entities, calendar_events, sent_emails)
        
        return {
            'top_items': top_items,
            'calendar_count': len(calendar_events),
            'email_count': len(sent_emails),
            'entities': combined_entities
        }
    
    def _extract_calendar_entities(self, events: List[Dict]) -> Dict:
        """Extract entities from calendar events"""
        entities = {
            'organizations': Counter(),
            'topics': Counter(),
            'projects': Counter(),
            'people': Counter()
        }
        
        for event in events:
            subject = event.get('subject', '')
            body = event.get('body', {}).get('content', '')
            
            # Combine subject and body for analysis
            text = f"{subject} {body}"
            
            # Extract organizations (likely customer names)
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    entities['organizations'][ent.text] += 1
                elif ent.label_ == 'PERSON':
                    entities['people'][ent.text] += 1
            
            # Extract tech keywords and topics
            text_lower = text.lower()
            for keyword in self.tech_keywords:
                if keyword in text_lower:
                    entities['topics'][keyword] += 1
            
            # Look for project patterns (PoC, PoV, etc.)
            project_patterns = [
                r'(?i)(poc|pov|pilot|proof of (?:concept|value))\s+(?:for|with|at)?\s+([A-Z][a-zA-Z\s]+)',
                r'(?i)([A-Z][a-zA-Z\s]+)\s+(?:poc|pov|pilot)',
            ]
            for pattern in project_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    project_name = ' '.join(match).strip()
                    if project_name:
                        entities['projects'][project_name] += 1
        
        return entities
    
    def _extract_email_entities(self, emails: List[Dict]) -> Dict:
        """Extract entities from sent emails"""
        entities = {
            'organizations': Counter(),
            'topics': Counter(),
            'projects': Counter(),
            'people': Counter()
        }
        
        for email in emails:
            subject = email.get('subject', '')
            body_preview = email.get('bodyPreview', '')
            
            # Combine subject and body preview
            text = f"{subject} {body_preview}"
            
            # Extract organizations
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    entities['organizations'][ent.text] += 2  # Weight emails higher
                elif ent.label_ == 'PERSON':
                    entities['people'][ent.text] += 1
            
            # Extract tech keywords
            text_lower = text.lower()
            for keyword in self.tech_keywords:
                if keyword in text_lower:
                    entities['topics'][keyword] += 2  # Weight emails higher
            
            # Extract recipients as potential customers/partners
            recipients = email.get('toRecipients', []) + email.get('ccRecipients', [])
            for recipient in recipients:
                email_addr = recipient.get('emailAddress', {}).get('address', '')
                # Extract domain as potential organization
                if '@' in email_addr:
                    domain = email_addr.split('@')[1].split('.')[0]
                    if domain not in ['nvidia', 'gmail', 'outlook', 'hotmail']:
                        entities['organizations'][domain.capitalize()] += 1
        
        return entities
    
    def _combine_entities(self, calendar_entities: Dict, email_entities: Dict) -> Dict:
        """Combine entities from calendar and email with weighted scoring"""
        combined = {
            'organizations': Counter(),
            'topics': Counter(),
            'projects': Counter(),
            'people': Counter()
        }
        
        for entity_type in combined.keys():
            combined[entity_type].update(calendar_entities[entity_type])
            combined[entity_type].update(email_entities[entity_type])
        
        return combined
    
    def _extract_top_items(self, entities: Dict, calendar_events: List[Dict], 
                          sent_emails: List[Dict]) -> List[Dict]:
        """Extract top items with context for email generation"""
        top_items = []
        
        # Get top organizations (customers)
        top_orgs = entities['organizations'].most_common(10)
        
        for org, count in top_orgs:
            # Find context from calendar and emails
            context = self._find_context(org, calendar_events, sent_emails)
            
            if context:
                top_items.append({
                    'name': org,
                    'type': 'customer',
                    'frequency': count,
                    'context': context
                })
        
        # Sort by frequency and return top N
        top_items.sort(key=lambda x: x['frequency'], reverse=True)
        return top_items[:7]
    
    def _find_context(self, entity: str, calendar_events: List[Dict], 
                     sent_emails: List[Dict]) -> List[str]:
        """Find context snippets mentioning the entity"""
        context = []
        entity_lower = entity.lower()
        
        # Search calendar events
        for event in calendar_events[:50]:  # Limit to recent events
            subject = event.get('subject', '')
            if entity_lower in subject.lower():
                context.append(f"Meeting: {subject}")
        
        # Search emails
        for email in sent_emails[:50]:  # Limit to recent emails
            subject = email.get('subject', '')
            preview = email.get('bodyPreview', '')
            
            if entity_lower in subject.lower() or entity_lower in preview.lower():
                # Extract relevant sentence
                sentences = preview.split('.')
                for sentence in sentences:
                    if entity_lower in sentence.lower():
                        context.append(sentence.strip())
                        break
        
        return context[:5]  # Return top 5 context items

