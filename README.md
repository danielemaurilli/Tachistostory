# Tachistostory

[Italian version](README.it.md)

<p align="center">
  <img src="assets/logo/tachistostory_title.png" alt="Tachistostory title" width="360" />


Tachistostory is a tachistoscopic reading-training app designed to support reading fluency through brief visual exposure, controlled pacing, and rapid-but-accurate responses.
The idea also has a specific goal: presenting a verbal-comprehension text through tachistoscopic reading and then asking the child comprehension questions at the end.

## Screenshots

<p align="center">
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.30.12.png" alt="Tachistostory screenshot 1" width="360" />
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.30.22.png" alt="Tachistostory screenshot 2" width="360" />
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.30.24.png" alt="Tachistostory screenshot 3" width="360" />
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.30.38.png" alt="Tachistostory screenshot 4" width="360" />
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.30.57.png" alt="Tachistostory screenshot 5" width="360" />
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.31.13.png" alt="Tachistostory screenshot 6" width="360" />
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.31.40.png" alt="Tachistostory screenshot 7" width="360" />
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.31.58.png" alt="Tachistostory screenshot 8" width="360" />
  <img src="assets/screenshots/Screenshot%202026-03-01%20alle%2016.32.06.png" alt="Tachistostory screenshot 9" width="360" />
</p>

## Project Overview

Reading is built on repeated fixation-saccade cycles, not continuous eye movement.  
Tachistostory is based on the idea that training visual sampling efficiency, attention control, and short-term maintenance of verbal information can support fluency and decoding automaticity.

The app does **not** claim a guaranteed causal effect on reading outcomes.  
Its training logic is aligned with evidence from eye-movement, visual-attention-span, working-memory, and executive-function research.

## Core Functionalities

- Tachistoscopic presentation loop (word display + mask + next trial)
- Adjustable exposure speed through an in-game slider
- Support for `.txt` and `.docx` input files
- Session flow with participant handling and stimulus-file selection
- Pause/restart/manual navigation controls during presentation
- Structured session logging (word events, pause events)
- End-of-session export to CSV and JSON
- Basic pseudonymization workflow for participant IDs
- Comprehension-oriented learning structure: text reading followed by final child-focused comprehension questions

## Why This Design Makes Sense

- **Oculomotor efficiency:** better fixation/saccade management can support fluent reading.
- **Tachistoscopic constraint:** brief exposure encourages fast selection of relevant visual information.
- **Visual attention span:** training rapid extraction from letter/word strings targets a known fluency-related component.
- **Working memory engagement:** users must briefly retain what was shown to respond correctly.
- **Executive-attentive control:** the task also recruits inhibition, sustained focus, and monitoring under time pressure.

In short, Tachistostory combines visual-timing constraints with response demands to engage multiple mechanisms associated with reading fluency.

## Run Locally

```bash
pip install -r requirements.txt
python main.py
```

## Download

You can download Tachistostory directly from the **GitHub Releases** section, where all published versions are available.

## Research Basis (selected)

- Rayner, K. (1998). *Eye movements in reading and information processing: 20 years of research.* Psychological Bulletin, 124(3), 372-422. https://doi.org/10.1037/0033-2909.124.3.372
- Bosse, M.-L., Tainturier, M. J., & Valdois, S. (2007). *Developmental dyslexia: The visual attention span deficit hypothesis.* Cognition, 104(2), 198-230. https://doi.org/10.1016/j.cognition.2006.05.009
- Bosse, M.-L., & Valdois, S. (2009). *Influence of the visual attention span on child reading performance: A cross-sectional study.* Journal of Research in Reading, 32(2), 230-253. https://doi.org/10.1111/j.1467-9817.2008.01387.x
- Lobier, M., Zoubrinetzky, R., & Valdois, S. (2012). *The visual attention span deficit in dyslexia is visual and not verbal.* Cortex, 48(6), 768-773. https://doi.org/10.1016/j.cortex.2011.09.003
- Valdois, S. (2022). *The visual-attention span deficit in developmental dyslexia: Review of evidence for a visual-attention-based deficit.* Dyslexia, 28(4), 397-415. https://doi.org/10.1002/dys.1724
- Sinha, N., Arrington, C. N., Malins, J. G., Pugh, K. R., Frijters, J. C., & Morris, R. (2024). *The reading-attention relationship: Variations in working memory network activity during single word decoding in children with and without dyslexia.* Neuropsychologia, 195, 108821. https://doi.org/10.1016/j.neuropsychologia.2024.108821
- Smith-Spark, J. H., & Gordon, R. (2022). *Automaticity and executive abilities in developmental dyslexia: A theoretical review.* Brain Sciences, 12(4), 446. https://doi.org/10.3390/brainsci12040446
- Hautala, J., Hawelka, S., & Ronimus, M. (2024). *An eye movement study on the mechanisms of reading fluency development.* Cognitive Development, 69, 101395. https://doi.org/10.1016/j.cogdev.2023.101395

## Disclaimer

Tachistostory is a training tool and should be considered complementary to professional educational or clinical assessment/intervention pathways.
