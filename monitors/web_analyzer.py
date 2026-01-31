"""
WebScraper Module - Analyze websites for quality and localization readiness.
"""
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, Any, Optional, List
from config import Config

try:
      from google import genai
      GENAI_AVAILABLE = True
except ImportError:
      GENAI_AVAILABLE = False


def _get_grade(score: float) -> str:
      if score >= 90: return 'A+'
elif score >= 80: return 'A'
elif score >= 70: return 'B'
elif score >= 60: return 'C'
elif score >= 50: return 'D'
else: return 'F'


class LocalizationScorer:
      @staticmethod
      def calculate_score(soup, url, links, html_content):
                score = 0
                details = {}

        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
                      score += 10
                      details['html_lang'] = html_tag.get('lang')

        hreflang_tags = soup.find_all('link', attrs={'hreflang': True})
        if len(hreflang_tags) > 1:
                      score += 20
                  details['hreflang_count'] = len(hreflang_tags)

        indicators = ['language', 'lang', 'locale', 'translate']
        has_switcher = any(ind in str(link).lower() for link in links for ind in indicators)
        if has_switcher:
                      score += 25
                  details['language_switcher'] = has_switcher

        i18n_libs = ['i18next', 'react-i18next', 'vue-i18n']
        found_libs = [lib for lib in i18n_libs if lib in html_content.lower()]
        if found_libs:
                      score += 15
                  details['i18n_libraries'] = found_libs

        return {
                      'score': min(score, 100),
                      'max_score': 100,
                      'grade': _get_grade(score),
                      'details': details,
                      'ready_for_localization': score < 30
        }


class WebAnalyzer:
      def __init__(self):
                self.headers = {'User-Agent': 'Mozilla/5.0 WebScraper/1.0'}
                self.timeout = 15

    def fetch_website(self, url):
              if not url.startswith(('http://', 'https://')):
                            url = 'https://' + url

              start_time = time.time()
              response = requests.get(url, headers=self.headers, timeout=self.timeout)
              response_time = time.time() - start_time
              response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else ''

        links = [{'href': a.get('href', ''), 'text': a.get_text(strip=True)} 
                                  for a in soup.find_all('a', href=True)[:100]]

        hreflang_tags = [{'hreflang': l.get('hreflang'), 'href': l.get('href', '')}
                                                 for l in soup.find_all('link', attrs={'hreflang': True})]

        localization_score = LocalizationScorer.calculate_score(soup, url, links, response.text)

        return {
                      'url': response.url,
                      'title': title_text,
                      'links': links,
                      'hreflang_tags': hreflang_tags,
                      'localization_score': localization_score,
                      'tech_stack': {'framework': None},
                      'quality_metrics': {'overall_score': 50}
        }

    def analyze_with_ai(self, website_data, prompt):
              if not GENAI_AVAILABLE:
                            raise Exception("Google AI not available")
                        if not Config.GEMINI_API_KEY:
                                      raise Exception("GEMINI_API_KEY not configured")

        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        analysis_prompt = f"Analyze this website: {website_data.get('url')}\n\nRequest: {prompt}"

        response = client.models.generate_content(
                      model=Config.GEMINI_MODEL,
                      contents=analysis_prompt
        )

        return {
                      'success': True,
                      'analysis': response.text,
                      'metadata': {'url': website_data.get('url'), 'title': website_data.get('title')}
        }

    def analyze_url(self, url, prompt=None):
              try:
                            website_data = self.fetch_website(url)

            if prompt:
                              result = self.analyze_with_ai(website_data, prompt)
                              result['localization_score'] = website_data['localization_score']
                              return result
else:
                return {
                                      'success': True,
                                      'url': website_data['url'],
                                      'title': website_data['title'],
                                      'localization_score': website_data['localization_score'],
                                      'tech_stack': website_data['tech_stack'],
                                      'metadata': {'url': website_data['url']}
                }
except Exception as e:
            return {'success': False, 'error': str(e)}


def analyze_website(url, prompt):
      return WebAnalyzer().analyze_url(url, prompt)


def analyze_website_technical(url):
      return WebAnalyzer().analyze_url(url, prompt=None)
