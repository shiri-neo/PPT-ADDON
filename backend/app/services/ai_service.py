"""AI service for document analysis and presentation generation using OpenAI"""

import json
import os
import aiohttp
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from app.core.config import get_settings

settings = get_settings()


class AIService:
    """Service for AI-powered document analysis, content generation, and image creation"""

    def __init__(self):
        """Initialize OpenAI client"""
        api_key = settings.openai_api_key
        if not api_key or api_key.startswith("sk-placeholder"):
            print("⚠️  WARNING: OpenAI API key not configured! Using stub responses.")
            print("   Set OPENAI_API_KEY in backend/.env to enable AI features.")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=api_key)

    async def analyze_document(
        self,
        document_content: str,
        document_name: str,
        custom_instructions: Optional[str] = None,
    ) -> Dict[str, any]:
        """
        Analyze a document and extract key information for presentation creation using GPT-4.

        Args:
            document_content: The full text content of the document
            document_name: Name of the document
            custom_instructions: Optional user instructions for analysis

        Returns:
            Dictionary with extracted information (topics, key_points, summary, tone, estimated_slides)
        """
        if not self.client:
            return self._get_stub_analysis(document_name, custom_instructions)

        try:
            system_prompt = """You are an expert document analyst and presentation designer.
Your task is to analyze documents and extract structured information perfect for creating engaging presentations.
Always respond with valid JSON only."""

            user_prompt = f"""Analyze this document and extract information for creating a presentation.

Document Name: {document_name}

Content:
{document_content[:8000]}

Custom Instructions: {custom_instructions or 'None - use your best judgment'}

Return a JSON object with:
- main_topics: array of 5-8 main topics/sections
- key_points: object mapping each topic to array of 3-5 key points
- summary: one paragraph summary (2-3 sentences)
- suggested_tone: recommended tone (professional/casual/academic/marketing)
- estimated_slides: recommended number of slides (5-15)
- visual_themes: array of 3-5 visual themes/concepts for images (e.g., "innovation", "teamwork", "data analytics")

Make it engaging and tailored to the content!"""

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            analysis = json.loads(response.choices[0].message.content)
            print(f"✅ Document analyzed successfully with GPT-4")
            return analysis

        except Exception as e:
            print(f"❌ Error analyzing document with AI: {e}")
            return self._get_stub_analysis(document_name, custom_instructions)

    async def generate_presentation_structure(
        self,
        analysis: Dict[str, any],
        slide_count: int,
        tone: str,
        company_branding: Dict[str, str],
        custom_instructions: Optional[str] = None,
    ) -> List[Dict[str, any]]:
        """
        Generate a personalized presentation structure using GPT-4.

        Args:
            analysis: Output from analyze_document()
            slide_count: Desired number of slides
            tone: Presentation tone (formal, casual, marketing, academic)
            company_branding: Company branding preferences
            custom_instructions: User's specific instructions

        Returns:
            List of slide dictionaries with title, bullets, notes, design_hints, image_prompt
        """
        if not self.client:
            return self._get_stub_slides(analysis, slide_count, tone, company_branding, custom_instructions)

        try:
            system_prompt = """You are an expert presentation designer who creates engaging, visually stunning presentations.
You understand design principles, visual hierarchy, and how to make content compelling.
Always respond with valid JSON only."""

            user_prompt = f"""Create a {slide_count}-slide presentation structure with a {tone} tone.

Document Analysis:
{json.dumps(analysis, indent=2)}

Company Branding:
- Style: {company_branding.get('design_style', 'professional')}
- Primary Color: {company_branding.get('primary_color', '#0078D4')}
- Secondary Color: {company_branding.get('secondary_color', '#106EBE')}
- Accent Color: {company_branding.get('accent_color', '#00BCF2')}
- Font: {company_branding.get('font_family', 'Arial')}

Custom Instructions: {custom_instructions or 'None - create the best presentation possible'}

Create exactly {slide_count} slides. Return a JSON object with a "slides" array. Each slide must have:
- title: compelling slide title
- bullets: array of 3-5 concise bullet points (keep them short and impactful)
- notes: speaker notes with talking points
- design_hints: object with layout type, colors to use, and visual style suggestions
- image_prompt: detailed DALL-E prompt to generate a relevant, professional image for this slide (be specific and descriptive)
- image_style: style guidance (e.g., "modern flat design", "professional photography", "abstract illustration", "data visualization")

Make each slide visually distinct and engaging. Follow the custom instructions strictly if provided.
The image prompts should be detailed and specific to create beautiful, relevant visuals."""

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8  # Higher temperature for more creative designs
            )

            result = json.loads(response.choices[0].message.content)
            slides = result.get("slides", [])
            print(f"✅ Generated {len(slides)} personalized slides with GPT-4")
            return slides[:slide_count]

        except Exception as e:
            print(f"❌ Error generating presentation structure: {e}")
            return self._get_stub_slides(analysis, slide_count, tone, company_branding, custom_instructions)

    async def generate_slide_image(
        self,
        image_prompt: str,
        image_style: str = "professional",
        slide_title: str = ""
    ) -> Optional[str]:
        """
        Generate a custom image for a slide using DALL-E 3.

        Args:
            image_prompt: Detailed prompt for image generation
            image_style: Style guidance for the image
            slide_title: Title of the slide (for context)

        Returns:
            URL to the generated image, or None if generation fails
        """
        if not self.client:
            print("⚠️  DALL-E image generation skipped (no API key)")
            return None

        try:
            # Enhance the prompt with style guidance
            enhanced_prompt = f"""{image_style} style image: {image_prompt}.
Professional quality, suitable for a business presentation slide about '{slide_title}'.
Clean composition, no text overlay, high contrast for readability."""

            print(f"🎨 Generating image with DALL-E for: {slide_title[:50]}...")

            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt[:4000],  # DALL-E 3 has a 4000 char limit
                size="1792x1024",  # Wide format perfect for slides
                quality="standard",  # Use "hd" for higher quality but slower/more expensive
                n=1
            )

            image_url = response.data[0].url
            print(f"✅ Image generated successfully!")
            return image_url

        except Exception as e:
            print(f"❌ Error generating image with DALL-E: {e}")
            return None

    async def refine_slide_content(
        self,
        slide_content: Dict[str, any],
        instruction: str,
    ) -> Dict[str, any]:
        """
        Refine a single slide based on user instruction using GPT-4.

        Args:
            slide_content: Current slide content (title, bullets, notes)
            instruction: User's refinement instruction

        Returns:
            Updated slide content
        """
        if not self.client:
            return self._get_stub_refinement(slide_content, instruction)

        try:
            system_prompt = "You are an expert at refining presentation slides. Always respond with valid JSON only."

            user_prompt = f"""Current slide content:
{json.dumps(slide_content, indent=2)}

User instruction: {instruction}

Refine the slide according to the instruction. Return a JSON object with:
- title: updated slide title
- bullets: updated bullet points array
- notes: updated speaker notes
- design_hints: updated design guidance

Keep it concise and impactful. Follow the instruction precisely."""

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            refined = json.loads(response.choices[0].message.content)
            print(f"✅ Slide refined successfully")
            return refined

        except Exception as e:
            print(f"❌ Error refining slide: {e}")
            return self._get_stub_refinement(slide_content, instruction)

    # Stub responses for when OpenAI API is not configured
    def _get_stub_analysis(self, document_name: str, custom_instructions: Optional[str]) -> Dict:
        """Return stub analysis when API is not configured"""
        return {
            "main_topics": [
                "Introduction and Overview",
                "Core Concepts",
                "Key Findings",
                "Methodology",
                "Results and Analysis",
                "Recommendations",
                "Conclusion"
            ],
            "key_points": {
                "Introduction and Overview": [
                    "Context and background information",
                    "Purpose and objectives of the document",
                    "Scope and limitations"
                ],
                "Core Concepts": [
                    "Primary framework and theoretical foundation",
                    "Key definitions and terminology",
                    "Supporting models and approaches"
                ],
                "Key Findings": [
                    "Major discovery and breakthrough insights",
                    "Critical patterns and trends identified",
                    "Notable observations and data points"
                ]
            },
            "summary": f"Comprehensive analysis of {document_name} covering key concepts, findings, and actionable recommendations.",
            "suggested_tone": custom_instructions or "professional and informative",
            "estimated_slides": 8,
            "visual_themes": ["innovation", "analysis", "strategy", "growth", "collaboration"]
        }

    def _get_stub_slides(self, analysis: Dict, slide_count: int, tone: str,
                        company_branding: Dict, custom_instructions: Optional[str]) -> List[Dict]:
        """Return stub slides when API is not configured"""
        slides = []
        main_topics = analysis.get("main_topics", [])

        # Title slide
        slides.append({
            "title": main_topics[0] if main_topics else "Presentation Title",
            "bullets": [
                analysis.get("summary", "Document overview"),
                f"Tone: {tone}",
                custom_instructions or "AI-Generated Presentation"
            ],
            "notes": "Opening slide - introduce the topic",
            "design_hints": {"layout": "title", "use_logo": True},
            "image_prompt": "Modern professional business presentation cover image with abstract geometric shapes",
            "image_style": "modern corporate design"
        })

        # Content slides
        for topic in main_topics[1:slide_count-1]:
            slides.append({
                "title": topic,
                "bullets": [f"Key point about {topic}", f"Important detail", f"Supporting information"],
                "notes": f"Discuss {topic} in detail",
                "design_hints": {"layout": "content"},
                "image_prompt": f"Professional illustration representing {topic}",
                "image_style": "clean minimal design"
            })

        return slides[:slide_count]

    def _get_stub_refinement(self, slide_content: Dict, instruction: str) -> Dict:
        """Return stub refinement when API is not configured"""
        return {
            "title": f"{slide_content.get('title', 'Slide Title')} [Refined: {instruction[:30]}]",
            "bullets": [f"Updated: {b}" for b in slide_content.get("bullets", [])],
            "notes": f"{slide_content.get('notes', '')} - Applied: {instruction}"
        }


# Singleton instance
ai_service = AIService()
