# Tachistostory

![License: Custom Non-Commercial](https://img.shields.io/badge/License-Custom_Non--Commercial-blue.svg)
![Clinical Use: Allowed](https://img.shields.io/badge/Clinical_Use-Allowed-green.svg)
![Version](https://img.shields.io/badge/version-0.9.0-orange.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

> Tachistoscopic application for enhancing reading skills through saccadic eye movement training

[🇮🇹 Italiano](README.md) | [🇬🇧 English](README_EN.md)

## 📋 Description

**Tachistostory** is an innovative clinical-educational tool designed to enhance children's reading skills through tachistoscopic technique. The application is based on solid neuroscientific principles regarding saccadic eye movements during reading.

- Presenting words or short strings for very brief intervals (100–250 ms) in controlled screen positions trains the visual-attentional systems that support saccades and fixations during reading (Bakker & Vinke, 1985; Lorusso et al., 2005).
- This type of training, both in clinical format (VHSS, Tachidino) and in game format (Tachistoscope), is associated with significant improvements in reading speed and accuracy in children with dyslexia and is maintained over time (Lorusso et al., 2022; Piazzalunga et al., 2023; McHolm, 2023).
- In individuals with ADHD, reading modalities that reduce or eliminate eye movements (e.g., RSVP) improve text comprehension compared to traditional reading, indicating that rapid and centered word presentation can compensate for part of the attentional difficulties (Moussaoui et al., 2023), and that tachistoscopic treatments for dyslexia remain effective even in the presence of ADHD (Lorusso et al., 2024).

An app like **Tachistostory**, which presents words for very brief intervals within a game/exercise structure, is therefore part of a tradition of *evidence-based* interventions: it leverages the same principles of tachistoscopic presentation and training of processing during fixations that have been documented as useful for improving reading fluency in dyslexia and, potentially, for supporting readers with ADHD.

---

**References**

Bakker, D. J., & Vinke, J. (1985). Effects of hemisphere-specific stimulation on brain activity and reading in dyslexics. *Journal of Clinical and Experimental Neuropsychology, 7*(5), 505–525. https://doi.org/10.1080/01688638508401282

Lorusso, M. L., Facoetti, A., Toraldo, A., & Molteni, M. (2005). Tachistoscopic treatment of dyslexia changes the distribution of visual–spatial attention. *Brain and Cognition, 57*(2), 135–142. https://doi.org/10.1016/j.bandc.2004.08.057

Lorusso, M. L., Borasio, F., & Molteni, M. (2022). Remote neuropsychological intervention for developmental dyslexia with the Tachidino platform: No reduction in effectiveness for older nor for more severely impaired children. *Children, 9*(1), 71. https://doi.org/10.3390/children9010071

Lorusso, M. L., Borasio, F., Mistò, P., Salandi, A., Travellini, S., Lotito, M., & Molteni, M. (2024). Remote treatment of developmental dyslexia: How ADHD comorbidity, clinical history and treatment repetition may affect its efficacy. *Frontiers in Public Health, 11*, 1135465. https://doi.org/10.3389/fpubh.2023.1135465

McHolm, S. (2023). *Exploring brain stimulation methods to improve reading in children with dyslexia: A systematic review*. SAERA – School of Advanced Education, Research and Accreditation.

Moussaoui, S., Siddiqi, A., Cheung, T. C. K., & Niemeier, M. (2023). Reading without eye movements: Improving reading comprehension in young adults with Attention-Deficit/Hyperactivity Disorder (ADHD) [Preprint]. OSF. https://doi.org/10.31234/osf.io/3d4ea

Piazzalunga, C., Dui, L. G., Fontolan, S., Franceschini, S., Bortolozzo, M., Termine, C., & Ferrante, S. (2023). Evaluating the efficacy of a serious game in enhancing word reading speed. In *Proceedings of the 17th European Conference on Games Based Learning*. https://doi.org/10.34190/ecgbl.17.1.1661

### Images
<img width="560" height="736" alt="Screenshot 2025-12-11 alle 16 48 39" src="https://github.com/user-attachments/assets/a1ec3bcf-fc98-4059-8f71-2a53306969ca" />
<img width="1698" height="937" alt="Screenshot 2025-12-11 alle 16 48 52" src="https://github.com/user-attachments/assets/32fafffc-301e-4e50-a601-28787ab84c6a" />
<img width="1624" height="918" alt="Screenshot 2025-12-11 alle 16 49 01" src="https://github.com/user-attachments/assets/a782e677-c18d-4c58-9f94-fe1496b28334" />

### How It Works

The tachistoscope presents single words for brief, controlled periods of time, training the visual system to process written information more efficiently. The training follows a gradual path:

- **Start**: Words are presented for **1200 ms** (comfortable time for struggling readers)
- **Progression**: With consistent exercise, exposure time is progressively reduced
- **Goal**: Reach **220-250 ms**, the natural time of a saccade during fluent reading according to scientific literature

### Clinical Objectives

1. **Reading speed enhancement**: Training of saccadic eye movements
2. **Text comprehension**: Comprehension questions after each sentence to verify processing
3. **Sustained and divided attention**: Maintaining focus during rapid presentation
4. **Working memory**: Word retention to reconstruct sentence meaning

## ✨ Key Features

- 📖 **Tachistoscopic presentation** of single words with configurable times (220-1200 ms)
- 🎯 **Post-stimulus masking** to prevent prolonged processing of retinal image
- 📝 **Content customization**: Load custom texts (`.txt`, `.doc`, `.docx`)
- 🎮 **Intuitive interface**: Simple controls suitable for use with children
- 📊 **Progress tracking**: Word-by-word advancement indicator
- 🖥️ **Fullscreen mode**: To eliminate visual distractions
- ⚙️ **Adjustment slider**: Real-time modification of exposure time

## 🎯 Target Audience

### Clinical Professionals
- **Psychologists and neuropsychologists** for cognitive training
- **Speech therapists** for reading rehabilitation
- **Educational psychologists** for educational interventions
- **Developmental neuropsychomotor therapists** for integrated interventions

### Usage Contexts
- Specific Learning Disorders (SLD - Dyslexia)
- Reading skill development delays
- Post-trauma or post-stroke rehabilitation (adults)
- Reading skill enhancement in typical readers

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- Pygame
- docx2txt

### Dependency Installation

```bash
# Clone the repository
git clone https://github.com/danielemaurilli/tachistostory.git

# Enter the directory
cd tachistostory

# Install dependencies
pip install -r requirements.txt
```

### requirements.txt File
```
pygame>=2.5.0
docx2txt>=0.8
```

## 💡 Usage

### Starting the Application

```bash
python main.py
```

### Material Preparation

1. **Prepare a text file** (`.txt`, `.doc`, or `.docx`) containing sentences to present
2. **Recommended format**: One sentence per line, with words separated by spaces
3. **Content example**:
   ```
   The cat sleeps on the sofa
   Maria plays ball in the park
   The sun shines in the blue sky
   ```

### Complete Clinical Workflow

1. **Loading**: Drag the file into the application window
2. **Configuration**: Adjust exposure time with slider (start from 1200 ms)
3. **Presentation**: Press ENTER to begin
4. **Reading**: Child reads each word that appears
5. **Reconstruction**: After complete sentence, ask child to reconstruct it
6. **Comprehension**: Ask questions about the read sentence (e.g., "Where was the cat sleeping?")
7. **Progression**: Gradually reduce exposure time in subsequent sessions

### Controls

| Key | Function |
|-----|----------|
| **ENTER** | Start presentation from instruction screen |
| **SPACE** | Move to next word (after mask) |
| **P** | Pause / Resume |
| **R** | Restart from first word |
| **F** | Toggle fullscreen |
| **I** | Minimize window |
| **Slider** | Adjust exposure time (220-1200 ms) |

## 🔬 Scientific Foundation

### Saccadic Movements in Reading

During fluent reading, eyes perform rapid movements called **saccades** lasting about **20-40 ms**, followed by fixations of **200-250 ms** during which the brain processes information. Tachistostory trains this natural process.

### Trained Cognitive Components

1. **Rapid visual processing**: Immediate word recognition
2. **Working memory**: Maintaining words in memory to reconstruct sentence
3. **Sustained attention**: Maintaining focus during presentation
4. **Divided attention**: Simultaneous management of reading and comprehension
5. **Sequential integration**: Meaning reconstruction from word sequence

## 📖 Clinical Session Example

### Setting
- Duration: 20-30 minutes
- Frequency: 2-3 times per week
- Environment: Quiet, with adequate lighting

### Protocol
1. **Warm-up** (5 min): Comfortable exposure time (e.g., 800 ms)
2. **Training** (10 min): Session target time
3. **Cool-down** (5 min): Comprehension questions and feedback
4. **Recording**: Note time used, number of sentences, errors, perceived fatigue

### Comprehension Questions (Examples)

For sentence: *"The cat sleeps on the sofa"*

- **Literal**: "Who sleeps?" "Where does the cat sleep?"
- **Inferential**: "Do you think it's day or night?" "Is the cat tired?"
- **Memory**: "How many words did the sentence have?" "What was the third word?"

## 🎨 Customization

### Content Suggestions

- Start with short words (3-5 letters)
- Use simple sentences (subject-verb-complement)
- Avoid complex syntactic structures initially
- Gradually increase complexity

## 📊 Progress Monitoring

### Progression Criteria
Reduce exposure time when the child:
- Correctly reads at least 80% of words
- Correctly reconstructs sentences
- Correctly answers comprehension questions
- Does not show excessive fatigue

## 📜 License

This project is released under a **Custom Non-Commercial License**.

### ✅ PERMITTED USE

- **Clinical use**: Free use by psychologists, speech therapists, therapists as a professional support tool
- **Educational use**: Use in educational, university, research contexts
- **Personal use**: Study, learning, experimentation
- **Collaboration**: Fork, modifications and contributions via GitHub

### ❌ PROHIBITED USE

- Sale of software or inclusion in commercial products
- Distribution as paid service (SaaS, apps)
- Redistribution outside GitHub

📋 **Full details**: [LICENSE_EN.md](LICENSE_EN.md)  
❓ **Frequently asked questions**: [FAQ_EN.md](FAQ_EN.md)

### 💼 Commercial License

Are you a company or institution interested in commercial use? [Contact me](mailto:maurillidaniele@gmail.com) to discuss a dedicated license.

## 🤝 Contributing

Contributions are welcome! This project is open to collaboration from the clinical and development community.

### How to Contribute

1. Fork the project
2. Create a branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add: new feature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

**💼 Showcase your contribution**: Contributors can include their contributions in CV, portfolio or LinkedIn!

Read [CONTRIBUTING_EN.md](CONTRIBUTING_EN.md) for more details.

## 🐛 Bug Reporting

Found a bug? [Open an issue](https://github.com/danielemaurilli/tachistostory/issues) describing:
- What you did
- What you expected
- What actually happened
- Operating system and Python version
- Screenshots (if relevant)

## 📚 Citation

If you use Tachistostory in a clinical or research context, cite it as:

```
Maurilli, D. (2025). Tachistostory: Tachistoscopic application for 
reading skills enhancement [Software]. 
GitHub: https://github.com/danielemaurilli/tachistostory
License: Custom Non-Commercial Clinical License
```

**BibTeX**:
```bibtex
@software{maurilli2025tachistostory,
  author = {Maurilli, Daniele},
  title = {Tachistostory: Tachistoscopic application for reading skills enhancement},
  year = {2025},
  url = {https://github.com/danielemaurilli/tachistostory},
  note = {License: Custom Non-Commercial Clinical License}
}
```

## 👤 Author

**Daniele Maurilli**

- 📧 Email: maurillidaniele@gmail.com
- 💼 GitHub: [@danielemaurilli](https://github.com/danielemaurilli)

## 🙏 Acknowledgments

- The scientific community for research on eye movements in reading
- Clinical professionals who will use this tool to help children
- The Pygame community for the excellent framework

## ⚠️ Clinical Disclaimer

Tachistostory is a clinical **support tool** and does not replace a complete diagnostic assessment or structured therapeutic intervention. It must be used:

- By qualified professionals (psychologists, speech therapists, therapists)
- Within a broader therapeutic pathway
- With direct supervision during use with children
- In compliance with privacy regulations (GDPR) and professional ethical codes

The user is responsible for appropriate use of the software and compliance with applicable regulations.

##  Support

- 📖 [Wiki](https://github.com/danielemaurilli/tachistostory/wiki) (in development)
- 💬 [Discussions](https://github.com/danielemaurilli/tachistostory/discussions)
- 🐛 [Issues](https://github.com/danielemaurilli/tachistostory/issues)
- 📧 Email: maurillidaniele@gmail.com

---

**Developed with ❤️**

*Version 0.9.0 - December 2025*
