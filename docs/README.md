# Documentation Assets

This directory contains documentation assets for the StoryCircuit project.

## Screenshots

### Required Files

1. **screenshot-ui.png** - Main application interface showing:
   - Topic input field with example "Intelligent multi-agent apps with Microsoft Foundry"
   - Platform checkboxes (LinkedIn, Twitter, GitHub, Blog)
   - Target Audience field
   - Additional Context field
   - Generate Content button

2. **screenshot-output.png** - Generated content display showing:
   - Platform-specific content with clean markdown formatting
   - Copy-to-clipboard buttons
   - Styled hashtags (blue pill-shaped badges)
   - Call-to-action section
   - Professional layout

### Adding Screenshots

To add screenshots to this folder:

```bash
# Navigate to the docs directory
cd docs/

# Add your screenshot files
# (Use Windows File Explorer or copy command)
copy "path\to\your\screenshot-ui.png" .
copy "path\to\your\screenshot-output.png" .

# Commit and push
git add screenshot-ui.png screenshot-output.png
git commit -m "docs: Add application screenshots"
git push origin main
```

## Example Content

- **example-output.md** - Full example of generated content for "Intelligent multi-agent apps with Microsoft Foundry" topic

## Future Documentation

Additional documentation may include:
- Architecture diagrams
- Deployment guides
- API usage examples
- Video demos
