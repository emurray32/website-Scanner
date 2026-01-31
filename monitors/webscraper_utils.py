"""
WebScraper Utility Functions - Tier calculation and expansion signal detection.
"""
from typing import Tuple, Dict, Any, List

TIER_CONFIG = {
      1: {'name': 'Global Leader', 'description': 'Mature global presence (10+ locales)', 'color': '#10b981'},
      2: {'name': 'Active Expansion', 'description': 'Already global, actively expanding', 'color': '#3b82f6'},
      3: {'name': 'Going Global', 'description': 'First-time global expansion', 'color': '#f59e0b'},
      4: {'name': 'Not Yet Global', 'description': 'No localization signals detected', 'color': '#6b7280'}
}

def detect_expansion_signals(website_data):
      signals = {'is_first_time_global': False, 'is_actively_expanding': False, 'expansion_signals': [], 'expansion_score': 0}
      if not website_data:
                return signals
            hreflang_tags = website_data.get('hreflang_tags', [])
    locale_count = len(hreflang_tags) if hreflang_tags else 0
    if locale_count >= 3:
              signals['is_actively_expanding'] = True
              signals['expansion_score'] += 20
elif locale_count >= 1:
        signals['is_first_time_global'] = True
        signals['expansion_score'] += 15
    return signals

def calculate_webscraper_tier(scan_results):
      if not scan_results:
                return (4, 'Not Yet Global')
            locale_count = scan_results.get('locale_count', 0) or 0
    hreflang_tags = scan_results.get('hreflang_tags', []) or []
    detected_count = max(locale_count, len(hreflang_tags))
    if detected_count >= 10:
              return (1, 'Global Leader')
          if detected_count >= 3:
                    return (2, 'Active Expansion')
                if detected_count >= 1:
                          return (3, 'Going Global')
                      return (4, 'Not Yet Global')

def extract_tier_from_scan_results(scan_results):
      tier, tier_label = calculate_webscraper_tier(scan_results)
    return {'tier': tier, 'tier_label': tier_label, 'locale_count': scan_results.get('locale_count', 0) or 0}

def generate_evidence_summary(scan_results, expansion_signals):
      evidence = []
    locale_count = scan_results.get('locale_count', 0) or 0
    if locale_count > 0:
              evidence.append(f"{locale_count} locale(s) detected")
          hreflang_tags = scan_results.get('hreflang_tags', []) or []
    if hreflang_tags:
              evidence.append(f"{len(hreflang_tags)} hreflang tags")
          return " | ".join(evidence) if evidence else "No signals detected"
