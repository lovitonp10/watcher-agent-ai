"""
Email service for sending digest reports.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from litellm import completion
import os

console = Console()


class EmailService:
    """Handles email sending for daily digests."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        from_email: str,
        use_tls: bool = True,
        llm_provider: str = "ollama",
        llm_model: str = "mistral",
        llm_api_key: str = None,
        llm_base_url: str = None,
        llm_temperature: float = 0.3,
    ):
        """
        Initialize email service.

        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password
            from_email: From email address
            use_tls: Use TLS encryption
            llm_provider: LLM provider for generating insights
            llm_model: LLM model name
            llm_api_key: API key for LLM provider
            llm_base_url: Base URL for LLM API
            llm_temperature: Temperature for LLM generation
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.use_tls = use_tls

        # LLM configuration
        self.llm_provider = llm_provider.lower()
        self.llm_model = self._format_model_name(llm_model)
        self.llm_temperature = llm_temperature
        self.llm_base_url = llm_base_url

        # Set API key in environment for LiteLLM
        if llm_api_key:
            if self.llm_provider == "openai":
                os.environ["OPENAI_API_KEY"] = llm_api_key
            elif self.llm_provider == "mistral":
                os.environ["MISTRAL_API_KEY"] = llm_api_key
            elif self.llm_provider == "anthropic":
                os.environ["ANTHROPIC_API_KEY"] = llm_api_key
            elif self.llm_provider == "groq":
                os.environ["GROQ_API_KEY"] = llm_api_key

    def _format_model_name(self, model: str) -> str:
        """Format model name for LiteLLM provider prefix."""
        # If model already has a provider prefix, return as-is
        if "/" in model:
            return model

        # Add provider prefix for LiteLLM
        if self.llm_provider in ["mistral", "anthropic", "ollama", "groq"]:
            return f"{self.llm_provider}/{model}"

        return model

    def _generate_video_popularity_insight(self, doc: Dict[str, Any], use_llm: bool = True) -> str:
        """
        Generate actionable Video Popularity project insights.

        Args:
            doc: Document dictionary
            use_llm: If True, try LLM analysis; if False or LLM fails, use keyword-based fallback

        Returns:
            HTML insight text with actionable recommendations
        """
        title = doc.get("title", "")
        abstract = doc.get("abstract", "")
        source = doc.get("source", "unknown")
        text = f"{title} {abstract}".lower()

        llm_error = None  # Track LLM errors for display in email

        # Try LLM analysis first if enabled
        if use_llm:
            try:
                prompt = f"""You are analyzing research papers for a Video Popularity Prediction project.

PROJECT CONTEXT:
We're building a multimodal AI system to predict video virality on TikTok/Instagram. The system analyzes:
- Visual features (frames, scenes, aesthetics)
- Audio features (music, voice, BPM)
- Text features (captions, hashtags, titles)
- Engagement metrics (CTR, watch time, shares)
Goal: Help creators optimize content for maximum engagement.

PAPER TO ANALYZE:
Title: {title}
Abstract: {abstract[:600]}
Source: {source}

TASK:
1. Determine if this paper is RELEVANT to our video popularity prediction project
2. If NOT relevant (e.g., robotics, chip design, medical imaging, general NLP), output exactly: "NOT_RELEVANT"
3. If RELEVANT, provide specific, actionable insights:

LEVERS: (2-4 concrete technical approaches from this paper we can apply)
- Be specific: mention techniques, architectures, metrics, or methods
- Example: "Apply attention mechanisms to identify key video frames for engagement"
- Example: "Use SHAP values to explain which features (hashtags, music) drive virality"

BENEFITS: (2-3 measurable business/technical benefits)
- Be concrete: mention metrics, improvements, or outcomes
- Example: "10-15% improvement in prediction accuracy for 60s+ videos"
- Example: "Transparent feature importance → creator trust and adoption"

