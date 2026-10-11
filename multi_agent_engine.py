name: GCC Investment Engine Automation

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  run-engine:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run Engine Script
        env:
          EMAIL_USER: ${{ secrets.EMAIL_USER }}
          EMAIL_PASS: ${{ secrets.EMAIL_PASS }}
        run: |
          python multi_agent_engine.py

      - name: Commit and Push Updated Sent Log
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add sent_opportunities.json
          git commit -m "Auto-update sent opportunities history [skip ci]" || echo "No changes to commit"
          git push
