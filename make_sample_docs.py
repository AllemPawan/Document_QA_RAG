"""Generate four sample AI-ethics documents (.txt, .docx, .pdf x2) into ./docs."""
from pathlib import Path

import fitz  # PyMuPDF
from docx import Document

OUT = Path(__file__).parent / "docs"
OUT.mkdir(exist_ok=True)

BIAS = """Algorithmic Bias and Fairness in Deployed AI Systems

1. Sources of bias
Machine learning models learn patterns from historical data. When that data reflects past discrimination, the model reproduces it. Hiring tools trained on résumés of previously hired employees have downgraded candidates from underrepresented groups. Facial recognition systems have shown markedly higher error rates for darker-skinned women than for lighter-skinned men, largely because training sets under-sampled those groups. Bias can also enter through proxy variables: a postal code can stand in for race or income even when those attributes are removed.

2. Measuring fairness
There is no single definition of fairness. Demographic parity requires equal positive-outcome rates across groups; equalized odds requires equal error rates; calibration requires that predicted scores mean the same thing for every group. These criteria are mathematically incompatible in most real settings, so organizations must decide which trade-off is appropriate for the context and document that decision.

3. Mitigation
Mitigation can occur before training (rebalancing or auditing data), during training (fairness constraints), or after training (threshold adjustment). Independent audits, diverse development teams, and ongoing monitoring after deployment are recommended because bias can emerge as populations drift over time.
"""

PRIVACY = """Privacy, Surveillance and Data Governance in AI

1. Data collection at scale
Modern AI systems depend on large datasets that often contain personal information scraped or inferred without meaningful consent. Large language models can memorize and regurgitate fragments of training data, including names and contact details. Re-identification attacks show that supposedly anonymized datasets can often be linked back to individuals.

2. Surveillance
Facial recognition, emotion detection and behavioural tracking enable mass surveillance. Deployed in public spaces or workplaces, these tools chill free expression and association. Many jurisdictions now restrict real-time remote biometric identification, allowing narrow exceptions only for serious crimes.

3. Governance practices
Recommended practices include data minimization (collect only what is necessary), purpose limitation, privacy-by-design, differential privacy, and clear retention limits. The GDPR grants individuals rights of access, correction and erasure, and restricts solely automated decisions with significant effects on people. Organizations should run data protection impact assessments before launching high-risk AI applications.
"""

ACCOUNT = """Transparency, Accountability and Human Oversight

1. The black-box problem
Deep neural networks are often opaque: even their developers cannot fully explain individual predictions. In domains such as credit, healthcare and criminal justice, people affected by a decision deserve an explanation they can contest. Explainability techniques such as SHAP, LIME and counterfactual explanations offer partial insight but can be unfaithful to the model's real reasoning.

2. Accountability gaps
When an AI system causes harm, responsibility is diffuse across data providers, developers, deployers and users. Clear lines of accountability should be assigned before deployment. Model cards and datasheets for datasets document intended use, limitations and evaluation results, helping downstream users judge suitability.

3. Human oversight
Human-in-the-loop review is essential for high-stakes decisions, but oversight is only effective if reviewers have the time, training and authority to override the system. Automation bias, where people over-trust machine output, can make nominal oversight meaningless. Incident reporting and redress mechanisms should be available to affected individuals.
"""

SOCIETY = """Societal Impact: Labour, Misinformation and Safety

1. Labour market disruption
Automation driven by AI is expected to displace some tasks while creating others. Routine cognitive work, such as customer support and data entry, is most exposed. Without reskilling programmes and social safety nets, benefits may concentrate among capital owners while costs fall on displaced workers, widening inequality.

2. Misinformation
Generative models can produce realistic text, images and audio at negligible cost. Deepfakes and automated disinformation campaigns threaten elections and public trust. Proposed responses include content provenance standards such as watermarking and cryptographic signing, platform policies, and media literacy education.

3. Safety and environmental cost
As AI systems become more capable and autonomous, ensuring they behave as intended (alignment) and are robust to misuse becomes critical. Red-teaming and staged release help identify risks early. Training large models also consumes significant energy and water, so developers should report and reduce environmental footprints.

4. Regulation
The EU AI Act classifies systems by risk level, banning unacceptable-risk uses such as social scoring and imposing strict requirements on high-risk systems. Other frameworks, including the NIST AI Risk Management Framework, offer voluntary guidance centred on governing, mapping, measuring and managing risk.
"""


def pdf(name: str, text: str) -> None:
    doc = fitz.open()
    for chunk_start in range(0, len(text), 2200):  # crude pagination
        page = doc.new_page()
        page.insert_textbox(fitz.Rect(50, 50, 545, 790), text[chunk_start:chunk_start + 2200], fontsize=10)
    doc.save(OUT / name)


if __name__ == "__main__":
    (OUT / "algorithmic_bias.txt").write_text(BIAS, encoding="utf-8")
    d = Document()
    for para in PRIVACY.strip().split("\n\n"):
        d.add_paragraph(para)
    d.save(OUT / "privacy_surveillance.docx")
    pdf("transparency_accountability.pdf", ACCOUNT)
    pdf("societal_impact.pdf", SOCIETY)
    print("Wrote", [p.name for p in OUT.iterdir()])
