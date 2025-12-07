# Tachistostory

![License: Custom Non-Commercial](https://img.shields.io/badge/License-Custom_Non--Commercial-blue.svg)
![Clinical Use: Allowed](https://img.shields.io/badge/Clinical_Use-Allowed-green.svg)
![Version](https://img.shields.io/badge/version-0.9.0-orange.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

> Tachistoscopic application for enhancing reading skills through saccadic eye movement training

[🇮🇹 Italiano](README.md) | [🇬🇧 English](README_EN.md)

## 📋 Description

**Tachistostory** is an innovative clinical-educational tool designed to enhance children's reading skills through tachistoscopic technique. The application is based on solid neuroscientific principles regarding saccadic eye movements during reading.

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

### Training Progression

```
Week 1-2:  1200 ms → Tool familiarization
Week 3-4:  900 ms  → First significant reduction
Week 5-6:  600 ms  → Approaching natural time
Week 7-8:  400 ms  → Skill refinement
Week 9+:   250 ms  → Target time for fluent reading
```

*Note: Times are indicative and should be adapted to individual children*

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
2. **Training** (15 min): Session target time
3. **Cool-down** (5 min): Comprehension questions and feedback
4. **Recording**: Note time used, number of sentences, errors, perceived fatigue

### Comprehension Questions (Examples)

For sentence: *"The cat sleeps on the sofa"*

- **Literal**: "Who sleeps?" "Where does the cat sleep?"
- **Inferential**: "Do you think it's day or night?" "Is the cat tired?"
- **Memory**: "How many words did the sentence have?" "What was the third word?"

## 🎨 Customization

### Creating Custom Materials

Content can be adapted to:
- Child's **reading level**
- **Personal interests** (sports, animals, video games)
- **Specific goals** (new vocabulary, grammatical structures)
- **Curricular themes** (for school support)

### Content Suggestions

- Start with short words (3-5 letters)
- Use simple sentences (subject-verb-complement)
- Avoid complex syntactic structures initially
- Gradually increase complexity

## 📊 Progress Monitoring

### Indicators to Record
- Exposure time used
- Number of words/sentences completed
- Accuracy in sentence reconstruction
- Correct answers to comprehension questions
- Perceived fatigue level (scale 1-5)

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

Found a bug? [Open an issue](https://github.com/[username]/tachistostory/issues) describing:
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
  url = {https://github.com/[username]/tachistostory},
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

Tachistostory is a clinical **support tool** and does not replace a comprehensive diagnostic evaluation or structured therapeutic intervention. It should be used:

- By qualified professionals (psychologists, speech therapists, therapists)
- Within a broader therapeutic pathway
- With direct supervision during use with children
- In compliance with privacy regulations (GDPR) and professional codes of ethics

The user is responsible for appropriate use of the software and compliance with applicable regulations.

## 🔮 Future Roadmap

- [ ] Automatic progress tracking system
- [ ] Report generation for parents
- [ ] Pre-configured sentence database by age/level
- [ ] Multiplayer mode for friendly competition
- [ ] Interface-integrated comprehension questions
- [ ] Support for images associated with words
- [ ] Data export for statistical analysis

## 📞 Support

- 📖 [Wiki](https://github.com/[username]/tachistostory/wiki) (in development)
- 💬 [Discussions](https://github.com/[username]/tachistostory/discussions)
- 🐛 [Issues](https://github.com/[username]/tachistostory/issues)
- 📧 Email: maurillidaniele@gmail.com

---

**Developed with ❤️ to support children with reading difficulties**

*Version 0.9.0 - December 2025*