"""
Email service for sending digest reports.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Dict, Any
from datetime import datetime
from rich.console import Console

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
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.use_tls = use_tls

    def _generate_video_popularity_insight(self, doc: Dict[str, Any]) -> str:
        """
        Generate actionable Video Popularity project insights for a document.

        Args:
            doc: Document dictionary

        Returns:
            HTML insight text with actionable recommendations
        """
        title = doc.get("title", "").lower()
        abstract = doc.get("abstract", "").lower()
        source = doc.get("source", "unknown").lower()
        text = f"{title} {abstract}"

        insights = []

        # === MULTIMODAL / VISION-LANGUAGE ===
        if any(kw in text for kw in ["multimodal", "vision-language", "vlm", "video understanding", "video-llm"]):
            if "clip" in text or "align" in text:
                insights.append("📹 <strong>Levier:</strong> Utiliser l'alignement vision-texte (type CLIP) pour encoder simultanément frames vidéo + captions + hashtags")
                insights.append("💰 <strong>Bénéfice:</strong> Meilleure représentation sémantique → prédiction viralité +15-25%")
            elif "fusion" in text or "modality" in text:
                insights.append("📹 <strong>Levier:</strong> Implémenter une fusion tardive (late fusion) des features vision/audio/texte avec attention cross-modale")
                insights.append("💰 <strong>Bénéfice:</strong> Capture des interactions entre modalités → +10-20% performance sur vidéos complexes")
            else:
                insights.append("📹 <strong>Levier:</strong> Intégrer ce modèle multimodal pour extraire des features denses (embeddings) des vidéos TikTok/Instagram")
                insights.append("💰 <strong>Bénéfice:</strong> Représentation riche du contenu → amélioration F1-score prédiction")

        # === EXPLAINABILITY ===
        if any(kw in text for kw in ["explainability", "xai", "interpretability", "shap", "lime", "attention"]):
            if "shap" in text:
                insights.append("🔍 <strong>Levier:</strong> Appliquer SHAP values pour identifier quels features (durée vidéo, #hashtags, musique) contribuent le plus à la viralité")
                insights.append("💰 <strong>Bénéfice:</strong> Dashboard créateurs montrant facteurs de succès → + engagement utilisateurs")
            elif "attention" in text or "saliency" in text:
                insights.append("🔍 <strong>Levier:</strong> Visualiser les attention maps pour montrer quelles parties de la vidéo (frames, régions) captent l'engagement")
                insights.append("💰 <strong>Bénéfice:</strong> Insights actionnables pour créateurs → optimisation thumbnails/hooks")
            else:
                insights.append("🔍 <strong>Levier:</strong> Ajouter une couche d'explication des prédictions avec importance des features")
                insights.append("💰 <strong>Bénéfice:</strong> Transparence → confiance utilisateurs + itérations produit rapides")

        # === ENGAGEMENT / RECOMMENDATION ===
        if any(kw in text for kw in ["engagement", "popularity", "viral", "recommendation", "ranking"]):
            if "tiktok" in text or "instagram" in text or "reels" in text:
                insights.append("📊 <strong>Levier:</strong> Benchmarker leur métrique d'engagement (watch time, shares, comments weight) pour calibrer notre scoring")
                insights.append("💰 <strong>Bénéfice:</strong> Alignement avec algos TikTok/Instagram → prédictions réalistes marché")
            elif "cold start" in text or "new user" in text:
                insights.append("📊 <strong>Levier:</strong> Implémenter leur stratégie cold-start pour prédire viralité de créateurs avec peu d'historique")
                insights.append("💰 <strong>Bénéfice:</strong> Couverture 100% créateurs (nouveaux inclus) → + valeur produit")
            elif "ranking" in text or "scoring" in text:
                insights.append("📊 <strong>Levier:</strong> Adapter leur fonction de ranking (probabilistic model) pour scorer vidéos par potentiel viral")
                insights.append("💰 <strong>Bénéfice:</strong> Priorisation contenu high-potential → optimisation créateurs")
            else:
                insights.append("📊 <strong>Levier:</strong> Intégrer ces métriques d'engagement dans notre feature engineering (CTR, completion rate, share velocity)")
                insights.append("💰 <strong>Bénéfice:</strong> Features comportementales → +10-15% recall sur vidéos virales")

        # === VIDEO/AUDIO FEATURES ===
        if any(kw in text for kw in ["scene detection", "shot boundary", "temporal", "video features", "audio features"]):
            if "scene" in text or "shot" in text:
                insights.append("🎬 <strong>Levier:</strong> Détecter les transitions/cuts pour calculer 'editing pace' (rythme montage) comme feature de viralité")
                insights.append("💰 <strong>Bénéfice:</strong> Vidéos dynamiques (>5 cuts/sec) = +30% viralité TikTok → feature exploitable")
            elif "audio" in text or "sound" in text or "music" in text:
                insights.append("🎬 <strong>Levier:</strong> Extraire features audio (BPM, genre, trending sounds) pour prédire l'accroche musicale")
                insights.append("💰 <strong>Bénéfice:</strong> Trending sounds = x2-x5 viralité → recommandation automatique aux créateurs")
            elif "temporal" in text:
                insights.append("🎬 <strong>Levier:</strong> Modéliser l'évolution temporelle (LSTM/Transformer) pour capter les patterns d'engagement au fil de la vidéo")
                insights.append("💰 <strong>Bénéfice:</strong> Prédiction drop-off → suggestions optimisation durée/hook")
            else:
                insights.append("🎬 <strong>Levier:</strong> Enrichir le feature set avec ces descripteurs vidéo bas-niveau (color, motion, shot length)")
                insights.append("💰 <strong>Bénéfice:</strong> Couverture complète du contenu → meilleure généralisation modèle")

        # === CROSS-PLATFORM / TRANSFER LEARNING ===
        if any(kw in text for kw in ["cross-platform", "transfer learning", "domain adaptation", "multi-domain"]):
            insights.append("🔄 <strong>Levier:</strong> Utiliser transfer learning TikTok→Instagram (ou inverse) pour mutualiser les apprentissages entre plateformes")
            insights.append("💰 <strong>Bénéfice:</strong> Réduction data requirements -50% + prédictions cross-platform → 2 marchés avec 1 modèle")

        # === TRANSFORMERS / ARCHITECTURES ===
        if any(kw in text for kw in ["transformer", "bert", "vit", "clip"]) and not any(ins for ins in insights if "clip" in ins.lower()):
            if "vit" in text or "vision transformer" in text:
                insights.append("⚡ <strong>Levier:</strong> Remplacer CNN par Vision Transformer (ViT) pour encoder frames → meilleure capture patterns visuels complexes")
                insights.append("💰 <strong>Bénéfice:</strong> +5-10% accuracy sur vidéos esthétiques (makeup, food, travel)")
            else:
                insights.append("⚡ <strong>Levier:</strong> Implémenter une architecture transformer pour fusionner séquences (frames + audio + metadata)")
                insights.append("💰 <strong>Bénéfice:</strong> Capture dépendances long-terme → meilleure prédiction vidéos >30sec")

        # === SOURCE-BASED FALLBACKS (more actionable) ===
        if not insights:
            if "arxiv" in source:
                # Try to extract more from title
                if "survey" in title or "review" in title:
                    insights.append("📚 <strong>Levier:</strong> Utiliser ce survey pour identifier les SOTA techniques à benchmarker contre notre baseline")
                    insights.append("💰 <strong>Bénéfice:</strong> Roadmap technique validée académiquement → réduction risque R&D")
                elif "dataset" in title:
                    insights.append("📚 <strong>Levier:</strong> Évaluer ce dataset pour enrichir nos données d'entraînement (+ diversité)")
                    insights.append("💰 <strong>Bénéfice:</strong> + robustesse modèle sur edge cases → -15% false positives")
                else:
                    insights.append("📚 <strong>Levier:</strong> Lire pour identifier techniques/architectures à tester dans notre stack ML")
                    insights.append("💰 <strong>Bénéfice:</strong> Veille académique → innovation continue produit")

            elif any(s in source for s in ["netflix", "meta", "google", "youtube", "tiktok", "instagram"]):
                insights.append("🏢 <strong>Levier:</strong> Reverse-engineer leurs pratiques ML (features, métriques, architectures) pour notre système")
                insights.append("💰 <strong>Bénéfice:</strong> Alignment avec standards industrie → crédibilité auprès créateurs")

            elif any(s in source for s in ["vidiq", "tubebuddy"]):
                insights.append("🎯 <strong>Levier:</strong> Analyser leurs features produit pour identifier gaps dans notre offre (ex: A/B testing thumbnails)")
                insights.append("💰 <strong>Bénéfice:</strong> Parité concurrentielle → réduction churn utilisateurs")

            else:
                # Last resort - still make it somewhat actionable
                insights.append("💡 <strong>Levier:</strong> Extraire insights techniques/pratiques transférables à notre contexte vidéo")
                insights.append("💰 <strong>Bénéfice:</strong> Accumulation de connaissances domaine → décisions produit éclairées")

        return "<br>".join(insights)

    def _format_competitor_section(self, competitor_docs: List[Dict[str, Any]]) -> str:
        """
        Format competitor news section HTML.

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

        # Build competitor cards
        competitor_html = ""
        for competitor_name, docs in competitors_grouped.items():
            # Take only most recent 4-5 posts
            recent_docs = sorted(
                docs,
                key=lambda x: x.get("published_date", "1970-01-01"),
                reverse=True
            )[:5]

            competitor_html += f"""
            <div style='background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 6px solid #ef4444;'>
                <h3 style='margin: 0 0 16px 0; color: #111827; font-size: 20px; font-weight: 700;'>
                    🎯 {competitor_name}
                </h3>
            """

            for doc in recent_docs:
                title = doc.get("title", "Sans titre")
                url = doc.get("url", "#")
                date = doc.get("published_date", "")
                # Use LLM-generated summary or fallback
                summary = doc.get("llm_summary") or doc.get("abstract", "")
                if summary and len(summary) > 200:
                    summary = summary[:200] + "..."

                competitor_html += f"""
                <div style='padding: 12px 0; border-bottom: 1px solid #e5e7eb;'>
                    <div style='margin-bottom: 4px;'>
                        <a href='{url}' style='color: #1f2937; text-decoration: none; font-weight: 600; font-size: 15px;' target='_blank'>{title}</a>
                    </div>
                    <div style='color: #6b7280; font-size: 13px; margin-bottom: 6px;'>
                        📅 {date}
                    </div>
                    {f"<div style='color: #4b5563; font-size: 14px; line-height: 1.5;'>{summary}</div>" if summary else ""}
                </div>
                """

            competitor_html += "</div>"

        # Wrap in section
        section_html = f"""
        <!-- Competitor News Section -->
        <div style='margin-bottom: 30px;'>
            <div style='display: flex; align-items: center; margin-bottom: 24px;'>
                <div style='width: 5px; height: 32px; background: linear-gradient(180deg, #ef4444 0%, #dc2626 100%); border-radius: 3px; margin-right: 14px;'></div>
                <h2 style='margin: 0; color: #111827; font-size: 26px; font-weight: 800;'>🚨 Competitor News</h2>
            </div>
            <div style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border: 2px solid #ef4444; padding: 16px; border-radius: 12px; margin-bottom: 20px;'>
                <div style='color: #991b1b; font-size: 14px; font-weight: 600;'>
                    📊 Dernières nouvelles des {len(competitors_grouped)} competitors directs (VidIQ, TubeBuddy, Aggero, Syllaby, Adverteyes, VidMob)
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

        for i, doc in enumerate(new_docs[:max_articles]):  # Limit articles
            title = doc.get("title", "Sans titre")
            url = doc.get("url", "#")

            # Use LLM-generated summary (preferred) or fallback to abstract
            summary = doc.get("llm_summary") or doc.get("abstract", "")

            # Truncate if too long
            if len(summary) > 350:
                summary = summary[:350] + "..."

            # If still empty, provide a minimal fallback
            if not summary or summary == "No summary available" or summary == "Résumé non disponible":
                summary = "Résumé non disponible. <a href='" + url + "' target='_blank'>Lire l'article complet →</a>"

            date = doc.get("published_date", "")
            source = doc.get("source", "unknown").replace('_', ' ').title()

            # Generate Video Popularity insight
            vp_insight = self._generate_video_popularity_insight(doc)

            # Alternating colors for visual variety
            border_colors = ["#8b5cf6", "#ec4899", "#f59e0b", "#10b981", "#3b82f6", "#ef4444"]
            border_color = border_colors[i % len(border_colors)]

            docs_html += f"""
            <div style='margin-bottom: 30px; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 6px solid {border_color};'>
                <!-- Card Header -->
                <div style='background: linear-gradient(135deg, {border_color}15 0%, {border_color}05 100%); padding: 20px 24px; border-bottom: 1px solid #e5e7eb;'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
                        <div style='background: {border_color}; color: white; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 600; text-transform: uppercase;'>
                            {source}
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
                            📄 Résumé
                        </div>
                        <div style='color: #4b5563; font-size: 15px; line-height: 1.7;'>
                            {summary}
                        </div>
                    </div>

                    <!-- Video Popularity Insight Box -->
                    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px;'>
                        <div style='font-weight: 700; color: #92400e; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;'>
                            🎯 Pour Le Projet Video Popularity
                        </div>
                        <div style='color: #78350f; font-size: 14px; line-height: 1.6;'>
                            {vp_insight}
                        </div>
                    </div>
                </div>
            </div>
            """

        if len(new_docs) > max_articles:
            docs_html += f"<div style='color: #6b7280; font-style: italic; text-align: center; padding: 20px; background: #f9fafb; border-radius: 8px;'>... et {len(new_docs) - max_articles} autres articles disponibles dans la base de données</div>"

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
                <h2 style='margin: 0; color: #1e40af; font-size: 18px; font-weight: 700;'>Contexte: Prédiction de Popularité Vidéo</h2>
            </div>
            <p style='margin: 0; color: #1e3a8a; font-size: 14px; line-height: 1.6;'>
                Projet multimodal (vision, audio, texte) pour prédire la popularité de vidéos sur TikTok/Instagram et expliquer les facteurs de succès.
            </p>
        </div>

        <!-- Summary Section -->
        <div style='background: white; padding: 28px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);'>
            <div style='display: flex; align-items: center; margin-bottom: 16px;'>
                <div style='width: 4px; height: 24px; background: linear-gradient(180deg, #f59e0b 0%, #eab308 100%); border-radius: 2px; margin-right: 12px;'></div>
                <h2 style='margin: 0; color: #111827; font-size: 22px; font-weight: 700;'>📊 Résumé de la Veille</h2>
            </div>
            <div style='color: #374151; line-height: 1.8; font-size: 15px; white-space: pre-line;'>
{summary}
            </div>
        </div>

        <!-- Stats Grid -->
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 30px;'>
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                <div style='font-size: 14px; font-weight: 600; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;'>{'Articles dans ce Digest' if full_database else f'Nouveaux {digest_type}'}</div>
                <div style='font-size: 36px; font-weight: 800;'>{len(new_docs)}</div>
                <div style='font-size: 13px; opacity: 0.8; margin-top: 4px;'>articles</div>
            </div>
            <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                <div style='font-size: 14px; font-weight: 600; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;'>Base Totale</div>
                <div style='font-size: 36px; font-weight: 800;'>{stats.get("total_documents", 0)}</div>
                <div style='font-size: 13px; opacity: 0.8; margin-top: 4px;'>{stats.get("total_chunks", 0)} chunks</div>
            </div>
        </div>

        <!-- Articles Section -->
        <div style='margin-bottom: 30px;'>
            <div style='display: flex; align-items: center; margin-bottom: 24px;'>
                <div style='width: 5px; height: 32px; background: linear-gradient(180deg, #6366f1 0%, #8b5cf6 100%); border-radius: 3px; margin-right: 14px;'></div>
                <h2 style='margin: 0; color: #111827; font-size: 26px; font-weight: 800;'>📚 {'Tous les Articles' if full_database else 'Nouveaux Articles'}</h2>
            </div>

            {docs_html if new_docs else "<div style='background: white; padding: 40px; border-radius: 12px; text-align: center; color: #6b7280; font-style: italic;'>Aucun document disponible.</div>"}
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

RÉSUMÉ
======
{summary}

STATISTIQUES
============
{doc_label}: {len(new_docs)}
Total en base : {stats.get('total_documents', 0)} documents

NOUVEAUX CONTENUS
=================
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