Keep each bullet under 15 words. Be specific to THIS paper's contribution, not generic."""

                messages = [
                    {"role": "system", "content": "You are a technical analyst specializing in ML research for social media applications."},
                    {"role": "user", "content": prompt}
                ]

                kwargs = {
                    "model": self.llm_model,
                    "messages": messages,
                    "temperature": 0.3,
                    "timeout": 60,  # Groq is fast, give it time for quality
                    "max_tokens": 500,  # Allow detailed responses
                }
                if self.llm_base_url:
                    kwargs["api_base"] = self.llm_base_url

                response = completion(**kwargs)
                result = response.choices[0].message.content.strip()

                if "NOT_RELEVANT" in result.upper():
                    return "<span style='color: #9ca3af; font-style: italic;'>Not directly applicable to video popularity prediction</span>"

                # Format as HTML
                html_output = result.replace("LEVERS:", "<strong>🎯 Levers:</strong>")
                html_output = html_output.replace("BENEFITS:", "<br><br><strong>💰 Benefits:</strong>")
                html_output = html_output.replace("Levers:", "<strong>🎯 Levers:</strong>")
                html_output = html_output.replace("Benefits:", "<br><br><strong>💰 Benefits:</strong>")
                return html_output

            except Exception as e:
                # Log to console
                console.print(f"[yellow]LLM analysis failed for '{title[:40]}...': {e}[/yellow]")
                console.print(f"[dim]Using keyword fallback instead[/dim]")

                # Store error for display in email
                error_msg = str(e)
                if len(error_msg) > 150:
                    error_msg = error_msg[:150] + "..."
                llm_error = error_msg

        # Keyword-based fallback - context-aware analysis

        # 1. Check if truly relevant to video popularity (STRICT filtering)
        video_relevant = any(kw in text for kw in [
            "video understanding", "video popularity", "video engagement", "video viral",
            "tiktok", "instagram reels", "youtube", "social media video",
            "short video", "video recommendation"
        ])

        # Exclude if multimodal but not video-related
        non_video_contexts = ["robot", "robotics", "chip", "floorplan", "navigation",
                               "autonomous", "embodied", "manipulation", "grasping"]
        is_non_video = any(kw in text for kw in non_video_contexts)

        if is_non_video or not video_relevant:
            # Check if it has engagement/recommendation focus
            has_engagement = any(kw in text for kw in ["engagement", "popularity", "viral", "recommendation"])
            has_explainability = any(kw in text for kw in ["explainability", "xai", "interpretability"])

            if not (has_engagement or has_explainability):
                return "<span style='color: #9ca3af; font-style: italic;'>Not directly applicable to video popularity prediction</span>"

        # 2. Generate context-specific insights based on paper content
        levers = []
        benefits = []

        # Video understanding techniques
        if any(kw in text for kw in ["video understanding", "temporal", "video-llm"]):
            levers.append("• Apply temporal modeling for video sequence analysis")
            benefits.append("• Better capture of video dynamics → +15% accuracy")

        # Multimodal fusion
        if any(kw in text for kw in ["multimodal", "vision-language", "cross-modal", "fusion"]):
            levers.append("• Implement multimodal fusion (vision+audio+text)")
            benefits.append("• Richer feature representation → improved F1-score")

        # Engagement/popularity specific
        if any(kw in text for kw in ["engagement", "popularity", "viral", "recommendation"]):
            levers.append("• Adapt engagement metrics from this research")
            benefits.append("• Alignment with real-world virality patterns")

        # Explainability
        if any(kw in text for kw in ["explainability", "xai", "interpretability", "attention"]):
            levers.append("• Add explainability layer for feature importance")
            benefits.append("• Transparent predictions → creator trust")

        # Long video handling
        if any(kw in text for kw in ["long video", "efficient", "token selection", "compression"]):
            levers.append("• Optimize for long-form video processing efficiency")
            benefits.append("• Handle 60s+ videos → broader coverage")

        # Platform-specific
        if any(kw in text for kw in ["tiktok", "instagram", "youtube", "social media"]):
            levers.append("• Benchmark against platform-specific algorithms")
            benefits.append("• Platform-aware predictions → +20% relevance")

        # Fallback if nothing specific matched
        if not levers:
            levers.append("• Extract techniques applicable to video prediction")
            levers.append("• Benchmark architecture against current model")

        if not benefits:
            benefits.append("• Improved prediction accuracy")
            benefits.append("• Actionable insights for creators")

        # Take top 3 levers and 2 benefits
        levers_html = "<strong>🎯 Levers:</strong><br>" + "<br>".join(levers[:3])
        benefits_html = "<br><br><strong>💰 Benefits:</strong><br>" + "<br>".join(benefits[:2])

        # Add error message if LLM failed
        error_html = ""
        if llm_error:
            error_html = f"<br><br><div style='background: #fef3c7; border-left: 3px solid #f59e0b; padding: 8px 12px; margin-top: 8px; border-radius: 4px;'><strong style='color: #92400e;'>⚠️ LLM analysis failed:</strong><br><span style='color: #78350f; font-size: 12px;'>{llm_error}</span><br><span style='color: #78350f; font-size: 12px; font-style: italic;'>Using keyword-based fallback analysis above</span></div>"

        return levers_html + benefits_html + error_html

    def _detect_article_theme(self, doc: Dict[str, Any]) -> tuple[str, str]:
        """
        Detect article theme and return (theme_name, theme_color).

        Args:
            doc: Document dictionary

        Returns:
            Tuple of (theme name, hex color)
        """
        title = doc.get("title", "").lower()
        abstract = doc.get("abstract", "").lower()
        text = f"{title} {abstract}"

        # Theme detection with priority order (most specific first)
        # Requires 2+ keyword matches or 1 very specific keyword for stricter filtering
        themes = [
            # (keywords, required_matches, theme_name, color)
            (["multimodal", "vision-language", "vlm", "video understanding", "video-llm", "visual-language"],
             1, "Multimodal & VLM", "#8b5cf6"),  # Purple - very specific keywords

            (["video popularity", "video viral", "tiktok", "instagram reels", "shorts algorithm"],
             1, "Social Media & Engagement", "#ec4899"),  # Pink - very specific

            (["explainability", "xai", "interpretability", "shap values", "lime explanation"],
             1, "Explainability & XAI", "#f59e0b"),  # Orange - specific

            (["3d reconstruction", "3d generation", "mesh generation", "neural rendering", "nerf"],
             1, "Computer Vision & 3D", "#10b981"),  # Green - specific

            (["large language model", "llm", "gpt", "transformer language", "bert"],
             1, "LLM & NLP", "#3b82f6"),  # Blue - specific

            (["diffusion model", "stable diffusion", "generative adversarial", "gan", "vae", "image generation"],
             1, "Generative AI", "#ec4899"),  # Pink - specific

            (["object detection", "image classification", "semantic segmentation", "instance segmentation"],
             1, "Detection & Classification", "#14b8a6"),  # Teal - specific

            (["ai agent", "autonomous agent", "multi-agent", "agent reasoning", "agent planning"],
             1, "AI Agents & Reasoning", "#a855f7"),  # Purple - specific

            (["misinformation detection", "fake news", "content moderation", "social media manipulation"],
             1, "Social AI & Misinformation", "#f59e0b"),  # Orange - specific

            (["benchmark dataset", "evaluation benchmark", "survey paper", "review paper"],
             1, "Datasets & Benchmarks", "#6366f1"),  # Indigo - specific

            (["transfer learning", "domain adaptation", "few-shot learning", "zero-shot learning"],
             1, "Transfer Learning", "#8b5cf6"),  # Purple - specific

            # Generic fallback categories (require 2+ matches)
            (["recommendation", "ranking", "engagement", "popularity"],
             2, "Recommendation Systems", "#ec4899"),  # Pink - generic, needs 2+

            (["video", "visual", "image", "computer vision"],
             2, "Computer Vision", "#10b981"),  # Green - generic, needs 2+

            (["attention", "transformer", "neural network"],
             2, "Deep Learning", "#3b82f6"),  # Blue - generic, needs 2+
        ]

        # Find matching theme with required match count
        for keywords, required_matches, theme_name, color in themes:
            match_count = sum(1 for kw in keywords if kw in text)
            if match_count >= required_matches:
                return (theme_name, color)

        # Default theme
        return ("General AI/ML", "#6b7280")  # Gray

    def _generate_theme_summary(self, docs: List[Dict[str, Any]]) -> str:
        """
        Generate a summary with count of articles by theme.

        Args:
            docs: List of documents

        Returns:
            HTML summary text with theme counts
        """
        from collections import Counter

        # Count articles by theme
        theme_counts = Counter()
        theme_colors = {}

        for doc in docs:
            theme_name, theme_color = self._detect_article_theme(doc)
            theme_counts[theme_name] += 1
            theme_colors[theme_name] = theme_color

        # Sort by count (descending)
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)

        # Build HTML summary
        summary_html = "<div style='line-height: 2;'>"

        for theme_name, count in sorted_themes:
            color = theme_colors[theme_name]
            summary_html += f"""
                <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                    <div style='width: 12px; height: 12px; background: {color}; border-radius: 3px; margin-right: 10px;'></div>
                    <span style='font-weight: 600; color: #111827;'>{theme_name}</span>
                    <span style='margin-left: auto; background: {color}20; color: {color}; padding: 2px 10px; border-radius: 12px; font-weight: 700; font-size: 14px;'>{count}</span>
                </div>
            """

        summary_html += "</div>"

        return summary_html

    def _rate_competitor_article_importance(self, doc: Dict[str, Any]) -> int:
        """
        Rate competitor article importance (1-3 stars) based on relevance to Video Popularity project.

        Args:
            doc: Document dictionary

        Returns:
            Rating from 1 to 3 stars
        """
        title = doc.get("title", "").lower()
        abstract = doc.get("abstract", "").lower()
        text = f"{title} {abstract}"

        # 3 stars: High priority keywords
        high_priority = [
            "viral", "popularity", "engagement", "algorithm", "recommendation",
            "tiktok", "instagram", "reels", "shorts", "fyp",
            "ai", "machine learning", "prediction", "analytics",
            "thumbnail", "title optimization", "a/b test"
        ]

        # 2 stars: Medium priority keywords
        medium_priority = [
            "video", "content", "creator", "youtube", "social media",
            "seo", "growth", "views", "subscribers", "audience",
            "retention", "watch time", "ctr", "click-through"
        ]

        # Count matches
        high_matches = sum(1 for kw in high_priority if kw in text)
        medium_matches = sum(1 for kw in medium_priority if kw in text)

        # Determine rating
        if high_matches >= 2:
            return 3  # ⭐⭐⭐
        elif high_matches >= 1 or medium_matches >= 3:
            return 2  # ⭐⭐
        else:
            return 1  # ⭐

    def _format_competitor_section(self, competitor_docs: List[Dict[str, Any]]) -> str:
        """
        Format competitor news section HTML (minimal: stars + title + date).

        Args:
            competitor_docs: List of competitor documents

        Returns:
            HTML for competitor news section
        """
        if not competitor_docs:
            return ""

        # Group by competitor
        competitors_grouped = {}
        for doc in competitor_docs:
            source = doc.get("source", "unknown")
            # Extract competitor name from source (format: competitor_vidiq)
            competitor_name = source.replace("competitor_", "").replace("_", " ").title()
            if competitor_name not in competitors_grouped:
                competitors_grouped[competitor_name] = []
            competitors_grouped[competitor_name].append(doc)

        # Build competitor cards (minimal format)
        competitor_html = ""
        for competitor_name, docs in competitors_grouped.items():
            # Take only most recent 5 posts
            recent_docs = sorted(
                docs,
                key=lambda x: x.get("published_date", "1970-01-01"),
                reverse=True
            )[:5]

            competitor_html += f"""
            <div style='background: white; border-radius: 8px; padding: 16px 20px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); border-left: 4px solid #ef4444;'>
                <h3 style='margin: 0 0 12px 0; color: #111827; font-size: 16px; font-weight: 700;'>
                    🎯 {competitor_name}
                </h3>
            """

            for doc in recent_docs:
                title = doc.get("title", "Untitled")
                url = doc.get("url", "#")
                date = doc.get("published_date", "")

                # Rate importance
                stars = self._rate_competitor_article_importance(doc)
                star_display = "⭐" * stars

                competitor_html += f"""
                <div style='padding: 8px 0; border-bottom: 1px solid #f3f4f6; display: flex; align-items: start; gap: 8px;'>
                    <div style='color: #f59e0b; font-size: 14px; min-width: 55px;'>{star_display}</div>
                    <div style='flex: 1;'>
                        <a href='{url}' style='color: #1f2937; text-decoration: none; font-weight: 500; font-size: 14px; line-height: 1.4;' target='_blank'>{title}</a>
                        <div style='color: #9ca3af; font-size: 12px; margin-top: 2px;'>📅 {date}</div>
                    </div>
                </div>
                """

            competitor_html += "</div>"

        # Wrap in section (compact)
        section_html = f"""
        <!-- Competitor News Section -->
        <div style='margin-bottom: 30px;'>
            <div style='display: flex; align-items: center; margin-bottom: 16px;'>
                <div style='width: 4px; height: 28px; background: linear-gradient(180deg, #ef4444 0%, #dc2626 100%); border-radius: 2px; margin-right: 12px;'></div>
                <h2 style='margin: 0; color: #111827; font-size: 22px; font-weight: 800;'>🚨 Competitors ({len(competitors_grouped)})</h2>
            </div>
            <div style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border: 1px solid #ef4444; padding: 10px 14px; border-radius: 8px; margin-bottom: 16px;'>
                <div style='color: #991b1b; font-size: 13px; font-weight: 600;'>
                    ⭐⭐⭐ High relevance | ⭐⭐ Medium relevance | ⭐ Monitor
                </div>
            </div>
            {competitor_html}
        </div>
        """

        return section_html

    def _format_html_digest(
        self,
        new_docs: List[Dict[str, Any]],
        summary: str,
        stats: Dict[str, Any],
        digest_type: str = "Daily",
        full_database: bool = False,
        max_articles: int = 15,
        competitor_docs: List[Dict[str, Any]] = None,
    ) -> str:
        """
        Format digest as HTML email with Video Popularity insights.

        Args:
            new_docs: List of documents
            summary: AI-generated summary
            stats: Database statistics
            digest_type: "Daily" or "Weekly"
            full_database: If True, showing full database
            max_articles: Maximum number of article cards to show in email
            competitor_docs: List of competitor news (optional, always shown separately)

        Returns:
            HTML email content
        """
        if competitor_docs is None:
            competitor_docs = []
        today = datetime.now().strftime("%d/%m/%Y")

        # Build document cards HTML (no grouping by source, all individual cards)
        docs_html = ""

        for doc in new_docs[:max_articles]:  # Limit articles
            title = doc.get("title", "Sans titre")
            url = doc.get("url", "#")

            # Use LLM-generated summary (preferred) or fallback to abstract
            summary = doc.get("llm_summary") or doc.get("abstract", "")

            # Truncate if too long
            if len(summary) > 350:
                summary = summary[:350] + "..."

            # If still empty, provide a minimal fallback
            if not summary or summary == "No summary available" or summary == "Summary unavailable":
                summary = "Summary unavailable. <a href='" + url + "' target='_blank'>Read full article →</a>"

            date = doc.get("published_date", "")
            source = doc.get("source", "unknown").replace('_', ' ').title()

            # Generate Video Popularity insight
            vp_insight = self._generate_video_popularity_insight(doc)

            # Detect theme and get color
            theme_name, border_color = self._detect_article_theme(doc)

            docs_html += f"""
            <div style='margin-bottom: 30px; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 6px solid {border_color};'>
                <!-- Card Header -->
                <div style='background: linear-gradient(135deg, {border_color}15 0%, {border_color}05 100%); padding: 20px 24px; border-bottom: 1px solid #e5e7eb;'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;'>
                        <div style='display: flex; gap: 8px; align-items: center;'>
                            <div style='background: {border_color}; color: white; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 600; text-transform: uppercase;'>
                                🏷️ {theme_name}
                            </div>
                            <div style='color: #9ca3af; font-size: 11px; font-weight: 500;'>
                                {source}
                            </div>
                        </div>
                        <div style='color: #6b7280; font-size: 13px;'>
                            📅 {date}
                        </div>
                    </div>
                    <h3 style='margin: 0; font-size: 20px; line-height: 1.4;'>
                        <a href='{url}' style='color: #111827; text-decoration: none; font-weight: 700;' target='_blank'>{title}</a>
                    </h3>
                </div>

                <!-- Card Body -->
                <div style='padding: 20px 24px;'>
                    <!-- Article Summary -->
                    <div style='background: #f9fafb; border-left: 3px solid #d1d5db; padding: 14px 16px; border-radius: 6px; margin-bottom: 16px;'>
                        <div style='color: #6b7280; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>
                            📄 Summary
                        </div>
                        <div style='color: #4b5563; font-size: 15px; line-height: 1.7;'>
                            {summary}
                        </div>
                    </div>

                    <!-- Video Popularity Insight Box -->
                    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px;'>
                        <div style='font-weight: 700; color: #92400e; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;'>
                            🎯 For Video Popularity Project
                        </div>
                        <div style='color: #78350f; font-size: 14px; line-height: 1.6;'>
                            {vp_insight}
                        </div>
                    </div>
                </div>
            </div>
            """

        if len(new_docs) > max_articles:
            docs_html += f"<div style='color: #6b7280; font-style: italic; text-align: center; padding: 20px; background: #f9fafb; border-radius: 8px;'>... and {len(new_docs) - max_articles} more articles in database</div>"

        # Build full HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @media only screen and (max-width: 600px) {{
            .container {{ padding: 10px !important; }}
            .card {{ margin-bottom: 20px !important; }}
        }}
    </style>
