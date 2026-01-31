"""
Configuration settings for Website Scanner.
"""
import os


class Config:
      """Application configuration."""

    # API Keys
      GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

    # Gemini Model
      GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')

    # Request settings
      REQUEST_TIMEOUT = 15

    # Social multi-region detection patterns
      SOCIAL_MULTI_REGION_PATTERNS = {
          'regional_social_handles': [
              '_de', '_fr', '_es', '_it', '_jp', '_kr', '_br', '_mx',
              '_uk', '_au', '_ca', '_in', '_sg', '_nl', '_be', '_ch',
              'de_', 'fr_', 'es_', 'it_', 'jp_', 'kr_', 'br_', 'mx_',
              '-de', '-fr', '-es', '-it', '-jp', '-kr', '-br', '-mx',
              'germany', 'france', 'spain', 'italy', 'japan', 'korea',
              'brazil', 'mexico', 'india', 'australia', 'canada',
          ]
      }
