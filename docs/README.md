# Documentation Assets

This directory contains documentation assets for the StoryCircuit project.

## Screenshots

### Available Files

1. **screenshot-ui.png** - Main application interface showing:
   - Topic input field with example "Intelligent multi-agent apps with Microsoft Foundry"
   - Platform checkboxes (LinkedIn, X/Twitter, GitHub, Blog)
   - Target Audience field: "Software developers"
   - Additional Context field: "Microsoft Foundry, Agent Framework, Azure"
   - Generate Content button

2. **screenshot-output.png** - Generated content display showing:
   - Platform-specific content with clean markdown formatting
   - Copy-to-clipboard buttons
   - Styled hashtags (blue pill-shaped badges)
   - Call-to-action section highlighted
   - Professional layout with proper spacing
   
   ⚠️ **To add:** Screenshot the actual content output from http://localhost:8001 after generating content

### Adding Screenshot for Content Output

To capture the output screenshot:

```bash
1. Run the application: http://localhost:8001
2. Generate content for "Intelligent multi-agent apps with Microsoft Foundry"
3. Take a screenshot of the displayed LinkedIn post
4. Save as: docs/screenshot-output.png
5. Commit: git add docs/screenshot-output.png && git commit -m "docs: Add content output screenshot"
6. Push: git push origin main
```

## Example Content

- **example-output.md** - Full example of generated content for "Intelligent multi-agent apps with Microsoft Foundry" topic

## Future Documentation

Additional documentation may include:
- Deployment guides
- API usage examples
- Video demos