</head>
<body style='margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: #f3f4f6;'>

    <div class='container' style='max-width: 900px; margin: 0 auto; padding: 20px;'>

        <!-- Header with gradient -->
        <div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%); color: white; padding: 50px 30px; border-radius: 16px; margin-bottom: 30px; text-align: center; box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);'>
            <div style='font-size: 48px; margin-bottom: 10px;'>🎯</div>
            <h1 style='margin: 0 0 10px 0; font-size: 36px; font-weight: 800; letter-spacing: -0.5px;'>Tech Watch {digest_type} Digest</h1>
            <div style='font-size: 18px; opacity: 0.95; font-weight: 500;'>{'📚 Full Database Summary' if full_database else 'Video Popularity Project Edition'}</div>
            <div style='margin-top: 15px; padding: 8px 16px; background: rgba(255,255,255,0.2); border-radius: 20px; display: inline-block; font-size: 14px;'>
                📅 {today}
            </div>
        </div>

        <!-- Project Context Banner -->
        <div style='background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%); border: 2px solid #3b82f6; padding: 20px 24px; border-radius: 12px; margin-bottom: 30px;'>
            <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                <div style='font-size: 24px; margin-right: 12px;'>🎬</div>
                <h2 style='margin: 0; color: #1e40af; font-size: 18px; font-weight: 700;'>Context: Video Popularity Prediction</h2>
            </div>
            <p style='margin: 0; color: #1e3a8a; font-size: 14px; line-height: 1.6;'>
                Multimodal project (vision, audio, text) to predict video popularity on TikTok/Instagram and explain success factors.
            </p>
        </div>

        <!-- Summary Section -->
        <div style='background: white; padding: 28px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <div style='width: 4px; height: 24px; background: linear-gradient(180deg, #f59e0b 0%, #eab308 100%); border-radius: 2px; margin-right: 12px;'></div>
                <h2 style='margin: 0; color: #111827; font-size: 22px; font-weight: 700;'>📊 Summary by Theme</h2>
            </div>
            <div style='color: #374151; font-size: 15px;'>
{self._generate_theme_summary(new_docs[:max_articles])}
            </div>
        </div>

        <!-- Stats Grid -->
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 30px;'>
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                <div style='font-size: 14px; font-weight: 600; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;'>{'Articles in Digest' if full_database else f'New {digest_type}'}</div>
                <div style='font-size: 36px; font-weight: 800;'>{len(new_docs)}</div>
                <div style='font-size: 13px; opacity: 0.8; margin-top: 4px;'>articles</div>
            </div>
            <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                <div style='font-size: 14px; font-weight: 600; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;'>Total Database</div>
                <div style='font-size: 36px; font-weight: 800;'>{stats.get("total_documents", 0)}</div>
                <div style='font-size: 13px; opacity: 0.8; margin-top: 4px;'>{stats.get("total_chunks", 0)} chunks</div>
            </div>
        </div>

        <!-- Articles Section -->
        <div style='margin-bottom: 30px;'>
            <div style='display: flex; align-items: center; margin-bottom: 24px;'>
                <div style='width: 5px; height: 32px; background: linear-gradient(180deg, #6366f1 0%, #8b5cf6 100%); border-radius: 3px; margin-right: 14px;'></div>
                <h2 style='margin: 0; color: #111827; font-size: 26px; font-weight: 800;'>📚 {'All Articles' if full_database else 'New Articles'}</h2>
            </div>

            {docs_html if new_docs else "<div style='background: white; padding: 40px; border-radius: 12px; text-align: center; color: #6b7280; font-style: italic;'>No documents available.</div>"}
        </div>

        {self._format_competitor_section(competitor_docs) if competitor_docs else ''}

        <!-- Footer -->
        <div style='background: white; border-radius: 12px; padding: 24px; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);'>
            <div style='color: #6b7280; font-size: 14px; margin-bottom: 12px;'>
                🤖 Généré automatiquement par <strong style='color: #111827;'>Tech Watch Agent</strong>
            </div>
            <div style='color: #9ca3af; font-size: 12px;'>
                Powered by Ollama (Mistral) + ChromaDB + LangChain
            </div>
        </div>

        <div style='height: 40px;'></div>

    </div>

</body>
</html>
        """

        return html

    def send_digest(
        self,
        to_email: str,
        new_docs: List[Dict[str, Any]],
        summary: str,
        stats: Dict[str, Any],
        digest_type: str = "Daily",
        full_database: bool = False,
        max_articles: int = 15,
        competitor_docs: List[Dict[str, Any]] = None,
    ) -> bool:
        """
        Send digest email (daily/weekly, new docs or full database).

        Args:
            to_email: Recipient email address
            new_docs: List of documents (new or full database)
            summary: AI-generated summary
            stats: Database statistics
            digest_type: "Daily" or "Weekly"
            full_database: If True, digest contains entire database
            max_articles: Maximum number of article cards to show in email
            competitor_docs: List of competitor news (optional, always shown)

        Returns:
            True if sent successfully, False otherwise
        """
        if competitor_docs is None:
            competitor_docs = []
        try:
            # Determine subject line
            if full_database:
                subject = f"Tech Watch - Full Database Summary ({len(new_docs)} docs) - {datetime.now().strftime('%d/%m/%Y')}"
            else:
                subject = f"Tech Watch {digest_type} Digest - {datetime.now().strftime('%d/%m/%Y')} - {len(new_docs)} documents"

            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email

            # Create HTML content
            html_content = self._format_html_digest(new_docs, summary, stats, digest_type, full_database, max_articles, competitor_docs)

            # Create plain text fallback
            doc_label = "Full database" if full_database else "New documents"
            text_content = f"""
Tech Watch {digest_type} Digest - {datetime.now().strftime('%d/%m/%Y')}

SUMMARY
=======
{summary}

STATISTICS
==========
{doc_label}: {len(new_docs)}
Total in database: {stats.get('total_documents', 0)} documents

NEW CONTENT
===========
"""
            for doc in new_docs[:20]:  # Limit to 20 in plain text
                text_content += f"\n• {doc.get('title', 'Sans titre')}\n"
                text_content += f"  Source: {doc.get('source', 'unknown')} | {doc.get('published_date', '')}\n"
                text_content += f"  {doc.get('url', '')}\n"

            # Attach parts
            part1 = MIMEText(text_content, "plain", "utf-8")
            part2 = MIMEText(html_content, "html", "utf-8")
            msg.attach(part1)
            msg.attach(part2)

            # Send email
            console.print(f"[cyan]Connecting to {self.smtp_host}:{self.smtp_port}...[/cyan]")

            if self.use_tls:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)

            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()

            console.print(f"[green]✓ Email sent successfully to {to_email}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Error sending email: {e}[/red]")
            return False

    def test_connection(self) -> bool:
        """
        Test SMTP connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            console.print(f"[cyan]Testing SMTP connection to {self.smtp_host}:{self.smtp_port}...[/cyan]")

            if self.use_tls:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=10)

            server.login(self.smtp_user, self.smtp_password)
            server.quit()

            console.print(f"[green]✓ SMTP connection successful![/green]")
            return True

        except Exception as e:
            console.print(f"[red]✗ SMTP connection failed: {e}[/red]")
            return False
