"""
Website Scanner - Website Localization Analysis Tool

A Flask application for analyzing websites for localization signals and quality gaps.
Extracted from the Lead Machine / GitHub Dossier project.
"""
import os
from flask import Flask, render_template, request, jsonify
from monitors.web_analyzer import analyze_website, analyze_website_technical
from monitors.webscraper_utils import (
    detect_expansion_signals, calculate_webscraper_tier, extract_tier_from_scan_results,
    generate_evidence_summary, TIER_CONFIG
)

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')


# ============================================================
# MAIN ROUTES
# ============================================================

@app.route('/')
def index():
      """Homepage - redirect to analyzer."""
      return render_template('webscraper.html')


@app.route('/analyzer')
def analyzer():
      """Analyzer page - analyze websites using natural language prompts."""
      return render_template('webscraper.html')


@app.route('/accounts')
def accounts():
      """Accounts page - manage and scan multiple websites."""
      return render_template('webscraper_accounts.html')


# ============================================================
# API ROUTES
# ============================================================

@app.route('/api/webscraper/analyze', methods=['POST'])
def api_webscraper_analyze():
      """
          Analyze a website using a natural language prompt.

              Request JSON:
                      url: Website URL to analyze (required)
                              prompt: Natural language prompt describing what to analyze (required)

                                  Returns JSON with analysis results.
                                      """
      try:
                data = request.get_json()

          if not data:
                        return jsonify({'error': 'Invalid JSON payload'}), 400

        url = data.get('url', '').strip()
        prompt = data.get('prompt', '').strip()

        if not url:
                      return jsonify({'error': 'Missing required field: url'}), 400

        if not prompt:
                      return jsonify({'error': 'Missing required field: prompt'}), 400

        # Analyze the website
        result = analyze_website(url, prompt)

        if not result.get('success'):
                      error_msg = result.get('error', 'Analysis failed')
                      return jsonify({'error': error_msg}), 500

        return jsonify(result), 200

except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/webscraper/analyze-technical', methods=['POST'])
def api_webscraper_analyze_technical():
      """
          Analyze a website for technical metrics only (no AI prompt).

              Request JSON:
                      url: Website URL to analyze (required)

                          Returns JSON with technical analysis results.
                              """
    try:
              data = request.get_json()

        if not data:
                      return jsonify({'error': 'Invalid JSON payload'}), 400

        url = data.get('url', '').strip()

        if not url:
                      return jsonify({'error': 'Missing required field: url'}), 400

        # Analyze the website (technical only)
        result = analyze_website_technical(url)

        if not result.get('success'):
                      error_msg = result.get('error', 'Analysis failed')
                      return jsonify({'error': error_msg}), 500

        return jsonify(result), 200

except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/webscraper/tier-config')
def api_tier_config():
      """Get the tier configuration."""
    return jsonify(TIER_CONFIG)


if __name__ == '__main__':
      port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
