from typing import List, Dict
from datetime import datetime

class EmailDraftGenerator:
    """Generates email drafts in the specified format"""
    
    def __init__(self, user_info: Dict = None):
        self.user_info = user_info or {}
        
    def generate_draft(self, analysis_results: Dict) -> Dict:
        """
        Generate email draft from analysis results
        
        Args:
            analysis_results: Dictionary containing analyzed data
            
        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        top_items = analysis_results.get('top_items', [])
        
        # Generate subject line
        subject = self._generate_subject(top_items)
        
        # Generate email body
        body = self._generate_body(top_items, analysis_results)
        
        return {
            'subject': subject,
            'body': body,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'calendar_events_analyzed': analysis_results.get('calendar_count', 0),
                'emails_analyzed': analysis_results.get('email_count', 0),
                'items_count': len(top_items)
            }
        }
    
    def _generate_subject(self, top_items: List[Dict]) -> str:
        """Generate subject line based on top items"""
        # Extract top 3 customer/project names for subject
        top_names = []
        for item in top_items[:3]:
            name = item.get('name', '')
            if name and name not in top_names:
                top_names.append(name)
        
        # Default subject format
        if top_names:
            subject_items = ' | '.join(top_names[:3])
            return f"Top 5 Things - {subject_items}"
        else:
            return "Top 5 Things - Monthly Update"
    
    def _generate_body(self, top_items: List[Dict], analysis_results: Dict) -> str:
        """Generate email body in the specified format"""
        body_lines = []
        
        # Header
        body_lines.append("Industry Business Development / Account Updates")
        body_lines.append("")
        
        # Generate entries for each top item
        for idx, item in enumerate(top_items, 1):
            name = item.get('name', f'Item {idx}')
            context = item.get('context', [])
            frequency = item.get('frequency', 0)
            
            # Item header with name
            body_lines.append(f"{name} -")
            
            # Add context as bullet points
            if context:
                for ctx in context[:3]:  # Limit to 3 context items
                    # Clean up context text
                    ctx_clean = ctx.replace('\r\n', ' ').replace('\n', ' ').strip()
                    if ctx_clean and not ctx_clean.startswith('Meeting:'):
                        body_lines.append(f"  {ctx_clean}")
                    elif ctx_clean.startswith('Meeting:'):
                        meeting_name = ctx_clean.replace('Meeting:', '').strip()
                        body_lines.append(f"  Ongoing discussions and meetings: {meeting_name}")
            else:
                # Placeholder if no context found
                body_lines.append(f"  Active engagement with {frequency} interactions this month")
                body_lines.append(f"  [Add specific details about current activities and status]")
            
            # Add spacing between items
            body_lines.append("")
        
        # Add footer note
        body_lines.append("")
        body_lines.append("---")
        body_lines.append(f"Generated from {analysis_results.get('calendar_count', 0)} calendar events "
                         f"and {analysis_results.get('email_count', 0)} sent emails from the past 30 days.")
        body_lines.append("")
        body_lines.append("Note: Please review and add specific details, metrics, and action items for each entry.")
        
        return '\n'.join(body_lines)
    
    def format_for_display(self, draft: Dict) -> str:
        """Format draft for display in web UI"""
        subject = draft.get('subject', '')
        body = draft.get('body', '')
        
        formatted = f"Subject: {subject}\n\n"
        formatted += "=" * 80 + "\n\n"
        formatted += body
        
        return formatted
    
    def format_as_html(self, draft: Dict) -> str:
        """Format draft as HTML for web display"""
        subject = draft.get('subject', '')
        body = draft.get('body', '')
        metadata = draft.get('metadata', {})
        
        # Convert body to HTML with proper formatting
        body_html = body.replace('\n', '<br>')
        
        html = f"""
        <div class="email-draft">
            <div class="email-header">
                <strong>Subject:</strong> {subject}
            </div>
            <hr>
            <div class="email-body">
                {body_html}
            </div>
            <hr>
            <div class="email-metadata">
                <small>
                    Generated: {metadata.get('generated_at', 'N/A')}<br>
                    Calendar Events: {metadata.get('calendar_events_analyzed', 0)}<br>
                    Emails Analyzed: {metadata.get('emails_analyzed', 0)}<br>
                    Top Items: {metadata.get('items_count', 0)}
                </small>
            </div>
        </div>
        """
        
        return html

